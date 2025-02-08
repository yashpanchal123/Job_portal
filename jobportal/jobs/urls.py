from django.urls import path
from .views import (
    HomeView, PostJobView, JobListView, ProfileView,
    SubscribeToJobsView, JobDetailView, ApplyJobView,
    ApplicationSuccessView
)

urlpatterns = [
    path('', HomeView.as_view(), name='home'),  # Home Page
    path('post-job/', PostJobView.as_view(), name='post_job'),  # To add new job
    path('jobs/', JobListView.as_view(), name='job_list'),  # Getting all jobs
    path('profile/', ProfileView.as_view(), name='profile'),
    path('subscribe/', SubscribeToJobsView.as_view(), name='subscribe_to_jobs'),  # Subscribing user to job search
    path('job/<int:pk>/', JobDetailView.as_view(), name='job_detail'),  # Using <int:pk> for DetailView compatibility
    path('job/<int:job_id>/apply/', ApplyJobView.as_view(), name='apply_job'),  # Apply for a job
    path('application-success/', ApplicationSuccessView.as_view(), name='application_success'),  # Application success page
]
