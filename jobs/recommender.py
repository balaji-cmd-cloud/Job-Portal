from django.db.models import Q
from collections import Counter
import os
import re
import zipfile
import xml.etree.ElementTree as ET
from .models import Job

def normalize_spaced_text(text):
    if not text:
        return ""
    
    # Check if this text is spaced out line by line
    normalized_lines = []
    has_spaced_line = False
    
    for line in text.split('\n'):
        tokens = line.split()
        if not tokens:
            normalized_lines.append("")
            continue
            
        single_char_tokens = [t for t in tokens if len(t) == 1]
        # If more than 50% of the tokens on this line are single characters, and line is long enough
        if len(tokens) >= 3 and len(single_char_tokens) / len(tokens) > 0.5:
            has_spaced_line = True
            # Split by double spaces to get the actual words/phrases
            words = line.split('  ')
            cleaned_words = []
            for w in words:
                cw = w.replace(' ', '')
                if cw:
                    cleaned_words.append(cw)
            normalized_lines.append(" ".join(cleaned_words))
        else:
            normalized_lines.append(line)
            
    if has_spaced_line:
        return "\n".join(normalized_lines)
    return text


def extract_text_from_file(file_path, file_name):
    """
    Extracts text from PDF, DOCX, or DOC files using dependency-minimal approaches.
    """
    ext = os.path.splitext(file_name)[1].lower()
    text = ""
    if ext == '.docx':
        try:
            with zipfile.ZipFile(file_path) as docx:
                xml_content = docx.read('word/document.xml')
                root = ET.fromstring(xml_content)
                ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
                text_elements = root.findall('.//w:t', ns)
                text = " ".join([elem.text for elem in text_elements if elem.text])
        except Exception:
            pass
    elif ext == '.pdf':
        try:
            from pypdf import PdfReader
            reader = PdfReader(file_path)
            pages_text = []
            for page in reader.pages:
                t = page.extract_text()
                if t:
                    pages_text.append(t)
            text = " ".join(pages_text)
        except Exception:
            pass
    elif ext == '.doc':
        try:
            with open(file_path, 'rb') as f:
                content = f.read()
            import string
            printable = set(string.printable.encode('ascii'))
            text = "".join([chr(b) for b in content if b in printable])
        except Exception:
            pass

    if text:
        text = normalize_spaced_text(text)
    return text

def extract_skills_from_text(text, available_skills):
    """
    Scans the text for available skills (case-insensitive) and returns a list of matched skills.
    """
    if not text or not available_skills:
        return []
    matched = []
    text_lower = text.lower()
    for skill in available_skills:
        pattern = r'\b' + re.escape(skill.lower()) + r'\b'
        if re.search(pattern, text_lower):
            matched.append(skill)
    return matched

