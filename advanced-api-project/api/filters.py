import django_filters
from .models import Book

class BookFilter(django_filters.FilterSet):
    """
    Defines filters for the Book model.
    """
    # Enables partial matching filter for the title field
    title = django_filters.CharFilter(lookup_expr='icontains')
    
    # Enables exact or partial matching filter for the author field
    author = django_filters.CharFilter(lookup_expr='icontains')
    
    # Enables range filtering for publication_year (e.g., ?publication_year__gt=2000)
    publication_year = django_filters.NumberFilter(lookup_expr='exact')
    
    # Example for advanced range filtering:
    publication_year_gte = django_filters.NumberFilter(field_name='publication_year', lookup_expr='gte')
    publication_year_lte = django_filters.NumberFilter(field_name='publication_year', lookup_expr='lte')

    class Meta:
        model = Book
        fields = ['title', 'author', 'publication_year']