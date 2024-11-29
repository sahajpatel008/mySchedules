from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

# Register your models here.

class CustomUserAdmin(UserAdmin):
    model = User
    # Display 'username', 'email', and 'role' in the list view
    list_display = ('username', 'email', 'role', 'is_active', 'is_staff')

    # Modify the 'fieldsets' to include custom fields without duplicating
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Fields', {'fields': ('role',)}),  # Only add 'role' here, since 'email' is already part of the default fieldsets
    )

    # Modify the 'add_fieldsets' for the user creation form
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'role'),
        }),
    ) + UserAdmin.add_fieldsets  # Include the default add fieldsets at the end

# Register the custom UserAdmin
admin.site.register(User, CustomUserAdmin)