from django.core.validators import MinLengthValidator, RegexValidator, MinValueValidator
from django.db import models

from main_app.managers import AstronautManager
from main_app.mixins import LaunchDateMixin, UpdatedAtMixin


# Create your models here.

class Astronaut(UpdatedAtMixin):
    name = models.CharField(
        max_length=120,
        validators=[
            MinLengthValidator(2)
        ]
    )

    phone_number = models.CharField(
        unique=True,
        validators=[
            RegexValidator(r'^\d{1,15}$')
        ],
        max_length=15
    )

    is_active = models.BooleanField(
        default=True
    )

    date_of_birth = models.DateField(
        null=True,
        blank=True
    )

    spacewalks = models.IntegerField(
        default=0,
        validators=[
            MinValueValidator(0)
        ]
    )

    objects = AstronautManager()


class Spacecraft(LaunchDateMixin, UpdatedAtMixin):
    name = models.CharField(
        max_length=120,
        validators=[
            MinLengthValidator(2)
        ]

    )

    manufacturer = models.CharField(
        max_length=100,
    )

    capacity = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1)
        ]
    )

    weight = models.FloatField(
        validators=[
            MinValueValidator(0.0)
        ]
    )


class Mission(LaunchDateMixin, UpdatedAtMixin):
    class StatusChoices(models.TextChoices):
        PLANNED = 'Planned', 'Planned'
        ONGOING = 'Ongoing', 'Ongoing'
        COMPLETED = 'Completed', 'Completed'

    name = models.CharField(
        max_length=120,
        validators=[
            MinLengthValidator(2)
        ]
    )

    description = models.TextField(
        blank=True,
        null=True,
    )

    status = models.CharField(
        max_length=9,
        choices=StatusChoices,
        default=StatusChoices.PLANNED
    )

    spacecraft = models.ForeignKey(Spacecraft, on_delete=models.CASCADE, related_name='missions')

    astronauts = models.ManyToManyField(
        Astronaut,
        related_name='missions'
    )

    commander = models.ForeignKey(
        Astronaut,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='commanded_missions'
    )
