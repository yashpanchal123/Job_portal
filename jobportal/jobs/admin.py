from django.contrib import admin
from .models import Job, Profile, JobApplication, SavedJob


# Register the Job model
@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "company",
        "posted_by",
        "created_at",
    )  # Fields to display in the list view
    search_fields = ("title", "company")  # Fields to search in the admin interface


# Register the Profile model
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user",)  # Display the user associated with the profile


@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ("job", "name", "email", "cover_letter")


@admin.register(SavedJob)
class SavedJobAdmin(admin.ModelAdmin):
    list_display = ("user", "job")
