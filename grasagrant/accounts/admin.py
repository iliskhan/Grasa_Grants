from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as auth_UserAdmin
from django.contrib.auth.forms import UserChangeForm as auth_UserChangeForm
from .models import User

# Register your models here.


class UserAdmin(auth_UserAdmin):
    form = auth_UserChangeForm
    list_display = ('username', 'email', 'is_staff')

    fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ()}
        ),
        ('Permissions', {
            'fields': ('is_staff','groups', 'user_permissions', 'email', 'username',)}
        )
        
    )

admin.site.register(User, UserAdmin)