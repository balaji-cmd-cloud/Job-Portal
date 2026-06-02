from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from .models import Job, Application, SavedJob
from .recommender import get_recommendations_for_user, get_trending_skills

User = get_user_model()

class JobRecommendationTests(TestCase):
    def setUp(self):
        # Create mock jobs
        self.job1 = Job.objects.create(
            title='Python Backend Dev',
            company_name='TestCorp',
            domain='IT',
            location='Bangalore',
            skills_required='Python, Django, SQL',
            salary_range='10L - 15L',
            experience_required=2
        )
        self.job2 = Job.objects.create(
            title='React Frontend Dev',
            company_name='FrontendSoft',
            domain='IT',
            location='Remote',
            skills_required='JavaScript, React, CSS',
            salary_range='8L - 12L',
            experience_required=1
        )
        self.job3 = Job.objects.create(
            title='Financial Advisor',
            company_name='MoneyTrust',
            domain='Finance',
            location='Mumbai',
            skills_required='Excel, Finance, Modeling',
            salary_range='12L - 18L',
            experience_required=3
        )

        from django.core.files.uploadedfile import SimpleUploadedFile
        # Create candidate user
        self.user = User.objects.create_user(
            email='testcandidate@example.com',
            password='Password123!',
            is_candidate=True,
            skills='Python, Django',
            domain='IT',
            location='Bangalore',
            experience_years=3,
            resume_file=SimpleUploadedFile("resume.pdf", b"dummy pdf content", content_type="application/pdf")
        )

    def test_skills_matching_recommender(self):
        recommended = get_recommendations_for_user(self.user, limit=5)
        # job1 should rank first since domain is IT, location matches Bangalore, experience matches, and skills overlap
        self.assertEqual(recommended[0], self.job1)
        # job2 is second as it has same domain (IT) but different location and no matching skills
        self.assertEqual(recommended[1], self.job2)

    def test_trending_skills_extraction(self):
        skills = get_trending_skills()
        self.assertIn('Python', skills)
        self.assertIn('Django', skills)
        self.assertIn('Excel', skills)

    def test_job_apply_api(self):
        self.client.force_login(self.user)
        url = reverse('api_job_apply', kwargs={'pk': self.job1.id})
        
        # Test valid apply
        response = self.client.post(url, {'cover_letter': 'Excited to apply'}, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Application.objects.filter(user=self.user, job=self.job1).exists())
        
        # Test duplicate apply
        response = self.client.post(url, {'cover_letter': 'Excited again'}, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_job_save_api(self):
        self.client.force_login(self.user)
        url = reverse('api_job_save', kwargs={'pk': self.job1.id})
        
        # Test save
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(SavedJob.objects.filter(user=self.user, job=self.job1).exists())
        
        # Test unsave (toggle toggle)
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(SavedJob.objects.filter(user=self.user, job=self.job1).exists())

    def test_employer_dashboard_and_job_crud(self):
        # Create employer user
        employer = User.objects.create_user(
            email='employer@example.com',
            password='Password123!',
            is_employer=True
        )
        self.client.force_login(employer)
        
        # Post new job
        response = self.client.post(reverse('create_job'), {
            'title': 'New Dev Role',
            'company_name': 'EmployerCorp',
            'domain': 'IT',
            'location': 'Bangalore',
            'skills_required': 'Python',
            'salary_range': '5L - 10L',
            'job_type': 'Full-Time',
            'experience_required': 1,
            'description': 'Description text'
        })
        self.assertEqual(response.status_code, 302) # Redirect to dashboard
        self.assertTrue(Job.objects.filter(title='New Dev Role', posted_by=employer).exists())
        
        new_job = Job.objects.get(title='New Dev Role')
        
        # Edit job
        response = self.client.post(reverse('edit_job', kwargs={'pk': new_job.id}), {
            'title': 'Senior Dev Role',
            'company_name': 'EmployerCorp',
            'domain': 'IT',
            'location': 'Bangalore',
            'skills_required': 'Python',
            'salary_range': '10L - 15L',
            'job_type': 'Full-Time',
            'experience_required': 3,
            'description': 'Updated description text'
        })
        self.assertEqual(response.status_code, 302)
        new_job.refresh_from_db()
        self.assertEqual(new_job.title, 'Senior Dev Role')
        
        # Toggle job status (deactivate)
        self.assertTrue(new_job.is_active)
        response = self.client.get(reverse('toggle_job_status', kwargs={'pk': new_job.id}))
        new_job.refresh_from_db()
        self.assertFalse(new_job.is_active)

    def test_email_alerts_on_apply_and_status_update(self):
        from django.core import mail
        
        # Clear outbox
        mail.outbox = []
        
        # Candidate applies for job
        self.client.force_login(self.user)
        response = self.client.post(reverse('apply_job', kwargs={'pk': self.job2.id}), {
            'cover_letter': 'Exciting React role!'
        })
        self.assertEqual(response.status_code, 302)
        
        # Verify apply email is sent
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn("Application Received", mail.outbox[0].subject)
        self.assertIn(self.user.email, mail.outbox[0].to)
        
        # Employer logs in and updates status
        employer = User.objects.create_user(
            email='employer2@example.com',
            password='Password123!',
            is_employer=True
        )
        self.job2.posted_by = employer
        self.job2.save()
        
        self.client.force_login(employer)
        application = Application.objects.get(user=self.user, job=self.job2)
        
        # Post status update
        response = self.client.post(reverse('manage_applicants', kwargs={'pk': self.job2.id}), {
            'application_id': application.id,
            'status': 'Shortlisted'
        })
        self.assertEqual(response.status_code, 302)
        
        # Verify status update email is sent
        self.assertEqual(len(mail.outbox), 2)
        self.assertIn("Application Status Update", mail.outbox[1].subject)
        self.assertIn("Shortlisted", mail.outbox[1].body)


class MCQPrepTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='candidate_test@example.com',
            password='Password123!',
            is_candidate=True
        )

    def test_mcq_prep_access_candidate(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('prep_landing'))
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse('prep_quiz', kwargs={'domain': 'it'}))
        self.assertEqual(response.status_code, 200)

    def test_mcq_prep_access_anonymous(self):
        response = self.client.get(reverse('prep_landing'))
        self.assertEqual(response.status_code, 302) # Redirect to login

    def test_resume_preferences_access(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('resume_preferences'))
        self.assertEqual(response.status_code, 200)

    def test_resume_preferences_post_and_fallback(self):
        self.client.force_login(self.user)
        
        # Create active jobs to match against
        Job.objects.create(
            title='React Dev',
            company_name='Frontend Ltd',
            domain='IT',
            location='Chennai',
            skills_required='React, JavaScript',
            experience_required=1
        )
        
        from django.core.files.uploadedfile import SimpleUploadedFile
        # Post a dummy PDF resume
        resume = SimpleUploadedFile("resume.pdf", b"%PDF-1.4 ... dummy text without matching skills", content_type="application/pdf")
        response = self.client.post(reverse('resume_preferences'), {'resume_file': resume})
        # Should redirect to resume_preferences page after successful upload
        self.assertEqual(response.status_code, 302)
        
        # Verify the file is uploaded
        self.user.refresh_from_db()
        self.assertTrue(self.user.resume_file)
        
        # Get preferences page and check if it falls back properly
        response = self.client.get(reverse('resume_preferences'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['is_fallback'])
        self.assertGreater(len(response.context['matching_jobs']), 0)


