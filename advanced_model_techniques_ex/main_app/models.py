from decimal import Decimal

from django.contrib.postgres.search import SearchVectorField
from django.db import models
from django.core.validators import MinValueValidator, RegexValidator, MinLengthValidator

from main_app.mixins import RechargeEnergyMixin
from main_app.validators import ValidateName


# Create your models here.

class Customer(models.Model):
    name = models.CharField(
        max_length=100,
        validators=[
            ValidateName("Name can only contain letters and spaces"),
        ],

    )

    age = models.PositiveIntegerField(
        validators=[
            MinValueValidator(18, message="Age must be greater than or equal to 18")
        ],
    )

    email = models.EmailField(
        error_messages={
            "invalid": "Enter a valid email address"
        },
    )

    phone_number = models.CharField(
        max_length=13,
        validators=[
            RegexValidator(
                regex=r"^\+359\d{9}$",  # ^ starts with \d is digits {9} length $ signifies end of string
                message="Phone number must start with '+359' followed by 9 digits"
            )
        ],
    )

    website_url = models.URLField(
        error_messages={
            "invalid": "Enter a valid URL"
        },
    )


class BaseMedia(models.Model):
    title = models.CharField(
        max_length=100,
    )

    description = models.TextField()

    genre = models.CharField(
        max_length=50,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        abstract = True
        ordering = ["-created_at", "title"]


class Book(BaseMedia):
    author = models.CharField(
        max_length=100,
        validators=[
            MinLengthValidator(
                5,
                message="Author must be at least 5 characters long"
            )
        ],
    )

    isbn = models.CharField(
        max_length=20,
        unique=True,
        validators=[
            MinLengthValidator(
                6,
                message="ISBN must be at least 6 characters long"
            )
        ],
    )

    class Meta(BaseMedia.Meta):
        verbose_name = "Model Book"
        verbose_name_plural = "Models of type - Book"


class Movie(BaseMedia):
    director = models.CharField(
        max_length=100,
        validators=[
            MinLengthValidator(
                8,
                message="Director must be at least 8 characters long"
            )
        ],
    )

    class Meta(BaseMedia.Meta):
        verbose_name = "Model Movie"
        verbose_name_plural = "Models of type - Movie"


class Music(BaseMedia):
    artist = models.CharField(
        max_length=100,
        validators=[
            MinLengthValidator(
                9,
                message="Artist must be at least 9 characters long"
            )
        ],
    )

    class Meta(BaseMedia.Meta):
        verbose_name = "Model Music"
        verbose_name_plural = "Models of type - Music"


class Product(models.Model):
    name = models.CharField(
        max_length=100,
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    def calculate_tax(self):
        return self.price * Decimal(0.08)

    @staticmethod
    def calculate_shipping_cost(weight: Decimal):
        return weight * Decimal(2.00)

    def format_product_name(self):
        return f"Product: {self.name}"


class DiscountedProduct(Product):
    class Meta:
        proxy = True

    def calculate_price_without_discount(self):
        return self.price + self.price * Decimal(0.2)

    def calculate_tax(self):
        return self.price * Decimal(0.05)

    @staticmethod
    def calculate_shipping_cost(weight: Decimal):
        return weight * Decimal(1.50)

    def format_product_name(self):
        return f"Discounted Product: {self.name}"


class Hero(models.Model, RechargeEnergyMixin):
    name = models.CharField(
        max_length=100,
    )

    hero_title = models.CharField(
        max_length=100,
    )

    energy = models.PositiveIntegerField()


class SpiderHero(Hero):
    ABILITY_COST = 80

    def swing_from_buildings(self):
        if self.energy < SpiderHero.ABILITY_COST:
            return f"{self.name} as Spider Hero is out of web shooter fluid"
        elif self.energy == SpiderHero.ABILITY_COST:
            self.energy = 1
        else:
            self.energy -= SpiderHero.ABILITY_COST
        self.save()
        return f"{self.name} as Spider Hero swings from buildings using web shooters"

    class Meta:
        proxy = True


class FlashHero(Hero):
    ABILITY_COST = 65

    def run_at_super_speed(self):
        if self.energy < FlashHero.ABILITY_COST:
            return f"{self.name} as Flash Hero needs to recharge the speed force"
        elif self.energy == FlashHero.ABILITY_COST:
            self.energy = 1
        else:
            self.energy -= FlashHero.ABILITY_COST
        self.save()
        return f"{self.name} as Flash Hero runs at lightning speed, saving the day"

    class Meta:
        proxy = True


class Document(models.Model):
    title = models.CharField(
        max_length=200
    )

    content = models.TextField()
    search_vector = SearchVectorField(null=True)

    class Meta:
        indexes = [
            models.Index(fields=["search_vector"])
        ]
