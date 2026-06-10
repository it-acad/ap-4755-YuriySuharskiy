from django.contrib import admin
from .models import Book

class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'count', 'description')
    list_filter = ('name', 'authors')
    search_fields = ('id', 'name')

    # Групуємо інформацію на дві окремі візуальні секції
    fieldsets = (
        ('Статичні дані (Не змінюються)', {
            'fields': ('name', 'authors', 'description')
        }),
        ('Динамічні дані (Змінюються)', {
            'fields': ('count',),
        }),
    )
    
    filter_horizontal = ('authors',)

admin.site.register(Book, BookAdmin)