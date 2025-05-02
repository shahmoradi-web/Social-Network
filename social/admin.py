from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from social.models import User


# Register your models here.

@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'job')
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Information', {'fields': ('data_of_brith', 'bio', 'job', 'phone', 'photo')}),
    )