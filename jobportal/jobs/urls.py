from django.urls import path
from .views import post_job, job_list, profile, subscribe_to_jobs, home, job_detail, apply_job, application_success

urlpatterns = [
    path('', home, name='home'),  # Home Page
    path('post-job/', post_job, name='post_job'),  # To add new job
    path('jobs/', job_list, name='job_list'),  # getting all jobs
    path('profile/', profile, name='profile'),
    path('subscribe/', subscribe_to_jobs, name='subscribe_to_jobs'),  # subscribing user to required job search
    path('job/<int:job_id>/', job_detail, name='job_detail'),  # for getting particular job with job id
    path('job/<int:job_id>/apply/', apply_job, name='apply_job'),  # Apply for a job
    path('application-success/', application_success, name='application_success'),  # Application success page
]
