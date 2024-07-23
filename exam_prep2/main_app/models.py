from django.core.validators import MinLengthValidator, MinValueValidator
from django.db import models

from main_app.managers import ProfileManager
from main_app.mixins import CreationDateMixin


# Create your models here.

class Profile(CreationDateMixin):
    full_name = models.CharField(
        max_length=100,
        validators=[
            MinLengthValidator(2)
        ]
    )

    email = models.EmailField()

    phone_number = models.CharField(
        max_length=15,
        help_text="This field is typically a string to accommodate various phone number formats.",
    )

    address = models.TextField(
        help_text="his field can store longer text, suitable for addresses."
    )

    is_active = models.BooleanField(default=True)

    objects = ProfileManager()

    def __str__(self):
        return self.full_name


class Product(CreationDateMixin):
    name = models.CharField(
        max_length=100,
    )

    description = models.TextField()

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[
            MinValueValidator(0.01)
        ]
    )

    in_stock = models.PositiveIntegerField()

    is_available = models.BooleanField(default=True)


class Order(CreationDateMixin):
    products = models.ManyToManyField(
        Product,
        related_name="orders",
    )

    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name="orders",
    )

    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[
            MinValueValidator(0.01)
        ]
    )

    is_completed = models.BooleanField(default=False)













