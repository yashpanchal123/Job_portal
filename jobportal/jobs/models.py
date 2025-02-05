from django.db import models
from django.contrib.auth.models import User


class Job(models.Model):
    JOB_TYPE_CHOICES = [
        ('full_time', 'Full Time'),
        ('part_time', 'Part Time'),
        ('contract', 'Contract'),
        ('internship', 'Internship'),
    ]

    title = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()
    job_type = models.CharField(max_length=50, choices=JOB_TYPE_CHOICES)
    location = models.CharField(max_length=255)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    experience = models.CharField(max_length=100)  # e.g., "2-3 years"
    education = models.CharField(max_length=100)  # e.g., "Bachelor's Degree"
    mandatory_skills = models.TextField()  # Comma-separated skills
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} at {self.company}"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    resume = models.FileField(upload_to='resumes/', blank=True)

    def __str__(self):
        return self.user.username


class JobApplication(models.Model):
    job = models.ForeignKey('Job', on_delete=models.CASCADE)  # Link to the job
    name = models.CharField(max_length=100)
    email = models.EmailField()
    resume = models.FileField(upload_to='resumes/')  # Path where resumes are stored
    cover_letter = models.TextField(blank=True, null=True)  # Optional cover letter
    submitted_at = models.DateTimeField(auto_now_add=True)  # Timestamp of submission
