from django.contrib import admin
from .models import Job, Profile


# Register the Job model
@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'posted_by', 'created_at')  # Fields to display in the list view
    search_fields = ('title', 'company')  # Fields to search in the admin interface


# Register the Profile model
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user',)  # Display the user associated with the profile
