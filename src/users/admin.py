from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class MyUserAdmin(UserAdmin):
    fieldsets = (
        (
            "personal info",
            {"fields": ("username", "email", "password", "is_manager", "is_staff")},
        ),
    )

    add_fieldsets = (
        (
            None,
            {"fields": ("username", "email", "password1", "password2", "is_manager")},
        ),
    )

    list_display = (
        "id",
        "username",
        "email",
        "is_manager",
    )
