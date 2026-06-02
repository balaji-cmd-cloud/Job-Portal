from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ['email', 'first_name', 'last_name', 'is_candidate', 'is_employer', 'is_staff']
    list_filter = ['is_candidate', 'is_employer', 'is_staff', 'is_superuser']
    fieldsets = UserAdmin.fieldsets + (
        ('Apna Info', {'fields': ('is_candidate', 'is_employer', 'skills', 'domain', 'location', 'experience_years', 'resume_summary', 'profile_picture')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Apna Info', {'fields': ('is_candidate', 'is_employer', 'skills', 'domain', 'location', 'experience_years', 'resume_summary', 'profile_picture')}),
    )
    ordering = ('email',)

admin.site.register(User, CustomUserAdmin)

