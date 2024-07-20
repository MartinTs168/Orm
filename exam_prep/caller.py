import os
from decimal import Decimal

import django
from django.db.models import Q, Count, Avg, F

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Director, Actor, Movie


# Create queries within functions

def get_directors(search_name=None, search_nationality=None) -> str:
    if search_name is None and search_nationality is None:
        return ""

    if search_name and search_nationality:
        query = Q(full_name__icontains=search_name) & Q(nationality__icontains=search_nationality)
    elif search_name:
        query = Q(full_name__icontains=search_name)
    else:
        query = Q(nationality__icontains=search_nationality)

    directors = Director.objects.filter(query).order_by('full_name')
    if not directors:
        return ""
    result = []
    for d in directors:
        result.append(f"Director: {d.full_name}, nationality: {d.nationality}, experience: {d.years_of_experience}")

    return "\n".join(result)


def get_top_director() -> str:
    top_director = Director.objects.get_directors_by_movies_count().first()
    if not top_director:
        return ""

    return f"Top Director: {top_director.full_name}, movies: {top_director.movies_count}."


def get_top_actor() -> str:
    top_actor = Actor.objects.prefetch_related('starring_movies').annotate(
        movies_count=Count('starring_movies'),
        avg_rating=Avg('starring_movies__rating')
    ).filter(movies_count__gt=0).order_by('-movies_count', 'full_name').first()

    if not top_actor:
        return ""

    movies = ', '.join(movie.title for movie in top_actor.starring_movies.all() if movie)

    return (f"Top Actor: {top_actor.full_name}, starring in movies: {movies}, "
            f"movies average rating: {top_actor.avg_rating:.1f}")


def get_actors_by_movies_count() -> str:
    actors = Actor.objects.prefetch_related('actor_movies').annotate(movies_count=Count('actor_movies')).filter(
        movies_count__gt=0).order_by('-movies_count', 'full_name')[:3]

    if not actors:
        return ""

    result = []
    for a in actors:
        result.append(f"{a.full_name}, participated in {a.movies_count} movies")

    return "\n".join(result)


def get_top_rated_awarded_movie() -> str:
    movie = Movie.objects.select_related('starring_actor').prefetch_related('actors').filter(is_awarded=True).order_by(
        '-rating', 'title').first()

    if not movie:
        return ""

    starring_actor_name = movie.starring_actor.full_name if movie.starring_actor else "N/A"
    actors = ', '.join(a.full_name for a in movie.actors.order_by('full_name') if a)

    return (f"Top rated awarded movie: {movie.title}, rating: {movie.rating}. "
            f"Starring actor: {starring_actor_name}. Cast: {actors}.")


def increase_rating() -> str:
    updated_movies = Movie.objects.filter(
        is_classic=True,
        rating__lt=10.0
    )

    if not updated_movies:
        return "No ratings increased."

    updated_movies.update(rating=F('rating') + 0.1)
    updated_movies_count = updated_movies.count()
    return f"Rating increased for {updated_movies_count} movies."



