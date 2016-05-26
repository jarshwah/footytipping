from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.template.loader import render_to_string
from django.views.generic import ListView, FormView, DetailView
from django.utils import simplejson
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from models import *
from forms import *


class AjaxFormView(FormView):
    def ajax_response(self, context, success=True):
        html = render_to_string(self.template_name, context)
        response = simplejson.dumps({'success': success, 'html': html})
        return HttpResponse(response, content_type="application/json", mimetype='application/json')


class RegistrationFormView(AjaxFormView):
    form_class = RegistrationForm
    template_name = "tipping/register_form.html"

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(RegistrationFormView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        registration = form.save()
        if self.request.is_ajax():
            context = {'competition': registration.competition}
            return self.ajax_response(context, success=True)
        return HttpResponseRedirect(registration.competition.get_absolute_url())

    def form_invalid(self, form):
        if self.request.is_ajax():
            context = {'errors': 'Error Occurred'}
            return self.ajax_response(context, success=False)
        return render_to_response(self.template_name, {'errors': form.errors})


class TipFormView(AjaxFormView):
    form_class = TipForm
    template_name = "tipping/tip_form.html"

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if not request.is_ajax():
            raise Http404
        return super(TipFormView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        registration = form.cleaned_data['registration']
        user = self.request.user
        if registration.user != user:
            context = {'match': tip.match, 'errors': 'cant vote for someone else!'}
            return self.ajax_response(context, success=False)
        tip = form.save()
        context = {'match': tip.match, 'tip': tip}
        return self.ajax_response(context, success=True)

    def form_invalid(self, form):
        context = {'errors': form.errors}
        return self.ajax_response(context, success=False)


class RegistrationListView(ListView):
    context_object_name = "registrations"
    template_name = "tipping/tippers_list.html"

    def get_queryset(self):
        self.competition = get_object_or_404(Competition, id=self.kwargs.get("pk"))
        return Registration.objects.filter(competition=self.competition).select_related(depth=1)

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(RegistrationListView, self).get_context_data(**kwargs)
        kwargs.get("pk")
        context['competition'] = self.competition
        return context


class CompetitionListView(ListView):
    context_object_name = 'competitions'
    template_name = 'tipping/competition_list.html'
    model = Competition

    def get_context_data(self, **kwargs):
        context = super(CompetitionListView, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated():
            registrations = Registration.objects.filter(user=self.request.user)
            context['registrations'] = registrations
        return context


class OpenCompetitionListView(CompetitionListView):

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(OpenCompetitionListView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Competition.all_open(self.request.user)


class MyCompetitionListView(OpenCompetitionListView):

    def get_queryset(self):
        return Competition.objects.filter(registrations__user=self.request.user)


class UpcomingMatchesView(MyCompetitionListView):
    template_name = 'tipping/upcoming_tips.html'


class FutureRoundsListView(MyCompetitionListView):
    template_name = 'tipping/future_rounds_list.html'


class CompetitionDetailView(DetailView):
    context_object_name = 'competition'
    template_name = 'tipping/competition_detail.html'
    model = Competition

    def get_context_data(self, **kwargs):
        context = super(CompetitionDetailView, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated():
            competition = self.object
            try:
                registration = Registration.objects.get(competition=competition, user=self.request.user)
                context['registration'] = registration
            except Registration.DoesNotExist:
                pass
        return context


class RoundListView(ListView):
    context_object_name = 'rounds'
    template_name = 'tipping/round_list.html'
    model = Round

    def get_query_set(self):
        competition_id = self.kwargs.get('competition_id')
        return Round.objects.filter(competition_id=competition_id)

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(RoundListView, self).get_context_data(**kwargs)
        competition = get_object_or_404(Competition, id=self.kwargs.get('competition_id'))
        context['competition'] = competition
        if self.request.user.is_authenticated():
            try:
                registration = Registration.objects.get(competition=competition, user=self.request.user)
                context['registration'] = registration
            except Registration.DoesNotExist:
                pass
        return context


class RoundDetailView(DetailView):
    context_object_name = 'round'
    template_name = 'tipping/round_detail.html'
    model = Round

    def get_context_data(self, **kwargs):
        context = super(RoundDetailView, self).get_context_data(**kwargs)
        if self.object is None:
            return context

        context['matches'] = self.object.matches.select_related(depth=2)
        if self.request.user.is_authenticated():
            try:
                registration = Registration.objects.get(competition=self.object.competition, user=self.request.user)
                context['registration'] = registration
            except Registration.DoesNotExist:
                pass
        return context


class UpcomingRoundDetailView(RoundDetailView):

    def get_object(self):
        # uses one more query than necessary, but contains logic in the model
        competition_id = self.kwargs.get('pk')
        return Competition.objects.get(id=competition_id).get_upcoming_round()


class MatchDetail(DetailView):
    context_object_name = 'match'
    template_name = 'tipping/match_detail.html'
    model = Match

    def get_object(self):
        return Match.objects.select_related(depth=2).get(id=self.kwargs.get('pk'))

    def get_context_data(self, **kwargs):
        context = super(MatchDetail, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated():
            try:
                registration = Registration.objects.get(
                    competition=self.object.round.competition, user=self.request.user)
                context['registration'] = registration
            except Registration.DoesNotExist:
                pass
        return context
