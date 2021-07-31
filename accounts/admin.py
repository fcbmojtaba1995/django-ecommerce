from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserCreationForm, UserChangeForm
from .models import User, VerifyCode


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('username', 'phone', 'email', 'date_joined', 'is_active', 'is_admin')
    list_filter = ('is_admin', 'is_active', 'date_joined', 'last_login')
    search_fields = ('username', 'phone', 'email')
    ordering = ('is_admin', 'is_active', 'date_joined', 'last_login')
    filter_horizontal = ()

    fieldsets = (
        ('Main', {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('phone', 'first_name', 'last_name', 'email', 'national_code', 'date_of_birth')}),
        ('Permissions', {'fields': ('is_admin', 'is_active')}),
        ('Other', {'fields': ('is_verified', 'is_set_password')})
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2'),
        }),
    )


admin.site.register(User, UserAdmin)
admin.site.unregister(Group)

admin.site.register(VerifyCode)
