# Generated by Django 5.0.4 on 2024-06-26 09:19

from django.db import migrations


def set_age_group(apps, schema_editor):
    person = apps.get_model('main_app', 'Person')

    people = person.objects.all()

    for record in people:
        if record.age <= 12:
            record.age_group = 'Child'
        elif record.age <= 17:
            record.age_group = 'Teen'
        else:
            record.age_group = 'Adult'

    person.objects.bulk_update(people, ['age_group'])


def reverse_age_group(apps, schema_editor):
    person = apps.get_model('main_app', 'Person')
    people = person.objects.all()

    for record in people:
        record.age_group = person._meta.get_field('age_group').default

    person.objects.bulk_update(people, ['age_group'])


class Migration(migrations.Migration):
    dependencies = [
        ('main_app', '0009_person'),
    ]

    operations = [
        migrations.RunPython(set_age_group, reverse_age_group)
    ]
