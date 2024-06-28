import os
import django
from django.db.models import F

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from main_app.models import Pet, Artifact, Location, Car, Task, HotelRoom, Character


# from populate_db import populate_model_with_data


def create_pet(name, species):
    Pet.objects.create(name=name, species=species)
    return f"{name} is a very cute {species}!"


# print(create_pet('Buddy', 'Dog'))
# print(create_pet('Whiskers', 'Cat'))
# print(create_pet('Rocky', 'Hamster'))


def create_artifact(name, origin, age, description, is_magical):
    Artifact.objects.create(
        name=name,
        origin=origin,
        age=age,
        description=description,
        is_magical=is_magical
    )
    return f"The artifact {name} is {age} years old!"


def rename_artifact(artifact: Artifact, new_name: str):
    if artifact.is_magical and artifact.age > 250:
        artifact.name = new_name
        artifact.save()


def delete_all_artifacts():
    Artifact.objects.all().delete()


def show_all_locations():
    result = ""
    for location in Location.objects.all().order_by('-id'):
        result += f"{location.name} has a population of {location.population}!\n"
    return result


def new_capital():
    location = Location.objects.first()
    location.is_capital = True
    location.save()


def get_capitals():
    return Location.objects.filter(is_capital=True).values('name')


def delete_first_location():
    Location.objects.first().delete()


def apply_discount():
    cars = Car.objects.all()

    for car in cars:
        discount = sum(int(digit) for digit in str(car.year)) / 100
        car.price_with_discount = float(car.price) - float(car.price) * discount

    Car.objects.bulk_update(cars, ['price_with_discount'])


def get_recent_cars():
    return Car.objects.filter(year__gt=2020).values('model', 'price_with_discount')


def delete_last_car():
    Car.objects.last().delete()


def show_unfinished_tasks():
    tasks = Task.objects.filter(is_finished=False)
    result = ""
    for task in tasks:
        result += f"Task - {task.title} needs to be done until {task.due_date}!\n"

    return result


def complete_odd_tasks():
    tasks = Task.objects.all()

    for task in tasks:
        if task.id % 2 != 0:
            task.is_finished = True
    Task.objects.bulk_update(tasks, ['is_finished'])


def encode_and_replace(text, task_title):
    decoded_text = ''.join(chr(ord(symbol) - 3) for symbol in text)
    Task.objects.filter(title=task_title).update(description=decoded_text)


def get_deluxe_rooms():
    rooms = HotelRoom.objects.filter(room_type='Deluxe')
    even_rooms = [str(r) for r in rooms if r.id % 2 == 0]

    return '\n'.join(even_rooms)


def increase_room_capacity():
    rooms = HotelRoom.objects.all().order_by('id')
    previous_room_capacity = None

    for room in rooms:
        if not room.is_reserved:
            continue

        if previous_room_capacity is not None:
            room.capacity += previous_room_capacity
        else:
            room.capacity += room.id

        previous_room_capacity = room.capacity

    HotelRoom.objects.bulk_update(rooms, ['capacity'])


def reserve_first_room():
    room = HotelRoom.objects.first()
    room.is_reserved = True
    room.save()


def delete_last_room():
    room = HotelRoom.objects.last()
    if not room.is_reserved:
        room.delete()


def update_characters():
    Character.objects.filter(class_name='Mage').update(
        level=F('level') + 3,
        intelligence=F('intelligence') - 7
    )
    Character.objects.filter(class_name='Warrior').update(
        hit_points=F('hit_points') / 2,
        dexterity=F('dexterity') + 4
    )
    Character.objects.filter(class_name__in=['Assassin', 'Scout']).update(
        inventory='The inventory is empty'
    )


def fuse_characters(first_character: Character, second_character: Character):
    fusion_name = f"{first_character.name} {second_character.name}"
    class_name = 'Fusion'
    level = (first_character.level + second_character.level) / 2
    strength = (first_character.strength + second_character.strength) * 1.2
    dexterity = (first_character.dexterity + second_character.dexterity) * 1.4
    intelligence = (first_character.intelligence + second_character.intelligence) * 1.5
    hit_points = (first_character.hit_points + second_character.hit_points)
    inventory = 'Bow of the Elven Lords, Amulet of Eternal Wisdom' if first_character.class_name in ('Mage', 'Scout') \
        else 'Dragon Scale Armor, Excalibur'

    Character.objects.create(
        name=fusion_name,
        class_name=class_name,
        level=level,
        strength=strength,
        dexterity=dexterity,
        intelligence=intelligence,
        hit_points=hit_points,
        inventory=inventory
    )

    first_character.delete()
    second_character.delete()


def grand_dexterity():
    Character.objects.all().update(
        dexterity=30
    )


def grand_strength():
    Character.objects.all().update(
        strength=50
    )


def grand_intelligence():
    Character.objects.all().update(
        intelligence=40
    )


def delete_characters():
    Character.objects.filter(inventory='The inventory is empty').delete()
