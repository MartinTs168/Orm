from datetime import date

from django.db import models


class Employee(models.Model):
    name = models.CharField(max_length=30)
    email_address = models.EmailField()
    photo = models.URLField()
    birth_date = models.DateField()
    works_full_time = models.BooleanField()
    created_on = models.DateTimeField(auto_now_add=True)


class Department(models.Model):
    class CityChoices(models.TextChoices):
        Sofia = 'Sf', 'Sofia'
        Plovdiv = 'Pd', 'Plovdiv'
        Varna = 'Vr', 'Varna'
        Burgas = 'Bs', 'Burgas'

    code = models.CharField(max_length=4, primary_key=True, unique=True)
    name = models.CharField(max_length=50, unique=True)
    employees_count = models.PositiveSmallIntegerField(default=1, verbose_name='Employees Count')
    location = models.CharField(max_length=20, null=True, choices=CityChoices)
    last_edited_on = models.DateTimeField(auto_now=True)
    # when we have auto_now or auto_now_add set to True editable will be False


class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True)
    budget = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    duration_in_days = models.PositiveSmallIntegerField(null=True, verbose_name="Duration in Days")
    estimated_hours = models.FloatField(null=True, verbose_name="Estimated Hours")
    start_date = models.DateField(verbose_name="Start Date", null=True, default=date.today)
    created_on = models.DateTimeField(auto_now_add=True)
    last_edited_on = models.DateTimeField(auto_now=True)
