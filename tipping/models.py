from django.db import models
from django.contrib.auth.models import User
from collections import defaultdict
from datetime import datetime


class Sport(models.Model):
    """
    Describes the sport that tipping will occur for, such as `AFL` or `NFL`. To account for different
    competitions in the same sport ie. VFL and AFL are both Australian Rules Football, use the name
    of the League.
    """
    description = models.CharField(max_length=200)

    def __unicode__(self):
        return self.description

    class Meta:
        ordering = ('description',)


class Team(models.Model):
    """
    Describes a Team that participates in a `Sport`.
    """
    sport = models.ForeignKey(Sport)
    name = models.CharField(max_length=100, help_text='The short name of the club eg: Melbourne')
    alias = models.CharField(max_length=100, blank=True, null=True, help_text='An alias eg: Cougars')

    class Meta:
        ordering = ('name',)

    def __unicode__(self):
        return u"%s %s" % (self.name, self.alias)

    @property
    def display_name(self):
        return self.alias or self.name


class Venue(models.Model):
    """
    Describes all the venues that can be used for `Matches`. In the case where a `Venue` is no longer
    used, the field `used_in_competition` should be set to `False` to maintain tipping history. It
    will no longer be valid for selection when creating new `Matches`.
    """
    sport = models.ForeignKey(Sport)
    teams = models.ManyToManyField(
        Team, related_name='home_grounds', help_text='Teams that call this venue a home ground')
    name = models.CharField(max_length=100, help_text='Name of the stadium, ground, or venue')
    used_in_competition = models.BooleanField(default=True)
    location = models.CharField(
        max_length=200,
        help_text='Description that allows tippers to understand where the Match takes place')

    class Meta:
        ordering = ('name', )

    def __unicode__(self):
        return u"%s (%s)" % (self.name, self.location)


class Competition(models.Model):
    """
    A `Competition` refers to a season of play that tipping will occur for.
    """
    sport = models.ForeignKey(Sport)
    season = models.CharField(max_length=50)
    start = models.DateTimeField(
        help_text='Registrations can not be made after this time')
    end = models.DateField(
        help_text='Winners will be shown after this date')
    fee = models.DecimalField(max_digits=7, decimal_places=2, default=0.00, verbose_name='Fee ($)')
    clean_sweep_extra_points = models.PositiveSmallIntegerField(
        default=0,
        help_text="How many extra points awarded for perfect tipping round?")
    notes = models.TextField(blank=True, null=True, help_text='Any other extra information useful to Tippers')

    class Meta:
        ordering = ('-start',)

    def __unicode__(self):
        return u"%s %s" % (self.sport, self.season)

    @property
    def is_open(self):
        return self.start > datetime.now()

    @classmethod
    def all_open(cls, user):
        return cls.objects.select_related(depth=1).filter(start__gt=datetime.now()).exclude(registrations__user=user)

    def get_upcoming_round(self):
        try:
            return self.get_future_rounds()[0]
        except IndexError:
            return None

    def get_played_rounds(self):
        return self.rounds.filter(start__lte=datetime.now())

    def get_future_rounds(self):
        return self.rounds.filter(end__gt=datetime.now())

    def ranked_registrations(self):
        # this looks terrible, but performs infinitely better than calculating each score as needed
        # (6 queries, down from 180 after 3 rounds of play)
        rounds = self.get_played_rounds().select_related(depth=1)
        registrations = self.registrations.select_related(depth=1)
        tips = Tip.objects.filter(registration__competition=self).select_related(depth=1)
        registration_tips = defaultdict(dict)  # {user:{matches:tips}}
        for tip in tips:
            for registration in registrations:
                if tip.registration_id == registration.id:
                    registration_tips[registration].update({tip.match: tip})

        for registration in registrations:
            score = sum(round.calculate_score(registration_tips.get(registration)) for round in rounds)
            registration._comp_score = score

        sorted_registrations = sorted(registrations, key=lambda registration: registration._comp_score, reverse=True)
        return sorted_registrations

    @models.permalink
    def get_absolute_url(self):
        return ('tipping:competition', [str(self.id)])


