from django.contrib import admin
from .models import Book


# Register your models here.
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_date')
    search_fields = ('title', 'author')
    list_filter = ('author', 'publication_date')
    # Optional: Set the fields that appear as links to the change page
    list_display_links = ('title', 'author')

admin.site.register(Book, BookAdmin)