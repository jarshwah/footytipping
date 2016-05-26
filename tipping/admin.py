from django.contrib import admin
from models import Sport, Team, Venue, Competition, Round, Match, Registration, Tip


class TeamInline(admin.TabularInline):
    model = Team
    extra = 16


class MatchInline(admin.TabularInline):
    model = Match
    extra = 8


class TipInline(admin.TabularInline):
    model = Tip
    extra = 5


class SportAdmin(admin.ModelAdmin):
    search_fields = ('description',)
    inlines = [TeamInline]


class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'alias', 'sport')
    list_filter = ('sport',)
    search_fields = ('name', 'alias')
    ordering = ('name',)


class RegistrationAdmin(admin.ModelAdmin):
    readonly_fields = ('user', 'competition')


class VenueAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'used_in_competition', 'sport')
    list_filter = ('sport', 'used_in_competition')
    search_fields = ('name', 'location')
    ordering = ('name',)


class RoundAdmin(admin.ModelAdmin):
    list_display = ('description', 'start', 'end', 'competition')
    list_filter = ('competition', )
    search_fields = ('description', 'start')
    ordering = ('start',)

    inlines = [MatchInline]


class MatchAdmin(admin.ModelAdmin):
    list_display = ('matchup', 'kickoff', 'venue', 'winner')
    list_filter = ('winner', 'venue', 'round')
    search_fields = ('venue', 'matchup')
    ordering = ('kickoff',)
    inlines = [TipInline]  # shouldn't be allowed to see other users tips, even an admin.


class CompetitionAdmin(admin.ModelAdmin):
    list_display = ('sport', 'season', 'start', 'end')
    list_filter = ('sport', 'season')
    search_fields = ('sport', 'season')
    ordering = ('-start',)

admin.site.register(Sport, SportAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(Venue, VenueAdmin)
admin.site.register(Competition, CompetitionAdmin)
admin.site.register(Round, RoundAdmin)
admin.site.register(Match, MatchAdmin)
admin.site.register(Registration, RegistrationAdmin)
