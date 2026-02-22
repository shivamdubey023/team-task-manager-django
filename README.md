# Team Task Manager – Basic Version (1-Tier Architecture)

A professional-grade task management system built with Django and Django REST Framework. Designed for small to medium teams to efficiently manage tasks, track progress, and generate sprint reports.

## 🎯 Project Overview

Team Task Manager is a web-based application that enables teams to:
- Authenticate securely with role-based access
- Create, assign, and track tasks
- Manage task workflow (Todo → In Progress → Done)
- Automate recurring task creation
- Generate weekly sprint performance reports

**Version:** 1.0 (1-Tier Architecture)  
**Status:** In Development  
**Python Version:** 3.10+  
**Framework:** Django 6.0+

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10 or higher
- pip (Python package manager)
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd team-task-manager
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   ```

3. **Activate virtual environment**
   - **Windows:**
     ```bash
     venv\Scripts\activate
     ```
   - **macOS/Linux:**
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Apply database migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create superuser (admin)**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run development server**
   ```bash
   python manage.py runserver
   ```

8. **Access the application**
   - Application: `http://localhost:8000`
   - Admin Panel: `http://localhost:8000/admin`

---

## 📋 Tech Stack

### Backend
- **Framework:** Django 6.0+
- **REST API:** Django REST Framework
- **Database:** SQLite (Development) / PostgreSQL (Production-ready)
- **Authentication:** Django's built-in User model + session-based auth
- **Task Scheduler:** APScheduler (for automation)

### Frontend
- **HTML5:** Semantic markup
- **CSS3:** Professional styling (Bootstrap 5 compatible)
- **JavaScript:** Vanilla JS for interactivity
- **Templates:** Django template engine

### Development Tools
- **Version Control:** Git
- **Virtual Environment:** Python venv
- **Database Management:** Django ORM

---

## 📁 Project Structure

```
team-task-manager/
├── config/                 # Project configuration
│   ├── settings.py        # Django settings
│   ├── urls.py            # URL routing
│   └── wsgi.py            # WSGI configuration
├── tasks/                  # Main app
│   ├── models.py          # Database models
│   ├── views.py           # View logic
│   ├── urls.py            # App URL routing
│   ├── forms.py           # Django forms
│   ├── admin.py           # Admin configuration
│   └── migrations/        # Database migrations
├── templates/              # HTML templates
│   ├── base.html          # Base template
│   ├── login.html         # Login page
│   ├── dashboard.html     # Task dashboard
│   ├── task_form.html     # Task creation/edit
│   └── report.html        # Sprint report
├── static/                 # Static files (CSS, JS, images)
│   ├── css/
│   ├── js/
│   └── images/
├── venv/                   # Virtual environment (not committed)
├── manage.py              # Django management script
├── requirements.txt       # Python dependencies
├── .gitignore             # Git ignore rules
├── .env                   # Environment variables (not committed)
├── README.md              # This file
├── FEATURES.md            # Feature documentation
└── ARCHITECTURE.md        # Architecture documentation
```

---

## 🔐 Authentication Flow

1. **Unauthenticated User** → Redirected to login
2. **Login** → Django session created
3. **Dashboard Access** → Session verified, user-specific tasks loaded
4. **Logout** → Session destroyed, redirected to login

**Only authenticated users can:**
- View their tasks
- Create new tasks
- Modify task status
- View their weekly reports

---

## 💾 Database Models

### User Model (Django Built-in)
- Uses Django's default `User` model
- Fields: username, email, password, first_name, last_name, is_active, date_joined

### Task Model
- **title:** CharField (max_length=200)
- **description:** TextField
- **assignee:** ForeignKey to User
- **status:** CharField (choices: todo, inprogress, done)
- **created_at:** DateTimeField (auto-generated)
- **updated_at:** DateTimeField (auto-updated)
- **due_date:** DateField (nullable)

---

## 🎮 Core Features

### 1. Authentication System
- User login with credentials
- Session management
- Logout functionality
- `@login_required` decorator on all views

### 2. Task Management
- Create tasks with title, description, assignee
- Edit task details
- Delete tasks (only owned tasks)
- Auto-assign to creator

### 3. Task Workflow
- Move tasks between statuses: Todo → In Progress → Done
- Button-based status changes on dashboard
- Real-time status updates

### 4. Automation
- Auto-assign new tasks to creator
- Optional: Auto-create recurring weekly tasks (configurable)

### 5. Sprint Reports
- Weekly performance metrics
- Tasks created this week
- Tasks completed this week
- Completion percentage
- Generated per user

---

## 🔄 API Endpoints (1-Tier - Django Views)

### Authentication
- `GET/POST /login/` – User login
- `GET /logout/` – User logout

### Tasks
- `GET /` – Dashboard (list all user tasks)
- `GET/POST /task/create/` – Create new task
- `GET/POST /task/<id>/update/` – Update task
- `DELETE /task/<id>/delete/` – Delete task
- `POST /task/<id>/status/<status>/` – Change task status

### Reports
- `GET /report/` – Weekly sprint report

---

## ⚙️ Configuration

### settings.py Key Configuration
```python
LOGIN_REDIRECT_URL = 'dashboard'
LOGOUT_REDIRECT_URL = 'login'
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'tasks',
]
```

### Environment Variables (.env)
```
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
```

---

## 🧪 Testing

```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test tasks

# Run with coverage
coverage run --source='.' manage.py test
coverage report
```

---

## 📊 Performance Considerations

### Optimization Strategies (1-Tier)
1. **Database Indexing** – Indexes on `assignee` and `created_at`
2. **Query Optimization** – Use `select_related()` and `prefetch_related()`
3. **Caching** – Cache weekly report calculations
4. **Pagination** – Implement task list pagination (coming v2)

---

## 🚀 Deployment (Future Versions)

For production deployment:
1. Use PostgreSQL instead of SQLite
2. Collect static files: `python manage.py collectstatic`
3. Set `DEBUG=False`
4. Use gunicorn: `gunicorn config.wsgi`
5. Use Nginx as reverse proxy
6. Enable HTTPS/SSL

---

## 📝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for development guidelines.

---

## 📄 License

MIT License - See LICENSE file for details

---

## 👥 Author

Developed as a professional-grade task management system.

---

## 📞 Support

For issues or feature requests, please open an issue on the repository.

---

**Last Updated:** February 22, 2026  
**Version:** 1.0-alpha
