import os
import django
from django.db.models import Q, Count, F, Case, When, Value, BooleanField

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Profile, Product, Order


# Create queries within functions


def get_profiles(search_string=None) -> str:
    if search_string is None:
        return ""

    query = Q(full_name__icontains=search_string) | Q(email__icontains=search_string) | Q(
        phone_number__icontains=search_string
    )

    profiles = Profile.objects.filter(query).order_by('full_name')

    if not profiles.exists():
        return ""

    result = []
    for p in profiles:
        result.append(f"Profile: {p.full_name}, email: {p.email}, "
                      f"phone number: {p.phone_number}, orders: {p.orders.count()}")

    return '\n'.join(result)


def get_loyal_profiles() -> str:
    profiles = Profile.objects.get_regular_customers()

    if not profiles:
        return ""

    result = []
    for p in profiles:
        result.append(f"Profile: {p.full_name}, orders: {p.orders.count()}")

    return '\n'.join(result)


def get_last_sold_products() -> str:
    order = Order.objects.prefetch_related('products').last()

    if order is None or not order.products.exists():
        return ""

    products = ', '.join(order.products.order_by('name').values_list('name', flat=True))

    return f"Last sold products: {products}"


def get_top_products() -> str:
    top_sold_products = (
        Product.objects.annotate(total_sold=Count('orders'))
        .filter(total_sold__gt=0).order_by('-total_sold', 'name')[:5]
    )

    if not top_sold_products:
        return ""

    result = ["Top products:"]

    for pr in top_sold_products:
        result.append(f"{pr.name}, sold {pr.total_sold} times")

    return '\n'.join(result)


def apply_discounts() -> str:
    orders = Order.objects.annotate(products_count=Count('products')).filter(
        products_count__gt=2,
        is_completed=False
    )

    orders.update(total_price=F('total_price') * 0.9)

    return f"Discount applied to {orders.count()} orders."


def complete_order() -> str:
    order = Order.objects.filter(is_completed=False).order_by('creation_date').first()

    if not order:
        return ""

    order.products.update(
        in_stock=F('in_stock') - 1,
        is_available=Case(
            When(in_stock=1, then=Value(False)),
            default=F('is_available'),
            output_field=BooleanField()
        )
    )

    order.is_completed = True
    order.save()

    return "Order has been completed!"


