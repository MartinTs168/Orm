from django.core.validators import MinLengthValidator, MaxLengthValidator, MinValueValidator, MaxValueValidator
from django.db import models

from main_app.managers import DirectorManager


# Create your models here.


class AwardedMixin(models.Model):
    is_awarded = models.BooleanField(default=False)

    class Meta:
        abstract = True


class BasePerson(models.Model):
    full_name = models.CharField(
        max_length=120,
        validators=[
            MinLengthValidator(2),
            MaxLengthValidator(120)
        ]
    )

    birth_date = models.DateField(default="1900-01-01")

    nationality = models.CharField(
        max_length=50,
        default="Unknown",
    )

    class Meta:
        abstract = True


class Director(BasePerson):
    years_of_experience = models.SmallIntegerField(
        default=0,
        validators=[
            MinValueValidator(0)
        ]
    )

    objects = DirectorManager()


class Actor(BasePerson, AwardedMixin):
    last_updated = models.DateTimeField(auto_now=True)


class Movie(AwardedMixin):
    class GenreChoices(models.TextChoices):
        ACTION = "Action", "Action"
        DRAMA = "Drama", "Drama"
        COMEDY = "Comedy", "Comedy"
        OTHER = "Other", "Other"

    title = models.CharField(
        max_length=150,
        validators=[
            MinLengthValidator(5)
        ],
    )

    release_date = models.DateField()
    storyline = models.TextField(null=True, blank=True)
    genre = models.CharField(
        max_length=6,
        validators=[
            MaxLengthValidator(6)
        ],
        default=GenreChoices.OTHER,
        choices=GenreChoices.choices,
    )

    rating = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        validators=[
            MinValueValidator(0.0),
            MaxValueValidator(10.0)
        ],
        default=0.0
    )

    is_classic = models.BooleanField(default=False)
    last_updated = models.DateTimeField(auto_now=True)
    director = models.ForeignKey(
        Director,
        on_delete=models.CASCADE,
        related_name='movies'
    )
    starring_actor = models.ForeignKey(
        Actor,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='starring_movies'
    )

    actors = models.ManyToManyField(Actor, related_name="actor_movies")



