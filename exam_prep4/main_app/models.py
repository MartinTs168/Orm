from django.core.validators import MinLengthValidator, MaxValueValidator, MinValueValidator
from django.db import models

from main_app.managers import TennisPlayerManager


# Create your models here.


class TennisPlayer(models.Model):
    full_name = models.CharField(
        max_length=100,
        validators=[
            MinLengthValidator(5)
        ],
    )

    birth_date = models.DateField()
    country = models.CharField(
        max_length=100,
        validators=[
            MinLengthValidator(2)
        ],
    )

    ranking = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(300)
        ],
    )

    is_active = models.BooleanField(default=True)
    objects = TennisPlayerManager()


class Tournament(models.Model):
    class SurfaceTypeChoices(models.TextChoices):
        NOT_SELECTED = 'Not Selected', 'Not Selected'
        CLAY = 'Clay', 'Clay'
        GRASS = 'Grass', 'Grass'
        HARD_COURT = 'Hard Court', 'Hard Court'

    name = models.CharField(
        max_length=150,
        validators=[
            MinLengthValidator(2)
        ],
        unique=True,
    )

    location = models.CharField(
        max_length=100,
        validators=[
            MinLengthValidator(2)
        ],
    )

    prize_money = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    start_date = models.DateField()
    surface_type = models.CharField(
        max_length=12,
        choices=SurfaceTypeChoices,
        default=SurfaceTypeChoices.NOT_SELECTED,
    )


class Match(models.Model):
    score = models.CharField(
        max_length=100,
    )

    summary = models.TextField(
        validators=[
            MinLengthValidator(5)
        ],
    )

    date_played = models.DateTimeField()
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, related_name='matches')
    players = models.ManyToManyField(TennisPlayer, related_name='matches')
    winner = models.ForeignKey(
        TennisPlayer,
        on_delete=models.SET_NULL,
        related_name='won_matches',
        null=True,
    )

    class Meta:
        verbose_name_plural = 'Matches'

