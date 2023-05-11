from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import CustomUser


@admin.register(CustomUser)
class AdminUser(UserAdmin):
    list_display = (
        'pk',
        'username',
        'email',
        'first_name',
        'last_name',
        'is_active',
        'last_login',
        'is_staff',
        'date_joined',
    )
    list_filter = ('email', 'first_name')
    search_fields = ('email', 'first_name')
    list_display_links = ('pk', 'username')
    readonly_fields = ('date_joined',)
    empty_value_display = '-пусто-'