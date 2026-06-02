from django.urls import path
from . import views
from . import api_views

urlpatterns = [
    # Template views
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('search/', views.job_list_view, name='job_list'),
    path('job/<int:pk>/', views.job_detail_view, name='job_detail'),
    path('job/<int:pk>/apply/', views.apply_job_view, name='apply_job'),
    path('job/<int:pk>/save/', views.save_job_view, name='save_job'),
    path('applications/', views.my_applications_view, name='my_applications'),
    path('saved/', views.saved_jobs_view, name='saved_jobs'),
    path('preferences/', views.resume_preferences_view, name='resume_preferences'),
    path('prep/', views.prep_landing_view, name='prep_landing'),
    path('prep/quiz/<str:domain>/', views.prep_quiz_view, name='prep_quiz'),

    # Employer management routes
    path('employer/', views.employer_dashboard_view, name='employer_dashboard'),
    path('employer/post/', views.create_job_view, name='create_job'),
    path('employer/edit/<int:pk>/', views.edit_job_view, name='edit_job'),
    path('employer/toggle/<int:pk>/', views.toggle_job_status_view, name='toggle_job_status'),
    path('employer/applicants/<int:pk>/', views.manage_applicants_view, name='manage_applicants'),

    # REST API views
    path('api/', api_views.JobListAPIView.as_view(), name='api_job_list'),
    path('api/<int:pk>/', api_views.JobDetailAPIView.as_view(), name='api_job_detail'),
    path('api/<int:pk>/apply/', api_views.JobApplyAPIView.as_view(), name='api_job_apply'),
    path('api/<int:pk>/save/', api_views.JobSaveAPIView.as_view(), name='api_job_save'),
    path('api/recommendations/', api_views.RecommendationsAPIView.as_view(), name='api_recommendations'),
    path('api/trending-skills/', api_views.TrendingSkillsAPIView.as_view(), name='api_trending_skills'),
]
