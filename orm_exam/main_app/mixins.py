from django.db import models


class UpdatedAtMixin(models.Model):
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class LaunchDateMixin(models.Model):
    launch_date = models.DateField()

    class Meta:
        abstract = True

