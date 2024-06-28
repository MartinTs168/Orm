# Generated by Django 5.0.4 on 2024-06-28 08:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0006_hotelroom'),
    ]

    operations = [
        migrations.CreateModel(
            name='Character',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('class_name', models.CharField(choices=[('WA', 'Warrior'), ('MG', 'Mage'), ('AS', 'Assassin'), ('SC', 'Scout')], max_length=20)),
                ('level', models.PositiveIntegerField()),
                ('strength', models.PositiveIntegerField()),
                ('dexterity', models.PositiveIntegerField()),
                ('intelligence', models.PositiveIntegerField()),
                ('hit_points', models.PositiveIntegerField()),
                ('inventory', models.TextField()),
            ],
        ),
    ]
