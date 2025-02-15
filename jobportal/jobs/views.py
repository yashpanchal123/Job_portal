from django.http import JsonResponse
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView, DetailView, CreateView, View
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.core.mail import send_mail
from django.urls import reverse_lazy
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Job, Profile, JobApplication, SavedJob
from .forms import JobForm, ProfileForm, ApplicationForm, SignUpForm
from django.views.generic.edit import FormView
from django.contrib.auth.decorators import login_required

# User Signup View
class SignupView(FormView):
    template_name = "jobs/signup.html"
    form_class = SignUpForm
    success_url = reverse_lazy("job_list")  # Redirect after successful signup

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)  # Automatically log in the user
        return super().form_valid(form)


# User Login View
class UserLoginView(LoginView):
    template_name = "jobs/login.html"
    authentication_form = AuthenticationForm

    def form_invalid(self, form):
        messages.error(self.request, "Invalid username or password. Please try again.")
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse_lazy("home")


# User Logout View
class UserLogoutView(LogoutView):
    next_page = reverse_lazy("login")


# Home view with authentication required
class HomeView(LoginRequiredMixin, ListView):
    model = Job
    template_name = "jobs/home.html"
    context_object_name = "jobs"


# Job detail view
class JobDetailView(LoginRequiredMixin, DetailView):
    model = Job
    template_name = "jobs/job_detail.html"
    context_object_name = "job"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["job"].mandatory_skills_list = context["job"].mandatory_skills.split(
            ","
        )
        return context


# Posting a job
class PostJobView(LoginRequiredMixin, CreateView):
    model = Job
    form_class = JobForm
    template_name = "jobs/post_job.html"
    success_url = reverse_lazy("job_list")

    def form_valid(self, form):
        form.instance.posted_by = self.request.user
        return super().form_valid(form)


# Listing all jobs
class JobListView(LoginRequiredMixin, ListView):
    model = Job
    template_name = "jobs/job_list.html"
    context_object_name = "jobs"

    def get_queryset(self):
        queryset = Job.objects.all()
        title_query = self.request.GET.get("title", "").strip()
        location_query = self.request.GET.get("Location", "").strip()

        if title_query:
            queryset = queryset.filter(title__icontains=title_query)
        if location_query:
            queryset = queryset.filter(location__icontains=location_query)

        return queryset


# Profile management view
class ProfileView(LoginRequiredMixin, View):
    template_name = "jobs/profile.html"

    def get(self, request):
        form = ProfileForm(instance=request.user.profile)
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect("profile")
        return render(request, self.template_name, {"form": form})


# Job subscription view
class SubscribeToJobsView(LoginRequiredMixin, View):
    def post(self, request):
        email = request.POST.get("email")
        send_mail(
            "Job Subscription",
            "Thank you for subscribing to job notifications.",
            "from@example.com",
            [email],
            fail_silently=False,
        )
        return redirect("job_list")


# Job application view
class ApplyJobView(LoginRequiredMixin, View):
    template_name = "jobs/apply_job.html"

    def get(self, request, job_id):
        job = get_object_or_404(Job, id=job_id)
        form = ApplicationForm()
        return render(request, self.template_name, {"job": job, "form": form})

    def post(self, request, job_id):
        job = get_object_or_404(Job, id=job_id)
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            JobApplication.objects.create(
                job=job,
                user=request.user,
                name=form.cleaned_data["name"],
                email=form.cleaned_data["email"],
                resume=form.cleaned_data["resume"],
                cover_letter=form.cleaned_data["cover_letter"],
            )
            return redirect("application_success")
        return render(request, self.template_name, {"job": job, "form": form})


class AppliedJobsListView(LoginRequiredMixin, View):
    template_name = "jobs/applied_jobs.html"

    def get(self, request):
        applied_jobs = JobApplication.objects.filter(user=request.user)
        return render(request, self.template_name, {"applied_jobs": applied_jobs})


# Application success view
class ApplicationSuccessView(LoginRequiredMixin, View):
    template_name = "jobs/application_success.html"

    def get(self, request):
        return render(request, self.template_name)


class SaveJobView(LoginRequiredMixin, View):
    def post(self, request, job_id):
        if not request.user.is_authenticated:
            return JsonResponse({"error": "User not authenticated"}, status=401)

        job = get_object_or_404(Job, id=job_id)

        # Toggle save/unsave logic
        saved_job, created = SavedJob.objects.get_or_create(user=request.user, job=job)
        if not created:
            saved_job.delete()
            return JsonResponse(
                {"saved": False, "message": "Job removed from saved jobs."}
            )

        return JsonResponse({"saved": True, "message": "Job saved successfully."})


class SavedJobsListView(LoginRequiredMixin, View):
    template_name = "jobs/saved_jobs_list.html"

    def get(self, request):
        saved_jobs = SavedJob.objects.filter(user=request.user)
        return render(request, self.template_name, {"saved_jobs": saved_jobs})

class UserSettingsView(LoginRequiredMixin, View):
    template_name = "jobs/settings.html"

    def get(self, request):
        return render(request, self.template_name, {"user": request.user})
