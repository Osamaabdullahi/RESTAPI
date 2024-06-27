import django_filters
from .models import Product

CATEGORY_CHOICES = [
        ('Laptops', 'Laptops'),
        ('Headphones', 'Headphones'),
        ('Tablets', 'Tablets'),
        ('Networking', 'Networking'),
        ('PC Gaming', 'PC Gaming'),
    ]

class ProductFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')
    category = django_filters.ChoiceFilter(field_name='category', choices=CATEGORY_CHOICES)

    class Meta:
        model = Product
        fields = ['name', 'category']
