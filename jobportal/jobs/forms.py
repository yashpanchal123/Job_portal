from django import forms
from .models import Job, Profile


class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'company', 'description', 'job_type', 'location', 'salary', 'experience', 'education',
                  'mandatory_skills']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'company': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'job_type': forms.Select(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'salary': forms.NumberInput(attrs={'class': 'form-control'}),
            'experience': forms.TextInput(attrs={'class': 'form-control'}),
            'education': forms.TextInput(attrs={'class': 'form-control'}),
            'mandatory_skills': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['resume']


class ApplicationForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    resume = forms.FileField()  # Assuming you want to upload a resume
    cover_letter = forms.CharField(widget=forms.Textarea, required=False)  # Optional cover letter
