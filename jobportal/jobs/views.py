from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView, DetailView, CreateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.urls import reverse_lazy
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Job, Profile, JobApplication
from .forms import JobForm, ProfileForm, ApplicationForm

# Home view as a class-based ListView
class HomeView(ListView):
    model = Job
    template_name = 'jobs/home.html'
    context_object_name = 'jobs'

# Job detail view
class JobDetailView(DetailView):
    model = Job
    template_name = 'jobs/job_detail.html'
    context_object_name = 'job'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['job'].mandatory_skills_list = context['job'].mandatory_skills.split(",")
        return context

# Posting a job
class PostJobView(LoginRequiredMixin, CreateView):
    model = Job
    form_class = JobForm
    template_name = 'jobs/post_job.html'
    success_url = reverse_lazy('job_list')

    def form_valid(self, form):
        form.instance.posted_by = self.request.user
        return super().form_valid(form)

# Listing all jobs
class JobListView(ListView):
    model = Job
    template_name = 'jobs/job_list.html'
    context_object_name = 'jobs'

# Profile management view
class ProfileView(LoginRequiredMixin, View):
    template_name = 'jobs/profile.html'

    def get(self, request):
        form = ProfileForm(instance=request.user.profile)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
        return render(request, self.template_name, {'form': form})

# Job subscription view
class SubscribeToJobsView(View):
    def post(self, request):
        email = request.POST.get('email')
        send_mail(
            'Job Subscription',
            'Thank you for subscribing to job notifications.',
            'from@example.com',
            [email],
            fail_silently=False,
        )
        return redirect('job_list')

# Job application view
class ApplyJobView(View):
    template_name = 'jobs/apply_job.html'

    def get(self, request, job_id):
        job = get_object_or_404(Job, id=job_id)
        form = ApplicationForm()
        return render(request, self.template_name, {'job': job, 'form': form})

    def post(self, request, job_id):
        job = get_object_or_404(Job, id=job_id)
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            JobApplication.objects.create(
                job=job,
                name=form.cleaned_data['name'],
                email=form.cleaned_data['email'],
                resume=form.cleaned_data['resume'],
                cover_letter=form.cleaned_data['cover_letter']
            )
            return redirect('application_success')
        return render(request, self.template_name, {'job': job, 'form': form})

# Application success view
class ApplicationSuccessView(View):
    template_name = 'jobs/application_success.html'

    def get(self, request):
        return render(request, self.template_name)
