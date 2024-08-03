import os
import django
from django.db.models import Q, Count, F, Avg

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Astronaut, Spacecraft, Mission


# Create queries within functions


def get_astronauts(search_string=None):
    if search_string is None:
        return ""

    query = Q(name__icontains=search_string) | Q(phone_number__icontains=search_string)
    astronauts = Astronaut.objects.filter(query).order_by('name')

    if not astronauts:
        return ""

    result = []

    for a in astronauts:
        result.append(f"Astronaut: {a.name}, phone number: {a.phone_number}, "
                      f"status: {'Active' if a.is_active else 'Inactive'}")

    return "\n".join(result)


def get_top_astronaut():
    top_a = Astronaut.objects.get_astronauts_by_missions_count().first()

    if not top_a or top_a.missions_count == 0:
        return 'No data.'

    return f"Top Astronaut: {top_a.name} with {top_a.missions_count} missions."


def get_top_commander():
    top_c = Astronaut.objects.annotate(
        commanded_missions_count=Count('commanded_missions')
    ).filter(commanded_missions_count__gt=0).order_by('-commanded_missions_count', 'phone_number').first()

    if not top_c:
        return 'No data.'

    return f"Top Commander: {top_c.name} with {top_c.commanded_missions_count} commanded missions."


def get_last_completed_mission():
    mission = Mission.objects.prefetch_related('astronauts').select_related('commander', 'spacecraft').filter(
        status='Completed').order_by('-launch_date').first()

    if not mission:
        return "No data."

    a_names = ', '.join(mission.astronauts.order_by('name').values_list('name', flat=True))
    spacewalks = sum(a.spacewalks for a in mission.astronauts.all())

    return (f"The last completed mission is: {mission.name}. "
            f"Commander: {mission.commander.name if mission.commander else 'TBA'}. "
            f"Astronauts: {a_names}. Spacecraft: {mission.spacecraft.name}. "
            f"Total spacewalks: {spacewalks}.")


def get_most_used_spacecraft():
    spacecraft = Spacecraft.objects.prefetch_related('missions', 'missions__astronauts').annotate(
        missions_count=Count('missions')
    ).filter(missions_count__gt=0).order_by('-missions_count', 'name').first()

    if not spacecraft:
        return "No data."

    num_unique_a_on_spacecraft = len(set(a for mission in spacecraft.missions.all() for a in mission.astronauts.all()))

    return (f"The most used spacecraft is: {spacecraft.name}, "
            f"manufactured by {spacecraft.manufacturer}, used in {spacecraft.missions_count} missions, "
            f"astronauts on missions: {num_unique_a_on_spacecraft}.")


def decrease_spacecrafts_weight():
    spacecrafts_count = Spacecraft.objects.prefetch_related('missions').filter(
        missions__status='Planned',
        weight__gte=200.0
    ).update(weight=F('weight') - 200.0)

    if spacecrafts_count == 0:
        return "No changes in weight."

    avg_weight = Spacecraft.objects.aggregate(avg_weight=Avg('weight'))['avg_weight']

    return (f"The weight of {spacecrafts_count} "
            f"spacecrafts has been decreased. The new average weight of all spacecrafts is {avg_weight:.1f}kg")


