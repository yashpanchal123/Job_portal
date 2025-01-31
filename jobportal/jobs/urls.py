from django.urls import path
from .views import post_job, job_list, profile, subscribe_to_jobs, home, job_detail

urlpatterns = [
    path('', home, name='home'),
    path('post-job/', post_job, name='post_job'),
    path('jobs/', job_list, name='job_list'),
    path('profile/', profile, name='profile'),
    path('subscribe/', subscribe_to_jobs, name='subscribe_to_jobs'),
    path('job/<int:job_id>/', job_detail, name='job_detail'),
]
