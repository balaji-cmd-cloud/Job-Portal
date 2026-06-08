import re
from django.urls import reverse
from jobs.models import Job
from jobs.recommender import get_recommendations_for_user, get_trending_skills

def get_chatbot_response(user_message, user=None):
    """
    Simulates a career counseling AI by returning HTML formatted responses.
    Integrates live data from the database (jobs list, recommendations, skills).
    """
    msg = user_message.lower().strip()
    
    # 1. Greetings
    if re.search(r'\b(hi|hello|hey|greetings|hola)\b', msg):
        name_clause = f", {user.first_name}" if (user and user.is_authenticated and user.first_name) else ""
        return (
            f"<p>Hello{name_clause}! 👋 I am your AI Career Assistant.</p>"
            "<p>I can help you with:</p>"
            "<ul>"
            "<li><strong>Career pathways</strong> (e.g., 'How to become a Software Engineer')</li>"
            "<li><strong>Skill suggestions</strong> (e.g., 'What are trending skills?')</li>"
            "<li><strong>Job search matching</strong> (e.g., 'Recommend jobs for me')</li>"
            "</ul>"
            "<p>What would you like to discuss today?</p>"
        )

    # 2. Requesting Job Recommendations
    if "recommend" in msg or "suggest job" in msg or "find job" in msg or "matching job" in msg:
        if not user or not user.is_authenticated:
            return (
                "<p>I can recommend tailored jobs for you! However, you are currently not logged in.</p>"
                f"<p>Please <a href='{reverse('login')}'>Log In</a> or <a href='{reverse('register')}'>Register</a> to complete your profile skills and get personal suggestions.</p>"
                "<p>Meanwhile, here are some active listings:</p>" + get_recent_jobs_html()
            )
        
        # Get recommended jobs
        recommended = get_recommendations_for_user(user, limit=4)
        if not recommended:
            return (
                "<p>I couldn't find matches tailored to your profile yet. Make sure to update your skills and domain in your profile!</p>"
                "<p>In the meantime, here are some active listings:</p>" + get_recent_jobs_html()
            )
            
        html = "<p>Here are some AI-recommended jobs based on your profile:</p><ul>"
        for job in recommended:
            job_url = reverse('job_detail', args=[job.id])
            html += f"<li><a href='{job_url}' target='_blank'><strong>{job.title}</strong></a> at {job.company_name} ({job.location})</li>"
        html += "</ul><p>Click any link to view details and apply!</p>"
        return html

    # 3. Requesting Trending Skills
    if "skill" in msg or "learn" in msg or "trending" in msg or "technolog" in msg:
        skills = get_trending_skills(limit=6)
        skills_list = "".join([f"<li><strong>{s}</strong></li>" for s in skills])
        return (
            "<p>Based on our active job listings, the most in-demand skills are:</p>"
            f"<ol>{skills_list}</ol>"
            "<p>Updating your profile with these skills can help increase your profile visibility to recruiters!</p>"
        )

    # 4. Career Guidance: Software Engineering / Web Development
    if "software" in msg or "developer" in msg or "coder" in msg or "programmer" in msg or "web dev" in msg:
        return (
            "<p><strong>Pathway to becoming a Software Engineer / Web Developer:</strong></p>"
            "<ol>"
            "<li><strong>Master core fundamentals:</strong> Learn HTML, CSS, JavaScript, and at least one backend language (Python, Java, Node.js).</li>"
            "<li><strong>Adopt frameworks:</strong> Build projects using Django, React, or Angular to understand MVC architectures.</li>"
            "<li><strong>Understand databases:</strong> Learn SQL (SQLite, PostgreSQL) and REST APIs.</li>"
            "<li><strong>Version Control:</strong> Host your code on GitHub to show recruiters your portfolio.</li>"
            "</ol>"
            f"<p>Check out our <a href='{reverse('job_list')}?q=Software'>Software Developer Job listings</a> to see active requirements!</p>"
        )

    # 5. Career Guidance: Data Science / AI / ML
    if "data" in msg or "analyst" in msg or "science" in msg or "machine learning" in msg or "ai" in msg:
        return (
            "<p><strong>Pathway to becoming a Data Scientist / Analyst:</strong></p>"
            "<ol>"
            "<li><strong>Learn Programming:</strong> Gain proficiency in Python or R.</li>"
            "<li><strong>Statistics & Math:</strong> Study probability, linear algebra, and data distributions.</li>"
            "<li><strong>Data manipulation:</strong> Learn libraries like Pandas, NumPy, and SQL.</li>"
            "<li><strong>Visualization & Modeling:</strong> Master Scikit-Learn, Matplotlib, and Tableau or PowerBI.</li>"
            "</ol>"
            f"<p>Explore our active <a href='{reverse('job_list')}?q=Data'>Data Science listings</a> to apply.</p>"
        )

    # 6. Career Guidance: Marketing & Sales
    if "market" in msg or "sales" in msg or "seo" in msg:
        return (
            "<p><strong>Pathway to a Career in Digital Marketing & Sales:</strong></p>"
            "<ol>"
            "<li><strong>Learn SEO & SEM:</strong> Understand search engine optimization and running Google Ads campaigns.</li>"
            "<li><strong>Data Analytics:</strong> Learn to read traffic reports in Google Analytics.</li>"
            "<li><strong>Content Creation:</strong> Develop copywriting, social media management, and email campaign skills.</li>"
            "</ol>"
            f"<p>Browse <a href='{reverse('job_list')}?q=Marketing'>Marketing Jobs here</a>.</p>"
        )

    # 7. Resume / Job Application Advice
    if "resume" in msg or "cv" in msg or "apply" in msg or "interview" in msg:
        return (
            "<p><strong>Career Advice for Applications:</strong></p>"
            "<ul>"
            "<li><strong>Customize:</strong> Tailor your resume summary to align with the specific job requirements.</li>"
            "<li><strong>Action Verbs:</strong> Start sentences with action words (e.g. 'Designed', 'Led', 'Optimized').</li>"
            "<li><strong>Include Keywords:</strong> Ensure skills specified in the job posting are reflected in your profile.</li>"
            "</ul>"
        )

    # Default general response
    return (
        "<p>I'm not sure I understand that request completely. I am trained in career guidance and job matching.</p>"
        "<p>Try asking me questions like:</p>"
        "<ul>"
        "<li><em>'How do I become a Software Engineer?'</em></li>"
        "<li><em>'Recommend jobs for me'</em></li>"
        "<li><em>'What are the trending skills?'</em></li>"
        "<li><em>'Give me resume writing tips'</em></li>"
        "</ul>"
    )

def get_recent_jobs_html():
    """Helper to list a few active jobs as HTML links"""
    recent_jobs = Job.objects.filter(is_active=True).order_by('-created_at')[:3]
    if not recent_jobs:
        return "<p>No active jobs found in the database at the moment.</p>"
    
    html = "<ul>"
    for job in recent_jobs:
        job_url = reverse('job_detail', args=[job.id])
        html += f"<li><a href='{job_url}' target='_blank'>{job.title} at {job.company_name}</a></li>"
    html += "</ul>"
    return html
