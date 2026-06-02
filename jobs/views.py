from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q

from .models import Job, Application, SavedJob
from .recommender import get_recommendations_for_user, get_related_jobs, get_trending_skills
from .forms import JobForm
from .email_services import send_application_confirmation, send_status_update_alert

@login_required
def dashboard_view(request):
    user = request.user
    
    # AI recommendations
    recommendations = get_recommendations_for_user(user, limit=6)
    trending_skills = get_trending_skills(limit=8)
    
    # User's current activity stats
    total_applied = Application.objects.filter(user=user).count()
    total_saved = SavedJob.objects.filter(user=user).count()
    
    # Profile completion indicator (heuristic)
    profile_score = 0
    if user.first_name: profile_score += 20
    if user.last_name: profile_score += 20
    if user.skills: profile_score += 20
    if user.domain: profile_score += 20
    if user.location: profile_score += 20
    
    # Extract preferences from resume if uploaded
    resume_skills = []
    resume_domain = ""
    if user.is_candidate and user.resume_file:
        try:
            import os
            import re
            from .recommender import extract_text_from_file, extract_skills_from_text
            resume_path = user.resume_file.path
            resume_name = user.resume_file.name
            if os.path.exists(resume_path):
                resume_text = extract_text_from_file(resume_path, resume_name)
                
                # Scan for unique skills across all active jobs
                active_jobs = Job.objects.filter(is_active=True)
                all_db_skills = set()
                for job in active_jobs:
                    all_db_skills.update([s.strip() for s in job.get_skills_list()])
                
                resume_skills = extract_skills_from_text(resume_text, all_db_skills)
                
                # Detect Domain
                resume_text_lower = resume_text.lower()
                domains_mapping = {
                    'IT / Software': ['it', 'software', 'developer', 'react', 'python', 'django', 'programming', 'web development', 'backend', 'frontend'],
                    'Finance': ['finance', 'analyst', 'tax', 'accounting', 'auditing', 'excel', 'investment'],
                    'Marketing & Sales': ['marketing', 'sales', 'seo', 'sem', 'ads', 'google analytics', 'copywriting'],
                    'HR': ['hr', 'recruiting', 'onboarding', 'human resources', 'talent acquisition'],
                    'Healthcare': ['healthcare', 'clinical', 'research', 'biotech', 'medical', 'pharmacy']
                }
                for dom, keywords in domains_mapping.items():
                    if any(re.search(r'\b' + re.escape(kw) + r'\b', resume_text_lower) for kw in keywords):
                        resume_domain = dom
                        break
        except Exception:
            pass

    context = {
        'recommendations': recommendations,
        'trending_skills': trending_skills,
        'total_applied': total_applied,
        'total_saved': total_saved,
        'profile_score': profile_score,
        'resume_skills': resume_skills,
        'resume_domain': resume_domain,
    }
    return render(request, 'jobs/dashboard.html', context)


