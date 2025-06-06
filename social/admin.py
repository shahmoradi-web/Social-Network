from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.core.mail import send_mail

from social.models import *


# Register your models here.

def make_deactivate(modeladmin, request, queryset):
    results = queryset.update(active=False)
    modeladmin.message_user(request, f'{results} accounts has been deactivated.')


def make_activate(modeladmin, request, queryset):
    results = queryset.update(active=True)
    modeladmin.message_user(request, f'{results} accounts has been activated.')

def send_post_status(modeladmin, request, queryset):

    for obj in queryset:
        if obj.active:
            send_mail('notification for your post', 'your post is active', 'shahmoradinrges@gmail.com',
                      [obj.author.email], fail_silently=False)
        elif not obj.active:
            send_mail('notification for your post', 'your post is deactivate', 'shahmoradinrges@gmail.com',
                      [obj.author.email], fail_silently=False)
    modeladmin.message_user(request, 'Send post status')


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
    actions = [make_deactivate, make_activate]

