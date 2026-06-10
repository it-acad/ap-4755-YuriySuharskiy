from django.contrib import admin
from .models import Author

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'surname')

    fieldsets = (
        ('Персональні дані автора', {
            'fields': ('name', 'surname', 'patronymic')
        }),
    )

admin.site.register(Author, AuthorAdmin)