def job_list_view(request):
    query = request.GET.get('q', '').strip()
    domain = request.GET.get('domain', '').strip()
    location = request.GET.get('location', '').strip()

    jobs = Job.objects.filter(is_active=True)
    is_fallback = False
    filters_applied = bool(query or domain or location)

    if filters_applied:
        from django.db.models import Case, When, Value, IntegerField
        
        # Build query conditions
        q_cond = Q(title__icontains=query) | Q(company_name__icontains=query) | Q(description__icontains=query) | Q(skills_required__icontains=query) if query else Q(id__isnull=True)
        domain_cond = Q(domain__icontains=domain) if domain else Q(id__isnull=True)
        loc_cond = Q(location__icontains=location) if location else Q(id__isnull=True)

        # Annotate each job with a match relevance score
        jobs = jobs.annotate(
            relevance_score=(
                Case(When(q_cond, then=Value(3)), default=Value(0), output_field=IntegerField()) +
                Case(When(domain_cond, then=Value(2)), default=Value(0), output_field=IntegerField()) +
                Case(When(loc_cond, then=Value(2)), default=Value(0), output_field=IntegerField())
            )
        )
        
        # Filter to show only jobs matching at least one parameter, ordering by relevance score
        jobs = jobs.filter(relevance_score__gt=0).order_by('-relevance_score', '-created_at')
        
        # Determine maximum possible score
        max_possible_score = 0
        if query: max_possible_score += 3
        if domain: max_possible_score += 2
        if location: max_possible_score += 2
        
        # If no job matched all the provided criteria, mark as fallback
        has_exact_match = jobs.filter(relevance_score=max_possible_score).exists()
        is_fallback = not has_exact_match
    else:
        jobs = jobs.order_by('-created_at')

    # Fetch applied and saved job IDs for candidate user to enable direct apply/save options on listings page
    applied_job_ids = set()
    saved_job_ids = set()
    if request.user.is_authenticated and request.user.is_candidate:
        applied_job_ids = set(Application.objects.filter(user=request.user).values_list('job_id', flat=True))
        saved_job_ids = set(SavedJob.objects.filter(user=request.user).values_list('job_id', flat=True))

    # Paginate results
    paginator = Paginator(jobs, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Maintain search params in pagination links
    params = request.GET.copy()
    if 'page' in params:
        del params['page']

    context = {
        'page_obj': page_obj,
        'query': query,
        'domain': domain,
        'location': location,
        'params': params.urlencode(),
        'is_fallback': is_fallback,
        'applied_job_ids': applied_job_ids,
        'saved_job_ids': saved_job_ids,
    }
    return render(request, 'jobs/job_list.html', context)


def job_detail_view(request, pk):
    job = get_object_or_404(Job, pk=pk, is_active=True)
    related_jobs = get_related_jobs(job, limit=3)
    
    has_applied = False
    has_saved = False
    
    if request.user.is_authenticated and request.user.is_candidate:
        has_applied = Application.objects.filter(user=request.user, job=job).exists()
        has_saved = SavedJob.objects.filter(user=request.user, job=job).exists()
        
    context = {
        'job': job,
        'related_jobs': related_jobs,
        'has_applied': has_applied,
        'has_saved': has_saved,
    }
    return render(request, 'jobs/job_detail.html', context)


@login_required
def apply_job_view(request, pk):
    if not request.user.is_candidate:
        messages.error(request, "Only job seekers can apply for jobs.")
        return redirect('job_detail', pk=pk)

    job = get_object_or_404(Job, pk=pk, is_active=True)
    
    if request.method == 'POST':
        cover_letter = request.POST.get('cover_letter', '')
        uploaded_file = request.FILES.get('resume_file')
        
        if uploaded_file:
            import os
            ext = os.path.splitext(uploaded_file.name)[1].lower()
            if ext not in ['.pdf', '.doc', '.docx']:
                messages.error(request, "Unsupported file format. Please upload a PDF, DOC, or DOCX document.")
                return render(request, 'jobs/apply_confirm.html', {'job': job})
            if uploaded_file.size > 5 * 1024 * 1024:
                messages.error(request, "File size exceeds the 5MB limit.")
                return render(request, 'jobs/apply_confirm.html', {'job': job})
            
            request.user.resume_file = uploaded_file
            request.user.save()
        elif not request.user.resume_file:
            messages.error(request, "You must upload a resume to submit your application.")
            return render(request, 'jobs/apply_confirm.html', {'job': job})
            
        application, created = Application.objects.get_or_create(
            user=request.user,
            job=job,
            defaults={'cover_letter': cover_letter}
        )
        
        if created:
            send_application_confirmation(application)
            messages.success(request, f"You have successfully applied for {job.title}!")
        else:
            messages.warning(request, "You have already applied for this job.")
            
        return redirect('my_applications')
        
    return render(request, 'jobs/apply_confirm.html', {'job': job})


@login_required
def save_job_view(request, pk):
    if not request.user.is_candidate:
        messages.error(request, "Only job seekers can save jobs.")
        return redirect('job_detail', pk=pk)

    job = get_object_or_404(Job, pk=pk, is_active=True)
    saved_job, created = SavedJob.objects.get_or_create(user=request.user, job=job)
    
    if not created:
        saved_job.delete()
        messages.info(request, "Job removed from saved list.")
    else:
        messages.success(request, "Job saved successfully.")
        
    return redirect(request.META.get('HTTP_REFERER', 'job_detail', pk=pk))


@login_required
def my_applications_view(request):
    if not request.user.is_candidate:
        messages.error(request, "Only job seekers have applications.")
        return redirect('dashboard')
        
    applications = Application.objects.filter(user=request.user).select_related('job')
    return render(request, 'jobs/my_applications.html', {'applications': applications})


@login_required
def saved_jobs_view(request):
    if not request.user.is_candidate:
        messages.error(request, "Only job seekers can save jobs.")
        return redirect('dashboard')
        
    saved_jobs = SavedJob.objects.filter(user=request.user).select_related('job')
    return render(request, 'jobs/saved_jobs.html', {'saved_jobs': saved_jobs})


# --- Employer Front-End Dashboard & Management Views ---

@login_required
def employer_dashboard_view(request):
    if not request.user.is_employer:
        messages.error(request, "Access denied. Only employers can access this dashboard.")
        return redirect('dashboard')
        
    posted_jobs = Job.objects.filter(posted_by=request.user).order_by('-created_at')
    
    # Enrich jobs with applicant counts
    for job in posted_jobs:
        job.applicant_count = job.applications.count()
        
    return render(request, 'jobs/employer_dashboard.html', {'posted_jobs': posted_jobs})


@login_required
def manage_applicants_view(request, pk):
    if not request.user.is_employer:
        messages.error(request, "Access denied. Only employers can manage applicants.")
        return redirect('dashboard')
        
    job = get_object_or_404(Job, pk=pk, posted_by=request.user)
    applications = job.applications.all().select_related('user')
    
    if request.method == 'POST':
        app_id = request.POST.get('application_id')
        new_status = request.POST.get('status')
        application = get_object_or_404(Application, id=app_id, job=job)
        
        if new_status in dict(Application.STATUS_CHOICES):
            application.status = new_status
            application.save()
            
            # Send status update email alert to the candidate
            send_status_update_alert(application)
            
            messages.success(request, f"Updated application status for {application.user.email} to '{new_status}'.")
        else:
            messages.error(request, "Invalid status choice.")
        return redirect('manage_applicants', pk=job.id)
        
    return render(request, 'jobs/manage_applicants.html', {'job': job, 'applications': applications})


@login_required
def create_job_view(request):
    if not request.user.is_employer:
        messages.error(request, "Access denied. Only employers can post jobs.")
        return redirect('dashboard')
        
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.posted_by = request.user
            job.save()
            messages.success(request, f"Successfully posted job listing: {job.title}!")
            return redirect('employer_dashboard')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = JobForm()
    return render(request, 'jobs/job_form.html', {'form': form, 'title': 'Post a New Job'})


@login_required
def edit_job_view(request, pk):
    if not request.user.is_employer:
        messages.error(request, "Access denied. Only employers can edit jobs.")
        return redirect('dashboard')
        
    job = get_object_or_404(Job, pk=pk, posted_by=request.user)
    
    if request.method == 'POST':
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            messages.success(request, f"Successfully updated job listing: {job.title}!")
            return redirect('employer_dashboard')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = JobForm(instance=job)
    return render(request, 'jobs/job_form.html', {'form': form, 'title': 'Edit Job Listing'})


@login_required
def toggle_job_status_view(request, pk):
    if not request.user.is_employer:
        messages.error(request, "Access denied.")
        return redirect('dashboard')
        
    job = get_object_or_404(Job, pk=pk, posted_by=request.user)
    job.is_active = not job.is_active
    job.save()
    
    state = "activated" if job.is_active else "deactivated"
    messages.info(request, f"Job listing '{job.title}' has been {state}.")
    return redirect('employer_dashboard')


@login_required
def prep_landing_view(request):
    return render(request, 'jobs/prep_landing.html')


@login_required
def prep_quiz_view(request, domain):
    from .prep_data import MCQ_QUESTIONS
    domain = domain.lower().strip()
    if domain not in MCQ_QUESTIONS:
        messages.error(request, "Invalid preparation domain.")
        return redirect('prep_landing')
        
    questions = MCQ_QUESTIONS[domain]
    domain_display = {
        'it': 'IT / Software Engineering',
        'finance': 'Finance',
        'marketing': 'Marketing & Sales',
        'hr': 'Human Resources (HR)'
    }.get(domain, domain.title())
    
    return render(request, 'jobs/prep_quiz.html', {
        'questions': questions,
        'domain': domain,
        'domain_display': domain_display
    })


@login_required
def resume_preferences_view(request):
    if not request.user.is_candidate:
        messages.error(request, "Only job seekers can access job preferences.")
        return redirect('dashboard')
        
    user = request.user
    
    if request.method == 'POST':
        uploaded_file = request.FILES.get('resume_file')
        if uploaded_file:
            import os
            ext = os.path.splitext(uploaded_file.name)[1].lower()
            if ext not in ['.pdf', '.doc', '.docx']:
                messages.error(request, "Unsupported file format. Please upload a PDF, DOC, or DOCX document.")
            elif uploaded_file.size > 5 * 1024 * 1024:
                messages.error(request, "File size exceeds the 5MB limit.")
            else:
                user.resume_file = uploaded_file
                user.save()
                messages.success(request, "Resume uploaded and preferences calculated successfully!")
                return redirect('resume_preferences')
        else:
            messages.error(request, "Please select a resume file to upload.")

    # Parse details if resume exists
    resume_skills = []
    resume_domain = ""
    matching_jobs = []
    
    if user.resume_file:
        try:
            import os
            import re
            from .recommender import extract_text_from_file, extract_skills_from_text
            resume_path = user.resume_file.path
            resume_name = user.resume_file.name
            if os.path.exists(resume_path):
                resume_text = extract_text_from_file(resume_path, resume_name)
                
                # Fetch all unique skills across active jobs
                active_jobs = Job.objects.filter(is_active=True)
                all_db_skills = set()
                for job in active_jobs:
                    all_db_skills.update([s.strip() for s in job.get_skills_list()])
                
                resume_skills = extract_skills_from_text(resume_text, all_db_skills)
                
                # Detect Domain
                resume_text_lower = resume_text.lower()
                domains_mapping = {
                    'IT / Software': ['it', 'software', 'developer', 'react', 'python', 'django', 'programming', 'web development', 'backend', 'frontend'],
                    'Finance': ['finance', 'analyst', 'tax', 'accounting', 'auditing', 'excel', 'investment'],
                    'Marketing & Sales': ['marketing', 'sales', 'seo', 'sem', 'ads', 'google analytics', 'copywriting'],
                    'HR': ['hr', 'recruiting', 'onboarding', 'human resources', 'talent acquisition'],
                    'Healthcare': ['healthcare', 'clinical', 'research', 'biotech', 'medical', 'pharmacy']
                }
                for dom, keywords in domains_mapping.items():
                    if any(re.search(r'\b' + re.escape(kw) + r'\b', resume_text_lower) for kw in keywords):
                        resume_domain = dom
                        break
                        
                # Match jobs based on resume skills
                from django.db.models import Case, When, Value, IntegerField
                if resume_skills or resume_domain:
                    # Score based on how many skills/domain match
                    q_skills = Q(id__isnull=True)
                    if resume_skills:
                        for s in resume_skills:
                            q_skills |= Q(skills_required__icontains=s)
                    
                    domain_q = Q(domain__icontains=resume_domain.split(' ')[0]) if resume_domain else Q(id__isnull=True)
                    
                    matching_jobs = list(Job.objects.filter(is_active=True).annotate(
                        match_score=(
                            Case(When(q_skills, then=Value(3)), default=Value(0), output_field=IntegerField()) +
                            Case(When(domain_q, then=Value(2)), default=Value(0), output_field=IntegerField())
                        )
                    ).filter(match_score__gt=0).order_by('-match_score', '-created_at')[:9])
        except Exception:
            pass

    # Fallback to general or profile recommendations if no direct keyword matches exist for the uploaded resume
    is_fallback = False
    fallback_reason = ""
    if user.resume_file and not matching_jobs:
        is_fallback = True
        from .recommender import get_recommendations_for_user
        matching_jobs = get_recommendations_for_user(user, limit=9)
        if not matching_jobs:
            matching_jobs = list(Job.objects.filter(is_active=True).order_by('-created_at')[:9])
            fallback_reason = "No direct matches found. Showing the latest active job openings on Apna."
        else:
            fallback_reason = "No direct matches found. Showing career options matching your profile and trending fields."

    # Fetch applied and saved jobs to enable direct action on lists
    applied_job_ids = set()
    saved_job_ids = set()
    if user.is_authenticated and user.is_candidate:
        applied_job_ids = set(Application.objects.filter(user=user).values_list('job_id', flat=True))
        saved_job_ids = set(SavedJob.objects.filter(user=user).values_list('job_id', flat=True))

    return render(request, 'jobs/resume_preferences.html', {
        'resume_skills': resume_skills,
        'resume_domain': resume_domain,
        'matching_jobs': matching_jobs,
        'is_fallback': is_fallback,
        'fallback_reason': fallback_reason,
        'applied_job_ids': applied_job_ids,
        'saved_job_ids': saved_job_ids,
    })


