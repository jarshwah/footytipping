from tipping.models import Competition


def my_competitions(request):
    qs = Competition.objects.none()
    if request.user.is_authenticated():
        qs = Competition.objects.filter(registrations__user=request.user).select_related(depth=1)
    return {'my_competitions': qs}
