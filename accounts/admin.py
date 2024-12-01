from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    """
    Custom admin for CustomUser model.

    Attributes:
        model (CustomUser): The model being registered with the admin.
        list_display (tuple): Fields to display in the list view.
        list_filter (tuple): Fields to filter by in the list view.
        search_fields (tuple): Fields to search by in the list view.
        ordering (tuple): Default ordering for the list view.
    """
    model: CustomUser = CustomUser
    list_display: tuple = ('username', 'email', 'is_staff', 'is_active',)
    list_filter: tuple = ('is_staff', 'is_active',)
    search_fields: tuple = ('email', 'username',)
    ordering: tuple = ('email',)


admin.site.register(CustomUser, CustomUserAdmin)