class Round(models.Model):
    """
    A week or round of play within a `Competition`.
    """
    competition = models.ForeignKey(Competition, related_name='rounds')
    description = models.CharField(max_length=20, help_text='The week or round number')
    start = models.DateTimeField()
    end = models.DateField()
    notes = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        ordering = ('competition', 'start')

    def __unicode__(self):
        return u"%s (%s - %s)" % (self.description, self.start, self.end)

    def calculate_score(self, tips):
        clean_sweep = True
        score = 0

        if not hasattr(self, '_matches'):
            self._matches = self.matches.all()

        for match in self._matches:
            tip = tips.get(match)
            if tip is None:
                clean_sweep = False
                guess_winner = match.away_team_id
            else:
                guess_winner = tip.winner_id

            if match.winner == "Draw":
                score += 1
                clean_sweep = False
            elif match.winner == "Home" and guess_winner == match.home_team_id:
                score += 1
            elif match.winner == "Away" and guess_winner == match.away_team_id:
                score += 1
            else:
                clean_sweep = False

        if clean_sweep:
            score += self.competition.clean_sweep_extra_points
        return score


class Match(models.Model):
    """
    A `Match` occurs between two `Team`s at a `Venue` in a particular `Round`. This is what tippers
    will `Tip` against.
    """

    winner_choices = (
        ('Home', 'Home Team'),
        ('Away', 'Away Team'),
        ('Draw', 'Draw')
    )

    round = models.ForeignKey(Round, related_name='matches')
    venue = models.ForeignKey(Venue, related_name='matches', limit_choices_to={'used_in_competition': True})
    home_team = models.ForeignKey(Team, related_name='home_matches')
    away_team = models.ForeignKey(Team, related_name='away_matches')
    kickoff = models.DateTimeField(help_text='No tips accepted after this time')
    winner = models.CharField(max_length=4, null=True, blank=True, choices=winner_choices, db_index=True)

    class Meta:
        verbose_name_plural = 'Matches'
        ordering = ('round', 'kickoff')

    def __unicode__(self):
        return u"%s (%s) @ %s" % (self.matchup, self.kickoff, self.venue.name)

    @property
    def matchup(self):
        if self.winner:
            if self.winner == 'Home':
                return u"%s defeated %s" % (self.home_team, self.away_team)
            elif self.winner == 'Away':
                return u"%s defeated by %s" % (self.home_team, self.away_team)
            else:
                return u"%s drew %s" % (self.home_team, self.away_team)

        return u"%s vs %s" % (self.home_team, self.away_team)

    @property
    def accepting_tips(self):
        return self.kickoff > datetime.now()

    def resolve_winner(self):
        if self.winner == "Home":
            return self.home_team.__unicode__()
        elif self.winner == "Away":
            return self.away_team.__unicode__()
        else:
            return self.winner


class Registration(models.Model):
    """
    `User`s need to register to `Tip` in a `Competition`. This ensures that `User`s can only compete
    by signing up before the `Competition` begins.
    """
    user = models.ForeignKey(User, related_name='registrations')
    competition = models.ForeignKey(Competition, related_name='registrations')
    paid = models.NullBooleanField(help_text='Tracks payment of registration fees if required')

    class Meta:
        ordering = ('competition', 'user')
        unique_together = ('user', 'competition')

    def __unicode__(self):
        return u"%s | %s" % (self.user, self.competition)

    def score_for_round(self, round):
        tips = dict((tip.match, tip) for tip in self.tips.filter(match__round=round).select_related(depth=1))
        return sum(r.calculate_score(tips) for r in self.competition.rounds.filter(id=round.id))

    @property
    def competition_score(self):
        if not hasattr(self, '_comp_score'):
            tips = dict((tip.match, tip) for tip in self.tips.filter().select_related(depth=1))
            qs = self.competition.rounds.filter(start__lte=datetime.now())
            self._comp_score = sum(round.calculate_score(tips) for round in qs)
        return self._comp_score


class Tip(models.Model):
    """
    Users `Tip` a winner of a particular `Match` that occurs in a `Competition` that they have
    Registered for.
    """
    registration = models.ForeignKey(Registration, related_name='tips')
    match = models.ForeignKey(Match, related_name='tips')
    winner = models.ForeignKey(Team, related_name='tips_to_win')

    class Meta:
        ordering = ('match', )
        unique_together = ('registration', 'match')

    def __unicode__(self):
        return u"%s tips %s in %s" % (self.registration.user, self.winner, self.match)
