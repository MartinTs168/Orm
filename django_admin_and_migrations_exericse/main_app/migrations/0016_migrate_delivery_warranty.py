# Generated by Django 5.0.4 on 2024-06-26 12:29

from django.db import migrations
from django.utils import timezone


def set_fields_deliver_warranty(apps, schema_editor):
    order_model = apps.get_model('main_app', 'Order')
    orders = order_model.objects.all()

    for order in orders:
        if order.status == 'Pending':
            order.delivery = order.order_date + timezone.timedelta(days=3)
        elif order.status == 'Completed':
            order.warranty = '24 months'
        else:
            order.delete()

    order_model.objects.bulk_update(orders, ['delivery', 'warranty'])


def reverse_delivery_warranty(apps, schema_field):
    order_model = apps.get_model('main_app', 'Order')
    orders = order_model.objects.all()

    for order in orders:
        if order.status == 'Pending':
            order.delivery = None
        elif order.status == 'Completed':
            order.warranty = order_model._meta.get_field('warranty').default

    order_model.objects.bulk_update(orders, ['delivery', 'warranty'])


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0015_order'),
    ]

    operations = [
        migrations.RunPython(set_fields_deliver_warranty, reverse_delivery_warranty),
    ]
