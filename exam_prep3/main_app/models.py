from django.core.validators import MinLengthValidator, MinValueValidator, MaxValueValidator
from django.db import models

from main_app.managers import AuthorManager
from main_app.mixins import PublishedOnMixin, ContentMixin


# Create your models here.


class Author(models.Model):
    full_name = models.CharField(
        max_length=100,
        validators=[
            MinLengthValidator(3)
        ]
    )

    email = models.EmailField(unique=True)

    is_banned = models.BooleanField(default=False)
    birth_year = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1900),
            MaxValueValidator(2005)
        ]
    )

    website = models.URLField(blank=True, null=True)

    objects = AuthorManager()


class Article(PublishedOnMixin, ContentMixin):
    class CategoryChoices(models.TextChoices):
        TECHNOLOGY = 'Technology', 'Technology'
        SCIENCE = 'Science', 'Science'
        EDUCATION = 'Education', 'Education'

    title = models.CharField(
        max_length=200,
        validators=[
            MinLengthValidator(5)
        ],
    )
    category = models.CharField(
        max_length=10,
        choices=CategoryChoices,
        default=CategoryChoices.TECHNOLOGY
    )

    authors = models.ManyToManyField(Author, related_name='articles')


class Review(PublishedOnMixin, ContentMixin):
    rating = models.FloatField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5)
        ],
    )
    author = models.ForeignKey(Author, related_name='reviews', on_delete=models.CASCADE)
    article = models.ForeignKey(Article, related_name='reviews', on_delete=models.CASCADE)
