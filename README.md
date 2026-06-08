# NaukriAI - Naukri-inspired Job Portal with AI Capabilities

A premium, production-ready Job Portal web application built using **Django, Bootstrap 5, HTML, CSS, JavaScript, and SQLite**. The UI implements a modern glassmorphism design system supporting light/dark themes and a fluid responsive layout for desktop and mobile views.

---

## Key Features

1. **Email-Based Authentication System**:
   - Custom User model where the primary key/username is the user's `email`.
   - Custom authentication backends to handle case-insensitive email matching.
   - Comprehensive password validation checking for length (8+ chars), uppercase, numeric, and special character combinations.
   
2. **Interactive Candidate Dashboard**:
   - Dynamic profile progress tracking bar (based on profile completeness).
   - Saved and applied application statistics.
   - Interactive sliding/collapsible chatbot panel.
   - Dynamic job search filtering by Domain, Title, and Location.

3. **Jobs Directory & Applications**:
   - Full search listing directory with Bootstrap 5 circular pagination.
   - Save or apply to roles interactively using AJAX fetch requests (without full page reloads).
   - Similar jobs suggestion sidebar on details pages.

4. **AI Recommendation & Trending Engine**:
   - Match algorithm calculating skill coverage ratio, experience level offsets, and location/domain matches to rank custom recommended jobs for Candidates.
   - Real-time aggregation of active job skills to display trending skills on the dashboard.

5. **AI Career Chatbot**:
   - Slide-out float widget with automated typing indicator animations.
   - Smart keyword counseling engine answering roadmap inquiries, resume tips, and suggesting database jobs as clickable HTML links.
   - Conversations are persisted in the database (`ChatHistory` model).

6. **REST API Layer**:
   - REST endpoints built with Django REST Framework (DRF) for Jobs, Applications, Pinned listings, and AI Career suggestions.

---

## Project Structure

```
├── manage.py
├── requirements.txt
├── README.md
│
├── job_portal/                 # Main settings & routes
│   ├── settings.py
│   └── urls.py
│
├── accounts/                   # Custom User & auth logic
│   ├── models.py
│   ├── auth_backends.py
│   ├── forms.py
│   └── views.py
│
├── jobs/                       # Job listings & recommendation engine
│   ├── models.py
│   ├── recommender.py          # AI algorithms
│   ├── api_views.py            # DRF endpoints
│   └── views.py
│
├── chatbot/                    # Chatbot API & history log
│   ├── models.py
│   ├── chatbot_logic.py        # Natural language parser
│   └── views.py
│
├── static/                     # Shared static assets
│   ├── css/styles.css          # Glassmorphism, Theme Variables
│   └── js/main.js              # Theme switcher, AJAX handles, Chat logic
│
└── templates/                  # Base structural templates
    └── base.html
```

---

## Installation & Setup Instructions

Ensure you have **Python 3.10+** installed on your system.

### 1. Clone & Initialize Environment
Open your command terminal inside the project directory and run:

```bash
# Create a virtual environment
python -m venv .venv

# Activate the virtual environment
# On Windows (PowerShell):
.venv\Scripts\Activate.ps1
# On Windows (cmd):
.venv\Scripts\activate.bat
# On macOS/Linux:
source .venv/bin/activate

# Install all dependencies
pip install -r requirements.txt
```

### 2. Apply Database Migrations
Create the SQLite database schemas for the custom user accounts, jobs, applications, and chat history models:

```bash
python manage.py makemigrations accounts jobs chatbot
python manage.py migrate
```

### 3. Seed Realistic Job Openings
We have included a database seeding command. Run it to automatically populate the platform with sample job posts in IT, Finance, Marketing, HR, and Healthcare:

```bash
python manage.py seed_jobs
```

### 4. Create an Admin Superuser
Create an administrative account to access the custom django admin control panel:

```bash
python manage.py createsuperuser
```
*(Enter your email, and a secure password).*

### 5. Launch the Development Server
Run the local dev server:

```bash
python manage.py runserver
```

Open your browser and navigate to: **[http://127.0.0.1:8000/](http://127.0.0.1:8000/)**

---

## Running Unit Tests
To verify all features (authentication, registration checks, recommender scores, chatbot history log, and REST APIs):

```bash
python manage.py test
```

---

## REST API Documentation

All APIs support standard JSON formats. For endpoints requiring authentication (Apply, Save, Recommendations), pass standard session auth or CSRF tokens in headers.

| Endpoint | Method | Auth Required | Description |
| :--- | :---: | :---: | :--- |
| `/jobs/api/` | `GET` | No | List all active jobs. Supports filtering via parameters `?q=`, `?domain=`, and `?location=`. |
| `/jobs/api/<id>/` | `GET` | No | Get detail object of a specific job posting. |
| `/jobs/api/<id>/save/` | `POST` | Yes | Toggle bookmark status of a job listing for candidate profile. |
| `/jobs/api/<id>/apply/` | `POST` | Yes | Submit application for a job post. Accepts `{"cover_letter": "text"}` in request body. |
| `/jobs/api/recommendations/` | `GET` | Yes | Fetch custom recommended job rankings for the logged-in candidate. |
| `/jobs/api/trending-skills/` | `GET` | No | Returns list of most commonly required skills in database. |
| `/chatbot/api/` | `POST` | No | Post message to career chatbot. Accepts `{"message": "text"}` and returns `{"response": "HTML_response"}`. Logs history in DB. |
