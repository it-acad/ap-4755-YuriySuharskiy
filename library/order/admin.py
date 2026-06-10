from django.contrib import admin
from .models import Order

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_user_email', 'get_book_name', 'created_at', 'end_at', 'plated_end_at')

    def get_user_email(self, obj):
        return obj.user.email
    get_user_email.short_description = 'User Email'

    def get_book_name(self, obj):
        return obj.book.name
    get_book_name.short_description = 'Book Name'

admin.site.register(Order, OrderAdmin)