from datetime import datetime
from django import forms
from models import Registration, Competition, Tip, Match, User, Team


class RegistrationForm(forms.Form):
    """
    Allows a `User` to register for a `Competition`
    """

    user = forms.ModelChoiceField(widget=forms.HiddenInput(), queryset=User.objects.filter())
    competition = forms.ModelChoiceField(widget=forms.HiddenInput(), queryset=Competition.objects.filter())

    def clean(self):
        user = self.cleaned_data.get('user')
        competition = self.cleaned_data.get('competition')

        if user and competition:
            try:
                Registration.objects.get(competition=competition, user=user)
                # already registered...
            except Registration.DoesNotExist:
                pass

        return self.cleaned_data

    def clean_competition(self):
        competition = self.cleaned_data.get('competition')
        if not competition.is_open:
            raise forms.ValidationError('This competition is not open for registration.')
        return competition

    def save(self):
        data = self.cleaned_data
        user = data['user']
        competition = data['competition']
        r = Registration(user=user, competition=competition)
        r.save()
        return r


class TipForm(forms.Form):
    """
    Allows a `Registration` to `Tip` a `Match`.

    Validation:
        * match.kickoff must be in the future
        * tipped_team must exist in (match.away_team, match.home_team)
        * registration.competition must equal match.round.competition

    """

    registration = forms.ModelChoiceField(widget=forms.HiddenInput(), queryset=Registration.objects.filter())
    match = forms.ModelChoiceField(widget=forms.HiddenInput(), queryset=Match.objects.filter())
    tipped_team = forms.ModelChoiceField(widget=forms.HiddenInput(), queryset=Team.objects.filter())

    def clean(self):
        registration = self.cleaned_data.get('registration')
        match = self.cleaned_data.get('match')
        tipped_team = self.cleaned_data.get('tipped_team')

        if registration and match and tipped_team:
            if tipped_team.id not in (match.away_team_id, match.home_team_id):
                raise forms.ValidationError("Your tip was not for a valid team in this match")
            if registration.competition_id != match.round.competition_id:
                raise forms.ValidationError("Can't tip a team in a competition you're not registered for")
        return self.cleaned_data

    def clean_match(self):
        match = self.cleaned_data.get('match')
        if match.kickoff < datetime.now():
            raise forms.ValidationError('Tips can not longer be placed for this Match')
        return match

    def save(self):
        registration = self.cleaned_data.get('registration')
        match = self.cleaned_data.get('match')
        tipped_team = self.cleaned_data.get('tipped_team')
        try:
            tip = Tip.objects.get(registration=registration, match=match)
        except Tip.DoesNotExist:
            tip = Tip(registration=registration, match=match)
        tip.winner = tipped_team
        tip.save()
        return tip
