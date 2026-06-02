from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
import re

User = get_user_model()

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Create Password'}), label="Password")
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}), label="Confirm Password")
    
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'is_candidate', 'is_employer']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'name@example.com'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'is_candidate': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_employer': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("A user with this email address already exists.")
        return email

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 8:
            raise forms.ValidationError("Password must be at least 8 characters long.")
        if not re.search(r"[A-Z]", password):
            raise forms.ValidationError("Password must contain at least one uppercase letter.")
        if not re.search(r"[0-9]", password):
            raise forms.ValidationError("Password must contain at least one digit.")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            raise forms.ValidationError("Password must contain at least one special character.")
        return password

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match.")
        
        is_candidate = cleaned_data.get('is_candidate')
        is_employer = cleaned_data.get('is_employer')
        
        if not is_candidate and not is_employer:
            self.add_error('is_candidate', "You must register as either a Candidate or an Employer.")
            
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = user.email
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'name@example.com'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'skills', 'domain', 'location', 'experience_years', 'resume_summary', 'profile_picture', 'resume_file']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'skills': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Python, Django, React, SQL'}),
            'domain': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. IT, Finance, Marketing'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Bangalore, Remote'}),
            'experience_years': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'resume_summary': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Brief description of your background, experience and education...'}),
            'profile_picture': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'resume_file': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    def clean_resume_file(self):
        resume = self.cleaned_data.get('resume_file')
        if resume:
            import os
            ext = os.path.splitext(resume.name)[1].lower()
            valid_extensions = ['.pdf', '.doc', '.docx']
            if ext not in valid_extensions:
                raise forms.ValidationError("Unsupported file format. Please upload a PDF, DOC, or DOCX document.")
            if resume.size > 5 * 1024 * 1024:
                raise forms.ValidationError("File size exceeds the 5MB limit.")
        return resume

