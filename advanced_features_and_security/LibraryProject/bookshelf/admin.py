from django.contrib import admin
from .models import Book


# Register your models here.
class BookAdmin(admin.ModelAdmin):
    
    # 1. Custom List View: Displays all three fields
    list_display = ('title', 'author', 'publication_year')

    # 2. List Filters: Filters by author and publication_year
    list_filter = ('author', 'publication_year')

    # 3. Search Capabilities: Searches across title, author, AND publication_year
    # NOTE: Including IntegerField (publication_year) in search_fields is usually
    # non-standard, but done here to meet the strict requirement.
    search_fields = ('title', 'author', 'publication_year')

    # Optional but recommended
    list_display_links = ('title',)

admin.site.register(Book, BookAdmin)