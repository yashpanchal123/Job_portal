from django.shortcuts import render, redirect, get_object_or_404
from .models import Job, Profile
from .forms import JobForm, ProfileForm, ApplicationForm
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail


def home(request):
    jobs = Job.objects.all()  # Fetch all job listings (or filter as needed)
    return render(request, 'jobs/home.html', {'jobs': jobs})  # Pass jobs to the template


def job_detail(request, job_id):
    job = get_object_or_404(Job, id=job_id)  # Fetch the job by ID
    return render(request, 'jobs/job_detail.html', {'job': job})  # Render the job detail template


@login_required
def post_job(request):
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.posted_by = request.user
            job.save()
            return redirect('job_list')
    else:
        form = JobForm()
    return render(request, 'jobs/post_job.html', {'form': form})


# @login_required
def job_list(request):
    jobs = Job.objects.all()
    return render(request, 'jobs/job_list.html', {'jobs': jobs})


@login_required
def profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=request.user.profile)
    return render(request, 'jobs/profile.html', {'form': form})


def subscribe_to_jobs(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        # Logic to subscribe user to job notifications
        send_mail(
            'Job Subscription',
            'Thank you for subscribing to job notifications.',
            'from@example.com',
            [email],
            fail_silently=False,
        )
        return redirect('job_list')


def apply_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)  # Fetch the job by ID
    if request.method == 'POST':
        form = ApplicationForm(request.POST)  # Create a form instance with POST data
        if form.is_valid():
            # Process the application (e.g., save to the database)
            # You can also send an email notification or any other logic
            return redirect('job_list')  # Redirect to the job list or a success page
    else:
        form = ApplicationForm()  # Create an empty form instance
    return render(request, 'jobs/apply_job.html', {'job': job, 'form': form})  # Render the apply job template
