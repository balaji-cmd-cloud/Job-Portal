from django import forms
from .models import Job

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = [
            'title', 'company_name', 'domain', 'location', 
            'description', 'skills_required', 'salary_range', 
            'job_type', 'experience_required'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Senior Software Engineer'}),
            'company_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Acme Corporation'}),
            'domain': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. IT, Finance, Marketing'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Bangalore, Remote'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 6, 'placeholder': 'Provide detailed job responsibilities and overview...'}),
            'skills_required': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Python, Django, React, SQL'}),
            'salary_range': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. ₹12L - ₹18L or $90,000 - $120,000'}),
            'job_type': forms.Select(attrs={'class': 'form-select'}),
            'experience_required': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'placeholder': 'e.g. 3'}),
        }
