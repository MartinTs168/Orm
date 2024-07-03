import os
import django
from django.db.models import Case, When, Value

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models
# Create and check models
# Run and print your queries
from main_app.models import ArtworkGallery, Laptop, ChessPlayer, Meal, Dungeon, Workout


def show_highest_rated_art():
    best_work = ArtworkGallery.objects.order_by('-rating', 'id').first()
    return f"{best_work.art_name} is the highest-rated art with a {best_work.rating} rating!"


def bulk_create_arts(first_art: ArtworkGallery, second_art: ArtworkGallery):
    ArtworkGallery.objects.bulk_create([first_art, second_art])


def delete_negative_rated_arts():
    ArtworkGallery.objects.filter(rating__lt=0).delete()


def show_the_most_expensive_laptop():
    most_expensive_laptop = Laptop.objects.order_by('-price', '-id').first()
    return (f"{most_expensive_laptop.brand} is "
            f"the most expensive laptop available for {most_expensive_laptop.price}$!")


def bulk_create_laptops(args):
    Laptop.objects.bulk_create(args)


def update_to_512_GB_storage():
    Laptop.objects.filter(brand__in=('Asus', 'Lenovo')).update(storage=512)


def update_to_16_GB_memory():
    Laptop.objects.filter(brand__in=('Apple', 'Dell', 'Acer')).update(memory=16)


def update_operation_systems():
    Laptop.objects.filter(brand='Asus').update(operation_system='Windows')
    Laptop.objects.filter(brand='Apple').update(operation_system='MacOS')
    Laptop.objects.filter(brand='Lenovo').update(operation_system='Chrome OS')
    Laptop.objects.filter(brand__in=('Dell', 'Acer')).update(operation_system='Linux')


def delete_inexpensive_laptops():
    Laptop.objects.filter(price__lt=1200).delete()


def bulk_create_chess_players(args):
    ChessPlayer.objects.bulk_create(args)


def delete_chess_players():
    ChessPlayer.objects.filter(title='no title').delete()


def change_chess_games_won():
    ChessPlayer.objects.filter(title='GM').update(games_won=30)


def change_chess_games_lost():
    ChessPlayer.objects.filter(title='no title').update(games_lost=25)


def change_chess_games_drawn():
    ChessPlayer.objects.update(games_drawn=10)


def grand_chess_title_GM():
    ChessPlayer.objects.filter(rating__gte=2400).update(title='GM')


def grand_chess_title_IM():
    ChessPlayer.objects.filter(rating__range=[2300, 2399]).update(title='IM')


def grand_chess_title_FM():
    ChessPlayer.objects.filter(rating__range=[2200, 2299]).update(title='FM')


def grand_chess_title_regular_player():
    ChessPlayer.objects.filter(rating__range=[0, 2199]).update(title='regular player')


def set_new_chefs():
    Meal.objects.update(
        chef=Case(
            When(meal_type='Breakfast', then=Value('Gordon Ramsay')),
            When(meal_type='Lunch', then=Value('Julia Child')),
            When(meal_type='Dinner', then=Value('Jamie Oliver')),
            When(meal_type='Snack', then=Value('Thomas Keller'))
        )
    )


def set_new_preparation_times():
    Meal.objects.update(
        preparation_time=Case(
            When(meal_type='Breakfast', then=Value('10 minutes')),
            When(meal_type='Lunch', then=Value('12 minutes')),
            When(meal_type='Dinner', then=Value('15 minutes')),
            When(meal_type='Snack', then=Value('5 minutes'))
        )
    )


def update_low_calorie_meals():
    Meal.objects.filter(meal_type__in=('Breakfast', 'Dinner')).update(calories=400)


def update_high_calorie_meals():
    Meal.objects.filter(meal_type__in=('Lunch', 'Snack')).update(calories=700)


def delete_lunch_and_snack_meals():
    Meal.objects.filter(meal_type__in=('Lunch', 'Snack')).delete()


# meal1 = Meal.objects.create(
#     name="Pancakes",
#     meal_type="Breakfast",
#     preparation_time="20 minutes",
#     difficulty=3,
#     calories=350,
#     chef="Jane",
# )
#
# meal2 = Meal.objects.create(
#     name="Spaghetti Bolognese",
#     meal_type="Dinner",
#     preparation_time="45 minutes",
#     difficulty=4,
#     calories=550,
#     chef="Sarah",
# )
# # Test the set_new_chefs function
# set_new_chefs()
#
# # Test the set_new_preparation_times function
# set_new_preparation_times()
#
# # Refreshes the instances
# meal1.refresh_from_db()
# meal2.refresh_from_db()
#
# # Print the updated meal information
# print("Meal 1 Chef:", meal1.chef)
# print("Meal 1 Preparation Time:", meal1.preparation_time)
# print("Meal 2 Chef:", meal2.chef)
# print("Meal 2 Preparation Time:", meal2.preparation_time)


def show_hard_dungeons():
    hard_dungeons = Dungeon.objects.filter(difficulty='Hard').order_by('-location')
    return '\n'.join([f"{d.name} is guarded by {d.boss_name} "
                      f"who has {d.boss_health} health points!" for d in hard_dungeons])


