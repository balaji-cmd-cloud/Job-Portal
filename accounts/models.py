from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        # Ensure username defaults to email to avoid blank username issues
        extra_fields.setdefault('username', email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    email = models.EmailField(unique=True)
    is_candidate = models.BooleanField(default=True)
    is_employer = models.BooleanField(default=False)
    skills = models.TextField(blank=True, help_text="Comma-separated skills (e.g. Python, Django, React)")
    domain = models.CharField(max_length=100, blank=True, help_text="Primary domain (e.g. IT, Finance, HR)")
    location = models.CharField(max_length=100, blank=True, help_text="Current location (e.g. Bangalore, Mumbai)")
    experience_years = models.IntegerField(default=0, help_text="Years of professional experience")
    resume_summary = models.TextField(blank=True, help_text="Brief professional summary/resume detail")
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    resume_file = models.FileField(upload_to='resumes/', blank=True, null=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def get_skills_list(self):
        if not self.skills:
            return []
        return [s.strip() for s in self.skills.split(',') if s.strip()]

