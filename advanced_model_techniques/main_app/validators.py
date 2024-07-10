from django.core.exceptions import ValidationError


def validate_menu_categories(value):
    value = value.lower()
    if "appetizers" not in value or "main course" not in value or "desserts" not in value:
        raise ValidationError('The menu must include each of '
                              'the categories "Appetizers", "Main Course", "Desserts".')