from django.db import models
from django.conf import settings

class Job(models.Model):
    JOB_TYPES = [
        ('Full-Time', 'Full-Time'),
        ('Part-Time', 'Part-Time'),
        ('Contract', 'Contract'),
        ('Internship', 'Internship'),
        ('Remote', 'Remote'),
    ]

    title = models.CharField(max_length=200)
    company_name = models.CharField(max_length=200)
    domain = models.CharField(max_length=100, help_text="e.g. IT, Finance, HR, Marketing")
    location = models.CharField(max_length=150)
    description = models.TextField()
    skills_required = models.TextField(help_text="Comma-separated skills (e.g. Python, Django, SQL)")
    salary_range = models.CharField(max_length=100, help_text="e.g. $80,000 - $100,000 or ₹10L - ₹15L")
    job_type = models.CharField(max_length=50, choices=JOB_TYPES, default='Full-Time')
    experience_required = models.IntegerField(default=0, help_text="Minimum experience required in years")
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    posted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='posted_jobs', null=True, blank=True)

    def __str__(self):
        return f"{self.title} at {self.company_name}"

    def get_skills_list(self):
        if not self.skills_required:
            return []
        return [s.strip() for s in self.skills_required.split(',') if s.strip()]


class Application(models.Model):
    STATUS_CHOICES = [
        ('Applied', 'Applied'),
        ('Shortlisted', 'Shortlisted'),
        ('Interviewing', 'Interviewing'),
        ('Offered', 'Offered'),
        ('Rejected', 'Rejected'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='applications')
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    applied_at = models.DateTimeField(auto_now_add=True)
    cover_letter = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Applied')

    class Meta:
        unique_together = ('user', 'job')
        ordering = ['-applied_at']

    def __str__(self):
        return f"{self.user.email} applied for {self.job}"


class SavedJob(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='saved_jobs')
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='saved_by_users')
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'job')
        ordering = ['-saved_at']

    def __str__(self):
        return f"{self.user.email} saved {self.job.title}"

