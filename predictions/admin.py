from django.contrib import admin
from .models import *
from django.utils.html import format_html
from .models import Profile  # Import the Profile model
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'display_logo')
    list_filter = ('tournament',)
    def display_logo(self, obj):
        if obj.logo:
            return format_html('<img src="{}" width="50" height="50" />', obj.logo.url)
        else:
            return "No Logo"

    display_logo.short_description = 'Logo'

admin.site.register(Team, TeamAdmin)
admin.site.register(Tournament)
admin.site.register(Match)
admin.site.register(Prediction)
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'facebook_username']
