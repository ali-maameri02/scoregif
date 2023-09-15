from django.contrib import admin
from django.utils.html import format_html
from django.core.exceptions import ValidationError
from .models import *
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'display_logo')
    list_filter = ('tournament',)

    def display_logo(self, obj):
        if obj.logo:
            return format_html('<img src="{}" width="50" height="50" />', obj.logo.url)
        else:
            return "No Logo"

    display_logo.short_description = 'Logo'

    def save_model(self, request, obj, form, change):
        if not change:  # Only perform the check when adding a new team
            # Check if a team with the same name already exists
            existing_team = Team.objects.filter(name=obj.name).first()

            if existing_team:
                # If it exists, raise a validation error and display a message
                raise ValidationError('Team with this name already exists.')

        super().save_model(request, obj, form, change)



admin.site.register(Team, TeamAdmin)
admin.site.register(Tournament)
admin.site.register(Match)
admin.site.register(Prediction)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'facebook_username']
