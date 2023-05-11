from django.contrib import admin
from users.models import CustomUser


@admin.register(CustomUser)
class AdminUser(admin.ModelAdmin):
    list_display = (
        'pk',
        'username',
        'email',
        'first_name',
        'last_name',
        'password',
        'is_active',
        'last_login',
        'is_staff',
    )
    list_filter = ('email', 'first_name')
    search_fields = ('email', 'first_name')
    list_display_links = ('pk', 'username')
    empty_value_display = '-пусто-'