def bulk_create_dungeons(dungeon_list):
    Dungeon.objects.bulk_create(dungeon_list)


def update_dungeon_names():
    Dungeon.objects.update(
        name=Case(
            When(difficulty='Easy', then=Value('The Erased Thombs')),
            When(difficulty='Medium', then=Value('The Coral Labyrinth')),
            When(difficulty='Hard', then=Value('The Lost Haunt'))
        )
    )


def update_dungeon_bosses_health():
    Dungeon.objects.exclude(difficulty='Easy').update(boss_health=500)


def update_dungeon_recommended_levels():
    Dungeon.objects.update(
        recommended_level=Case(
            When(difficulty='Easy', then=25),
            When(difficulty='Medium', then=50),
            When(difficulty='Hard', then=75)
        )
    )


def update_dungeon_rewards():
    Dungeon.objects.update(
        reward=Case(
            When(location__endswith='s', then=Value('Dragonheart Amulet')),
            When(location__startswith='E', then=Value('New dungeon unlocked')),
            When(boss_health=500, then=Value('1000 Gold'))
        )
    )


def set_new_locations():
    Dungeon.objects.update(
        location=Case(
            When(recommended_level=25, then=Value('Enchanted Maze')),
            When(recommended_level=50, then=Value('Grimstone Mines')),
            When(recommended_level=75, then=Value('Shadowed Abyss'))
        )
    )


# Create two instances
# dungeon1 = Dungeon(
#     name="Dungeon 1",
#     boss_name="Boss 1",
#     boss_health=1000,
#     recommended_level=75,
#     reward="Gold",
#     location="Eternal Hell",
#     difficulty="Hard",
# )
#
# dungeon2 = Dungeon(
#     name="Dungeon 2",
#     boss_name="Boss 2",
#     boss_health=400,
#     recommended_level=25,
#     reward="Experience",
#     location="Crystal Caverns",
#     difficulty="Easy",
# )
#
# # Bulk save the instances
# bulk_create_dungeons([dungeon1, dungeon2])
#
# # Update boss's health
# update_dungeon_bosses_health()
#
# # Show hard dungeons
# hard_dungeons_info = show_hard_dungeons()
# print(hard_dungeons_info)
#
# # Change dungeon names based on difficulty
# update_dungeon_names()
# dungeons = Dungeon.objects.order_by('boss_health')
# print(dungeons[0].name)
# print(dungeons[1].name)
#
# # Change the dungeon rewards
# update_dungeon_rewards()
# dungeons = Dungeon.objects.order_by('boss_health')
# print(dungeons[0].reward)
# print(dungeons[1].reward)


def show_workouts():
    workouts = Workout.objects.filter(workout_type__in=('CrossFit', 'Calisthenics')).order_by('id')
    return '\n'.join([f"{w.name} from {w.workout_type} type has {w.difficulty} difficulty!" for w in workouts])


def get_high_difficulty_cardio_workouts():
    return Workout.objects.filter(workout_type='Cardio', difficulty='High').order_by('instructor')


def set_new_instructors():
    Workout.objects.update(
        instructor=Case(
            When(workout_type='Cardio', then=Value('John Smith')),
            When(workout_type='Strength', then=Value('Michael Williams')),
            When(workout_type='Yoga', then=Value('Emily Johnson')),
            When(workout_type='CrossFit', then=Value('Sarah Davis')),
            When(workout_type='Calisthenics', then=Value('Chris Heria'))
        )
    )


def set_new_duration_times():
    Workout.objects.update(
        duration=Case(
            When(instructor='John Smith', then=Value('15 minutes')),
            When(instructor='Sarah Davis', then=Value('30 minutes')),
            When(instructor='Chris Heria', then=Value('45 minutes')),
            When(instructor='Michael Williams', then=Value('1 hour')),
            When(instructor='Emily Johnson', then=Value('1 hour and 30 minutes'))
        )
    )


def delete_workouts():
    Workout.objects.exclude(workout_type__in=('Strength', 'Calisthenics')).delete()


# Create two Workout instances
# workout1 = Workout.objects.create(
#     name="Push-Ups",
#     workout_type="Calisthenics",
#     duration="10 minutes",
#     difficulty="Intermediate",
#     calories_burned=200,
#     instructor="Bob"
# )
#
# workout2 = Workout.objects.create(
#     name="Running",
#     workout_type="Cardio",
#     duration="30 minutes",
#     difficulty="High",
#     calories_burned=400,
#     instructor="Lilly"
# )
#
# # Run the functions
# print(show_workouts())
#
# high_difficulty_cardio_workouts = get_high_difficulty_cardio_workouts()
# for workout in high_difficulty_cardio_workouts:
#     print(f"{workout.name} by {workout.instructor}")
#
# set_new_instructors()
# for workout in Workout.objects.all():
#     print(f"Instructor: {workout.instructor}")
#
# set_new_duration_times()
# for workout in Workout.objects.all():
#     print(f"Duration: {workout.duration}")