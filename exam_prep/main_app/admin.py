from django.contrib import admin

from main_app.models import Director, Actor, Movie


# Register your models here.

@admin.register(Director)
class DirectorAdmin(admin.ModelAdmin):
    list_display = [
        'full_name',
        'birth_date',
        'nationality'
    ]

    list_filter = [
        'years_of_experience'
    ]

    search_fields = [
        'full_name',
        'nationality'
    ]


@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    list_display = [
        'full_name',
        'birth_date',
        'nationality'
    ]

    list_filter = [
        'is_awarded'
    ]

    search_fields = [
        'full_name'
    ]

    readonly_fields = [
        'last_updated'
    ]


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'rating',
        'director',
        'storyline'
    ]

    list_filter = [
        'is_awarded',
        'genre',
        'is_classic'
    ]

    readonly_fields = [
        'last_updated'
    ]

    search_fields = [
        'title',
        'director__full_name'
    ]

