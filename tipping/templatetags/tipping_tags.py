from django.conf import settings
from django.template import Context, Template
from django.template.loader import get_template, render_to_string
from django import template
from tipping.forms import RegistrationForm, TipForm
from tipping.models import Registration, Competition, Tip
from django.contrib.auth.models import User

register = template.Library()

@register.filter
def can_register(user, competition):
    if user.is_authenticated() and competition.is_open:
        try:
            r = Registration.objects.get(competition=competition, user=user)
        except Registration.DoesNotExist:
            return True
    return False
    
@register.filter
def as_registration_form(competition, user):
    initial_data = {'competition':competition, 'user': user}
    form = RegistrationForm(initial=initial_data)
    return form

@register.filter
def tip_home_form(match, registration):
    return get_tipping_form(match, registration, match.home_team)
    
@register.filter
def tip_away_form(match, registration):
    return get_tipping_form(match, registration, match.away_team)

def get_tipping_form(match, registration, team):
    try:
        initial_data = {'match': match, 'registration': registration, 'tipped_team': team}
        form = TipForm(initial=initial_data)
        return form
    except Registration.DoesNotExist:
        return "<strong> Error Rendering Tipping Form </strong>"

@register.filter
def my_tip(registration, match):
    try:
        tip = get_tip(registration, match)
        return "Tipped %s" % tip.winner
    except Tip.DoesNotExist:
        return "No Tip. %s selected for you" % match.away_team
    except:
        return "<strong> Error </strong>"

@register.simple_tag
def tipped(registration, match, team):
    try:
        tip = get_tip(registration, match)
        if tip.winner == team:
            return "selected"
    except Exception,e:
        pass
    return ""

def get_tip(registration, match):
    cache_key = '_match_%s' % match.id
    tip = getattr(registration, cache_key, None)
    if tip is None:
        tip = Tip.objects.get(registration=registration, match=match)
        setattr(registration, cache_key, tip)
    return tip

@register.filter
def round_score(registration, round):
    return registration.score_for_round(round)

@register.filter
def get_registration(user, competition):
    try:
        return Registration.objects.get(user=user, competition=competition)
    except Registration.DoesNotExist:
        return None
