import os
import django
from django.db.models import Count

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import TennisPlayer, Tournament, Match


# Create queries within functions

def get_tennis_players(search_name=None, search_country=None) -> str:
    if search_name is not None and search_country is not None:
        players = TennisPlayer.objects.filter(
            full_name__icontains=search_name,
            country__icontains=search_country
        ).order_by('ranking')
    elif search_country is not None:
        players = TennisPlayer.objects.filter(country__icontains=search_country).order_by('ranking')

    elif search_name is not None:
        players = TennisPlayer.objects.filter(full_name__icontains=search_name).order_by('ranking')

    else:
        return ""

    result = []
    for player in players:
        result.append(f"Tennis Player: {player.full_name}, country: {player.country}, ranking: {player.ranking}")

    return '\n'.join(result)


def get_top_tennis_player():
    player = TennisPlayer.objects.get_tennis_players_by_wins_count().first()

    if player:
        return f"Top Tennis Player: {player.full_name} with {player.num_wins} wins."

    return ""


def get_tennis_player_by_matches_count():
    player = TennisPlayer.objects.annotate(num_matches=Count('matches')).order_by('-num_matches', 'ranking').first()

    if not player or player.num_matches == 0:
        return ""

    return f"Tennis Player: {player.full_name} with {player.num_matches} matches played."


def get_tournaments_by_surface_type(surface=None):
    if surface is None:
        return ""

    tournaments = Tournament.objects.filter(surface_type__icontains=surface).order_by('-start_date')

    if not tournaments:
        return ""

    result = []
    for t in tournaments:
        result.append(f"Tournament: {t.name}, start date: {t.start_date}, matches: {t.matches.count()}")

    return '\n'.join(result)


def get_latest_match_info():
    match = Match.objects.prefetch_related('players').order_by('-date_played', '-id').first()

    if not match:
        return ""

    players_names = match.players.values_list('full_name', flat=True)

    return (f"Latest match played on: {match.date_played}, tournament: {match.tournament.name}, "
            f"score: {match.score}, players: {' vs '.join(players_names)}, "
            f"winner: {match.winner.full_name if match.winner else 'TBA'}, summary: {match.summary}")


def get_matches_by_tournament(tournament_name=None):
    if tournament_name is None:
        return "No matches found."

    matches = Match.objects.filter(tournament__name=tournament_name).order_by('-date_played')

    if not matches:
        return "No matches found."

    result = []
    for m in matches:
        result.append(
            f"Match played on: {m.date_played}, score: {m.score}, winner: {m.winner.full_name if m.winner else 'TBA'}")

    return '\n'.join(result)


print(get_latest_match_info())