from django import forms
from .models import Job, Profile


class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'description', 'company', 'job_type', 'location', 'salary', 'experience', 'education',
                  'mandatory_skills',]


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['resume']
