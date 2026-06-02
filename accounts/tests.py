from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

# Python 3.14 compatibility workaround for Context copying in Django tests
import django.test.client
def safe_copy(x):
    from django.template.context import Context
    if isinstance(x, Context):
        from django.template import Context
        new_ctx = Context()
        new_ctx.dicts = [d.copy() for d in x.dicts]
        return new_ctx
    from copy import copy
    return copy(x)
django.test.client.copy = safe_copy

User = get_user_model()

class UserAuthTests(TestCase):
    def test_create_user_with_email(self):
        user = User.objects.create_user(
            email='candidate@example.com',
            password='Password123!',
            first_name='Candidate',
            last_name='User',
            is_candidate=True
        )
        self.assertEqual(user.email, 'candidate@example.com')
        self.assertEqual(user.username, 'candidate@example.com')
        self.assertTrue(user.is_candidate)
        self.assertFalse(user.is_employer)
        self.assertTrue(user.check_password('Password123!'))

    def test_create_superuser(self):
        user = User.objects.create_superuser(
            email='admin@example.com',
            password='Password123!'
        )
        self.assertEqual(user.email, 'admin@example.com')
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

    def test_registration_view(self):
        # Test registration with mismatching passwords
        response = self.client.post(reverse('register'), {
            'email': 'newuser@example.com',
            'first_name': 'New',
            'last_name': 'User',
            'password': 'Password123!',
            'confirm_password': 'Password1234!',
            'is_candidate': True
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(email='newuser@example.com').exists())

        # Test registration with matching passwords
        response = self.client.post(reverse('register'), {
            'email': 'newuser@example.com',
            'first_name': 'New',
            'last_name': 'User',
            'password': 'Password123!',
            'confirm_password': 'Password123!',
            'is_candidate': True
        })
        self.assertEqual(response.status_code, 302) # Redirect to login
        self.assertTrue(User.objects.filter(email='newuser@example.com').exists())

    def test_login_view(self):
        # Create user
        User.objects.create_user(
            email='loginuser@example.com',
            password='Password123!'
        )
        
        # Test wrong password
        response = self.client.post(reverse('login'), {
            'email': 'loginuser@example.com',
            'password': 'WrongPassword1!'
        })
        self.assertEqual(response.status_code, 200)
        
        # Test correct login
        response = self.client.post(reverse('login'), {
            'email': 'loginuser@example.com',
            'password': 'Password123!'
        })
        self.assertEqual(response.status_code, 302) # Redirects to dashboard

    def test_profile_form_resume_validation(self):
        from .forms import UserProfileForm
        from django.core.files.uploadedfile import SimpleUploadedFile

        # Valid resume (PDF)
        pdf_file = SimpleUploadedFile("resume.pdf", b"dummy pdf content", content_type="application/pdf")
        form = UserProfileForm(
            data={'first_name': 'Test', 'last_name': 'Candidate', 'experience_years': 0},
            files={'resume_file': pdf_file}
        )
        self.assertTrue(form.is_valid())

        # Invalid resume (TXT)
        txt_file = SimpleUploadedFile("resume.txt", b"dummy txt content", content_type="text/plain")
        form = UserProfileForm(
            data={'first_name': 'Test', 'last_name': 'Candidate', 'experience_years': 0},
            files={'resume_file': txt_file}
        )
        self.assertFalse(form.is_valid())
        self.assertIn('resume_file', form.errors)


