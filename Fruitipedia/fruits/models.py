from django.core.validators import MinLengthValidator
from django.db import models

from fruits.validators import OnlyLettersValidator


# Create your models here.


class Category(models.Model):
    name = models.CharField(unique=True, max_length=100)

    def __str__(self):
        return self.name


class Fruit(models.Model):
    name = models.CharField(
        max_length=30,
        validators=[
            MinLengthValidator(2),
            OnlyLettersValidator()
        ]
    )

    image_url = models.URLField()
    description = models.TextField()
    nutrition = models.TextField(null=True, blank=True)

    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
