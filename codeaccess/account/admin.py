from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import User


class UserAdmin(BaseUserAdmin):
    """register .."""

    # form = UpdateUserForm
    # add_form = AddUserForm

    list_display = ('username', 'email', 'mobile', 'is_staff')
    list_filter = ('is_staff', )
    search_fields = ('email','mobile')
    fieldsets = (
        (None, {'fields': ('username', 'email', 'mobile', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_staff')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2'),
        }),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


admin.site.register(User, UserAdmin)