def get_recommendations_for_user(user, limit=5):
    """
    Suggests jobs based on user profile (domain, location, skills, experience).
    Also parses the user's uploaded resume file for skills/keywords if present.
    Returns a sorted list of job objects.
    """
    if not user.is_authenticated or not user.is_candidate:
        # Fallback to latest jobs for unauthenticated users or employers
        return Job.objects.filter(is_active=True).order_by('-created_at')[:limit]

    # Parse resume text if file exists
    parsed_resume_skills = []
    resume_domain = ""
    if user.resume_file:
        try:
            resume_path = user.resume_file.path
            resume_name = user.resume_file.name
            if os.path.exists(resume_path):
                resume_text = extract_text_from_file(resume_path, resume_name)
                
                # Fetch all unique skills across active jobs
                active_jobs = Job.objects.filter(is_active=True)
                all_db_skills = set()
                for job in active_jobs:
                    all_db_skills.update([s.strip() for s in job.get_skills_list()])
                
                parsed_resume_skills = extract_skills_from_text(resume_text, all_db_skills)
                
                # Extract domain fallback
                resume_text_lower = resume_text.lower()
                domains_mapping = {
                    'it': ['it', 'software', 'developer', 'react', 'python', 'django', 'programming', 'web development', 'backend', 'frontend'],
                    'finance': ['finance', 'analyst', 'tax', 'accounting', 'auditing', 'excel', 'investment'],
                    'marketing': ['marketing', 'sales', 'seo', 'sem', 'ads', 'google analytics', 'copywriting'],
                    'hr': ['hr', 'recruiting', 'onboarding', 'human resources', 'talent acquisition'],
                    'healthcare': ['healthcare', 'clinical', 'research', 'biotech', 'medical', 'pharmacy']
                }
                for dom, keywords in domains_mapping.items():
                    if any(re.search(r'\b' + re.escape(kw) + r'\b', resume_text_lower) for kw in keywords):
                        resume_domain = dom
                        break
        except Exception:
            pass

    user_skills = [s.lower() for s in user.get_skills_list()]
    # Merge parsed resume skills
    for skill in parsed_resume_skills:
        skill_lower = skill.lower()
        if skill_lower not in user_skills:
            user_skills.append(skill_lower)

    user_domain = user.domain.strip().lower() if user.domain else resume_domain
    user_location = user.location.strip().lower() if user.location else ""
    user_exp = user.experience_years

    # If user profile is completely empty, return recent jobs
    if not user_skills and not user_domain and not user_location:
        return Job.objects.filter(is_active=True).order_by('-created_at')[:limit]

    # Pre-filter: get active jobs that match either domain, location, or have overlapping skills
    query = Q(is_active=True)
    domain_query = Q()
    location_query = Q()
    skills_query = Q()

    if user_domain:
        domain_query = Q(domain__iexact=user_domain)
    if user_location:
        location_query = Q(location__icontains=user_location)
    
    # Check for skill overlap in query
    if user_skills:
        for skill in user_skills:
            skills_query |= Q(skills_required__icontains=skill)

    # Combine queries
    combined_query = domain_query | location_query | skills_query
    if combined_query:
        jobs = Job.objects.filter(Q(is_active=True) & combined_query)
    else:
        jobs = Job.objects.filter(is_active=True)

    # Scored ranking
    scored_jobs = []
    for job in jobs:
        score = 0
        
        # 1. Domain match (high weight)
        if user_domain and job.domain.strip().lower() == user_domain:
            score += 15
            
        # 2. Location match (medium weight)
        if user_location and user_location in job.location.strip().lower():
            score += 10
            
        # 3. Skills match (dynamic weight)
        job_skills = [s.lower() for s in job.get_skills_list()]
        if user_skills and job_skills:
            matching_skills = set(user_skills).intersection(set(job_skills))
            # Score represents percentage of job's skills user possesses
            score += len(matching_skills) * 8
            
        # 4. Experience match
        # Prefer jobs where user meets or slightly exceeds experience, penalize extreme differences
        diff = user_exp - job.experience_required
        if diff >= 0:
            score += 5  # Meets requirement
            if diff <= 2:
                score += 3  # Optimal experience fit
        else:
            score -= (abs(diff) * 2)  # Penalty for under-experience
            
        scored_jobs.append((job, score))
        
    # Sort by score descending and return top matches
    scored_jobs.sort(key=lambda x: x[1], reverse=True)
    return [job for job, score in scored_jobs[:limit]]


def get_related_jobs(reference_job, limit=3):
    """
    Returns jobs related to the reference job based on domain and matching skills.
    """
    active_jobs = Job.objects.filter(is_active=True).exclude(id=reference_job.id)
    ref_domain = reference_job.domain.strip().lower()
    ref_skills = [s.lower() for s in reference_job.get_skills_list()]

    scored_jobs = []
    for job in active_jobs:
        score = 0
        # Domain match
        if job.domain.strip().lower() == ref_domain:
            score += 10
            
        # Skills match
        job_skills = [s.lower() for s in job.get_skills_list()]
        if ref_skills and job_skills:
            matching_skills = set(ref_skills).intersection(set(job_skills))
            score += len(matching_skills) * 5
            
        if score > 0:
            scored_jobs.append((job, score))
            
    scored_jobs.sort(key=lambda x: x[1], reverse=True)
    
    # Fallback to general latest active jobs if no related jobs scored
    if not scored_jobs:
        return list(active_jobs.order_by('-created_at')[:limit])
        
    return [job for job, score in scored_jobs[:limit]]


def get_trending_skills(limit=8):
    """
    Extracts the most frequent skills required in current active job posts.
    """
    active_jobs = Job.objects.filter(is_active=True)
    all_skills = []
    
    for job in active_jobs:
        all_skills.extend([s.strip().title() for s in job.get_skills_list()])
        
    if not all_skills:
        # Default trending skills if database has no entries
        return ["Python", "JavaScript", "React", "Django", "SQL", "Docker", "AWS", "Git"][:limit]
        
    skill_counts = Counter(all_skills)
    trending = [skill for skill, count in skill_counts.most_common(limit)]
    return trending
