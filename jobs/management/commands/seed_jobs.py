from django.core.management.base import BaseCommand
from jobs.models import Job

class Command(BaseCommand):
    help = 'Seeds the database with realistic sample job postings across domains'

    def handle(self, *args, **kwargs):
        jobs_data = [
            # IT / Software Development
            {
                'title': 'Python Developer',
                'company_name': 'Coimbatore Tech Solutions',
                'domain': 'IT',
                'location': 'Coimbatore',
                'description': 'We are looking for a Python Developer to join our engineering team in Coimbatore. You will design, build, and maintain robust scalable web applications using Python and Django.',
                'skills_required': 'Python, Django, SQL, REST APIs, Git',
                'salary_range': '₹6L - ₹10L',
                'job_type': 'Full-Time',
                'experience_required': 2,
            },
            {
                'title': 'Senior Python Developer',
                'company_name': 'TechSolutions India',
                'domain': 'IT',
                'location': 'Bangalore (Hybrid)',
                'description': 'We are looking for a Senior Python Developer to join our backend engineering team. You will design, build, and maintain robust scalable web applications and REST APIs using Python and Django.\n\nRequirements:\n- Strong knowledge of Python and Django framework.\n- Experience with SQL databases (SQLite, PostgreSQL).\n- Understanding of Git, Docker, and AWS services.',
                'skills_required': 'Python, Django, SQL, REST APIs, Git, Docker, AWS',
                'salary_range': '₹15L - ₹22L',
                'job_type': 'Full-Time',
                'experience_required': 5,
            },
            {
                'title': 'Frontend Engineer (React)',
                'company_name': 'InnoWeb Technologies',
                'domain': 'IT',
                'location': 'Remote',
                'description': 'Join our product team as a React developer. You will collaborate on clean UI design systems, optimize app performance, and write responsive modular code using Bootstrap 5 and modern React architectures.\n\nRequirements:\n- Proficient in JavaScript, HTML5, CSS3, and React.\n- Familiarity with TailwindCSS or Bootstrap 5.\n- Experience with state management tools like Redux.',
                'skills_required': 'JavaScript, React, HTML, CSS, Bootstrap 5, Redux',
                'salary_range': '₹8L - ₹14L',
                'job_type': 'Remote',
                'experience_required': 2,
            },
            {
                'title': 'Machine Learning Engineer',
                'company_name': 'Brainwave AI',
                'domain': 'IT',
                'location': 'Hyderabad',
                'description': 'We are seeking a Machine Learning Engineer to design and deploy AI models. You will work on natural language processing models, data pipelines, and predictive algorithms.\n\nRequirements:\n- Solid Python skills.\n- Experience with Pandas, NumPy, Scikit-Learn, and PyTorch.\n- Knowledge of SQL databases.',
                'skills_required': 'Python, Pandas, NumPy, Scikit-Learn, PyTorch, SQL, AI, Machine Learning',
                'salary_range': '₹18L - ₹28L',
                'job_type': 'Full-Time',
                'experience_required': 4,
            },
            # Finance
            {
                'title': 'Financial Analyst',
                'company_name': 'Capital Trust',
                'domain': 'Finance',
                'location': 'Mumbai',
                'description': 'We are looking for an analytical mind to join our core Finance group. You will research market trends, manage budgets, analyze balance sheets, and present projections to stakeholders.\n\nRequirements:\n- Degree in Finance, Economics, or MBA.\n- High proficiency in Excel and financial modeling.\n- Strong data representation skills.',
                'skills_required': 'Excel, Financial Modeling, Analytics, Finance, SQL',
                'salary_range': '₹10L - ₹15L',
                'job_type': 'Full-Time',
                'experience_required': 3,
            },
            {
                'title': 'Tax Associate',
                'company_name': 'Apex Tax & Audit',
                'domain': 'Finance',
                'location': 'Pune',
                'description': 'Perform auditing, prepare tax filings, and consult corporate clients on regulatory compliances.\n\nRequirements:\n- Certified CA or equivalent financial degree.\n- Experience with Indian tax regulations.',
                'skills_required': 'Taxation, Auditing, Finance, Excel',
                'salary_range': '₹6L - ₹10L',
                'job_type': 'Contract',
                'experience_required': 1,
            },
            # Marketing / Sales
            {
                'title': 'Digital Marketing Specialist',
                'company_name': 'BrandViral Corp',
                'domain': 'Marketing',
                'location': 'Remote',
                'description': 'Drive organic and paid user acquisition. You will draft campaigns, analyze SEO patterns, manage social media handles, and analyze conversion channels using Google Analytics.\n\nRequirements:\n- Experience with SEO, SEM, Google Ads, and Facebook Ads manager.\n- Excellent copywriting skills.',
                'skills_required': 'SEO, SEM, Copywriting, Google Analytics, Marketing, Social Media',
                'salary_range': '₹7L - ₹11L',
                'job_type': 'Remote',
                'experience_required': 2,
            },
            {
                'title': 'Sales Account Manager',
                'company_name': 'SaaSify Inc',
                'domain': 'Marketing',
                'location': 'Bangalore',
                'description': 'Manage client relations, pitch enterprise SaaS products, and close enterprise contracts.\n\nRequirements:\n- Prior B2B sales experience.\n- Excellent English presentation and communication.',
                'skills_required': 'Sales, B2B, SaaS, Negotiation, Communication',
                'salary_range': '₹12L - ₹18L',
                'job_type': 'Full-Time',
                'experience_required': 3,
            },
            # HR / Operations
            {
                'title': 'HR Manager',
                'company_name': 'Global HR Hub',
                'domain': 'HR',
                'location': 'Delhi NCR',
                'description': 'Overlook company recruiting, onboard new hires, manage employee retention cycles, and update training documentation.\n\nRequirements:\n- Master degree in Human Resources.\n- Experience handling conflict resolution and HR policies.',
                'skills_required': 'Recruiting, Onboarding, HR Policies, Communication',
                'salary_range': '₹9L - ₹13L',
                'job_type': 'Full-Time',
                'experience_required': 4,
            },
            # Healthcare
            {
                'title': 'Clinical Research Associate',
                'company_name': 'PharmaLife Labs',
                'domain': 'Healthcare',
                'location': 'Chennai',
                'description': 'Monitor clinical trials, draft regulatory paperwork, and inspect compliance at clinical research sites.\n\nRequirements:\n- Degree in Pharmacy, BioTech, or Nursing.\n- Knowledge of clinical trial regulations.',
                'skills_required': 'Clinical Trials, Research, Biotech, Healthcare',
                'salary_range': '₹8L - ₹12L',
                'job_type': 'Full-Time',
                'experience_required': 2,
            }
        ]

        created_count = 0
        for job_info in jobs_data:
            job, created = Job.objects.get_or_create(
                title=job_info['title'],
                company_name=job_info['company_name'],
                defaults=job_info
            )
            if created:
                created_count += 1

        self.stdout.write(self.style.SUCCESS(f'Successfully processed jobs. Created {created_count} new jobs.'))
