from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

class UserAdmin(BaseUserAdmin):
    ordering = ['id']
    list_display = ['email', 'first_name', 'last_name', 'is_staff']
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Información personal', {'fields': ('first_name', 'last_name')}),
        ('Permisos', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('Fechas importantes', {'fields': ('last_login', 'date_joined')}),
    )
    
    readonly_fields = ['last_login', 'date_joined']

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email', 'first_name', 'last_name', 'password1', 'password2', 
                'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'
            ),
        }),
    )

admin.site.register(User, UserAdmin)