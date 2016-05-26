from django.conf import settings
from django.conf.urls.defaults import patterns, url
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page
from django.views.generic import TemplateView

from models import *
from views import *


# short timeout - specifically meant to increase the speed of a short session rather than to service multiple users
URL_CACHE_TIME = 60 * 2
if settings.DEBUG:
    URL_CACHE_TIME = 5

urlpatterns = patterns(
    '',
    url(r'^competitions/$', CompetitionListView.as_view(), name='competitions'),

    url(r'^competitions/open/$',
        login_required(OpenCompetitionListView.as_view()),
        name='open_competitions'),

    url(r'^competitions/mine/$',
        login_required(MyCompetitionListView.as_view()),
        name='my_competitions'),

    url(r'^competitions/(?P<pk>\d+)/$',
        CompetitionDetailView.as_view(),
        name='competition'),

    url(r'^competitions/(?P<pk>\d+)/leaderboard/$',
        cache_page(
            CompetitionDetailView.as_view(template_name='tipping/_leaderboard_comp.html'),
            URL_CACHE_TIME
        ),
        name='competition_leaderboard'),

    url(r'^competitions/(?P<pk>\d+)/rounds/$',
        cache_page(
            CompetitionDetailView.as_view(template_name='tipping/_rounds_comp.html'),
            URL_CACHE_TIME
        ),
        name='competition_rounds'),

    url(r'^competitions/(?P<pk>\d+)/register/$',
        RegistrationFormView.as_view(),
        name='register'),

    url(r'^competitions/(?P<pk>\d+)/tippers/$',
        RegistrationListView.as_view(),
        name='tippers'),

    url(r'^competitions/(?P<pk>\d+)/upcoming/$',
        UpcomingRoundDetailView.as_view(),
        name='upcoming_round'),

    url(r'^rounds/(?P<pk>\d+)/$',
        RoundDetailView.as_view(),
        name='round'),

    url(r'^matches/(?P<pk>\d+)/$',
        MatchDetail.as_view(),
        name='match'),

    url(r'^tips/submit/$',
        login_required(TipFormView.as_view()),
        name='tip_form'),

    url(r'^tips/upcoming/$',
        login_required(UpcomingMatchesView.as_view()),
        name='upcoming_tips'),

    url(r'^$', TemplateView.as_view(template_name='tipping/index.html'), name='index'),
)
