from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from social.models import *


# Register your models here.

class ImagInline(admin.TabularInline):
    model = Image
    extra = 0

@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'job')
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Information', {'fields': ('data_of_brith', 'bio', 'job', 'phone', 'photo')}),
    )

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['author', 'created', 'description']
    ordering = ['created']
    list_filter = ['created']
    inlines = [ImagInline]