from django.contrib import admin
from .models import Job, Application, SavedJob

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'company_name', 'domain', 'location', 'job_type', 'salary_range', 'created_at', 'is_active')
    list_filter = ('is_active', 'job_type', 'domain', 'location')
    search_fields = ('title', 'company_name', 'domain', 'location', 'skills_required')
    list_editable = ('is_active',)
    actions = ['activate_jobs', 'deactivate_jobs']

    def activate_jobs(self, request, queryset):
        queryset.update(is_active=True)
    activate_jobs.short_description = "Activate selected jobs"

    def deactivate_jobs(self, request, queryset):
        queryset.update(is_active=False)
    deactivate_jobs.short_description = "Deactivate selected jobs"


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('user', 'job', 'status', 'applied_at')
    list_filter = ('status', 'applied_at')
    search_fields = ('user__email', 'user__first_name', 'job__title', 'job__company_name')
    list_editable = ('status',)


@admin.register(SavedJob)
class SavedJobAdmin(admin.ModelAdmin):
    list_display = ('user', 'job', 'saved_at')
    search_fields = ('user__email', 'job__title', 'job__company_name')
    list_filter = ('saved_at',)

