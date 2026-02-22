# ARCHITECTURE.md – System Architecture & Design Decisions

**Version:** 1.0 (1-Tier Architecture)  
**Date:** February 22, 2026  
**Document Status:** Architecture Specification

---

## 📑 Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [System Architecture Diagram](#system-architecture-diagram)
3. [Component Breakdown](#component-breakdown)
4. [Data Flow](#data-flow)
5. [Database Schema](#database-schema)
6. [Authentication Flow](#authentication-flow)
7. [API/View Structure](#api-view-structure)
8. [Design Patterns](#design-patterns)
9. [Performance Considerations](#performance-considerations)
10. [Security Architecture](#security-architecture)
11. [Future Architecture (v2.0)](#future-architecture-v20)

---

## 🏗️ Architecture Overview

### Current Architecture: 1-Tier (Monolithic)

```
┌─────────────────────────────────────────┐
│        Team Task Manager v1.0           │
│       (Single Instance Deployment)      │
└─────────────────────────────────────────┘
     ↓ (HTTP/HTTPS)
┌─────────────────────────────────────────┐
│         Web Application Layer           │
│  ┌─────────────────────────────────┐   │
│  │    Django Application Server    │   │
│  │  (Gunicorn / Development)       │   │
│  └─────────────────────────────────┘   │
│         ↓ ↓ ↓                          │
│  ┌──────────────────────────────────┐  │
│  │  Application Logic               │  │
│  │  ├─ Authentication (Django Auth) │  │
│  │  ├─ Task Management              │  │
│  │  ├─ Reports Generation           │  │
│  │  └─ Automation Logic             │  │
│  └──────────────────────────────────┘  │
└─────────────────────────────────────────┘
     ↓ (Query/Write)
┌─────────────────────────────────────────┐
│       Database Layer (SQLite)           │
│  ┌──────────────────────────────────┐  │
│  │   User Table                     │  │
│  │   Task Table                     │  │
│  │   Session Table                  │  │
│  └──────────────────────────────────┘  │
└─────────────────────────────────────────┘
```

### Why 1-Tier for v1.0?

| Criteria | 1-Tier | Reason |
|----------|--------|--------|
| **Complexity** | Low | Easier to build and maintain |
| **Development Speed** | Fast | Fewer components = faster development |
| **Cost** | Very Low | Single server, no infrastructure |
| **Suitable for** | Small teams (1-50 users) | MVP phase |
| **Learning Value** | High | Understand monolithic before microservices |

---

## 📊 System Architecture Diagram

### High-Level Component Diagram

```
┌────────────────────────────────────────────────────────────┐
│                        Browser Client                      │
│          (HTML5 + CSS3 + Vanilla JavaScript)               │
└────────────────────────────────────────────────────────────┘
                            ↕ HTTP/HTTPS
┌────────────────────────────────────────────────────────────┐
│                    Django Web Server                       │
│  ┌──────────────────────────────────────────────────────┐  │
│  │            URL Routing Layer (urls.py)              │  │
│  │  • /login/ → auth_views.LoginView                  │  │
│  │  • / → tasks.views.dashboard                       │  │
│  │  • /task/create/ → tasks.views.create_task         │  │
│  │  • /task/<id>/status/ → tasks.views.change_status  │  │
│  │  • /report/ → tasks.views.weekly_report            │  │
│  └──────────────────────────────────────────────────────┘  │
│                            ↓                               │
│  ┌──────────────────────────────────────────────────────┐  │
│  │         View Layer (views.py)                        │  │
│  │                                                      │  │
│  │  ┌────────────────────────────────────────────────┐ │  │
│  │  │ Authentication Views                           │ │  │
│  │  │ • LoginView (Django built-in)                 │ │  │
│  │  │ • LogoutView (Django built-in)                │ │  │
│  │  │ • login_required decorator                    │ │  │
│  │  └────────────────────────────────────────────────┘ │  │
│  │                                                      │  │
│  │  ┌────────────────────────────────────────────────┐ │  │
│  │  │ Business Logic Views                           │ │  │
│  │  │ • dashboard(request)                          │ │  │
│  │  │ • create_task(request)                        │ │  │
│  │  │ • update_task(request, pk)                    │ │  │
│  │  │ • delete_task(request, pk)                    │ │  │
│  │  │ • change_status(request, pk, status)          │ │  │
│  │  │ • weekly_report(request)                      │ │  │
│  │  └────────────────────────────────────────────────┘ │  │
│  │                                                      │  │
│  └──────────────────────────────────────────────────────┘  │
│                            ↓                               │
│  ┌──────────────────────────────────────────────────────┐  │
│  │         Model Layer (models.py)                      │  │
│  │                                                      │  │
│  │  ┌────────────────────────────────────────────────┐ │  │
│  │  │ Django User Model (Built-in)                  │ │  │
│  │  │ • username, email, password, name, is_active  │ │  │
│  │  └────────────────────────────────────────────────┘ │  │
│  │                                                      │  │
│  │  ┌────────────────────────────────────────────────┐ │  │
│  │  │ Task Model (Custom)                           │ │  │
│  │  │ • title, description, assignee (FK→User)     │ │  │
│  │  │ • status (choices: todo, inprogress, done)    │ │  │
│  │  │ • created_at, updated_at, due_date           │ │  │
│  │  └────────────────────────────────────────────────┘ │  │
│  │                                                      │  │
│  └──────────────────────────────────────────────────────┘  │
│                            ↓                               │
│  ┌──────────────────────────────────────────────────────┐  │
│  │      Django ORM (Object-Relational Mapping)        │  │
│  │    • Translates Python to SQL automatically        │  │
│  │    • Handles database transactions                 │  │
│  │    • Provides query interface                      │  │
│  └──────────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────┘
                            ↓ SQL
┌────────────────────────────────────────────────────────────┐
│                  SQLite Database                           │
│  ┌──────────────────────────────────────────────────────┐  │
│  │         db.sqlite3 (Single File)                    │  │
│  │                                                      │  │
│  │  ┌─────────────────────────────────────────────┐   │  │
│  │  │ Users Table (auth_user)                     │   │  │
│  │  │ ├─ id (PK)                                 │   │  │
│  │  │ ├─ username                                │   │  │
│  │  │ ├─ email                                   │   │  │
│  │  │ └─ password (hashed)                       │   │  │
│  │  └─────────────────────────────────────────────┘   │  │
│  │                                                      │  │
│  │  ┌─────────────────────────────────────────────┐   │  │
│  │  │ Tasks Table (tasks_task)                    │   │  │
│  │  │ ├─ id (PK)                                 │   │  │
│  │  │ ├─ title                                   │   │  │
│  │  │ ├─ description                             │   │  │
│  │  │ ├─ assignee_id (FK→auth_user)            │   │  │
│  │  │ ├─ status                                  │   │  │
│  │  │ ├─ created_at                              │   │  │
│  │  │ ├─ updated_at                              │   │  │
│  │  │ └─ due_date                                │   │  │
│  │  └─────────────────────────────────────────────┘   │  │
│  │                                                      │  │
│  └──────────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────┘
```

---

## 🧩 Component Breakdown

### 1. **Web Interface Layer**

**Responsibility:** Render UI to user

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Templates** | Django Templates (Jinja-like) | HTML rendering |
| **Base Template** | `base.html` | Common layout (nav, footer) |
| **View Templates** | `login.html`, `dashboard.html`, `task_form.html`, `report.html` | Page-specific HTML |
| **Static Files** | CSS, JavaScript | Styling and interactivity |

**Key Files:**
```
templates/
├── base.html              # Navigation, footer inheritance
├── login.html             # Login form
├── dashboard.html         # Task kanban board (3 columns)
├── task_form.html         # Create/Edit form
└── report.html            # Sprint metrics display

static/
├── css/
│   └── style.css          # Professional styling
└── js/
    └── main.js            # Form validation, DOM manipulation
```

### 2. **Application Logic Layer**

**Responsibility:** Business logic, authentication, task management

| Component | Module | Responsibility |
|-----------|--------|-----------------|
| **Authentication Handling** | `auth_views` (Django built-in) | Login/logout sessions |
| **Task Views** | `tasks/views.py` | CRUD operations on tasks |
| **Access Control** | `login_required` decorator | Protect views |
| **Query Building** | `tasks/models.py` queries | Fetch filtered data |

**Key Functions:**
```python
# Authentication
auth_views.LoginView.as_view()
auth_views.LogoutView.as_view()

# Task Management
views.dashboard(request)           # List all user tasks
views.create_task(request)         # POST: Create task
views.update_task(request, pk)     # GET/POST: Edit task
views.delete_task(request, pk)     # POST: Delete task
views.change_status(request, pk, status)  # POST: Update status
views.weekly_report(request)       # GET: Generate report
```

### 3. **Data Access Layer (ORM)**

**Responsibility:** Database queries, transaction management

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Query Builder** | Django ORM | Pythonic SQL queries |
| **Migrations** | Django Migrations | Schema versioning |
| **Transactions** | Django Transactions | ACID compliance |
| **Indexing** | Django Indexes | Query optimization |

**Example ORM Usage:**
```python
# Query: Get all tasks for user
tasks = Task.objects.filter(assignee=request.user)

# Query: Get completed tasks this week
completed = Task.objects.filter(
    assignee=request.user,
    status='done',
    updated_at__gte=week_ago
).count()
```

### 4. **Database Layer**

**Responsibility:** Persistent data storage

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Database** | SQLite | File-based relational DB |
| **Tables** | Django schema | User, Task, Session tables |
| **Constraints** | FK, PK, NOT NULL | Data integrity |
| **Indices** | Database indices | Query performance |

---

## 🔄 Data Flow

### Use Case 1: User Creates Task

```
1. User clicks "Create Task" button on dashboard
   ↓
2. Browser displays task_form.html (GET /task/create/)
   ↓
3. User fills form:
   - Title: "Write API docs"
   - Description: "Document all endpoints"
   - Due Date: 2026-03-01
   (Assignee hidden/auto-set to current user)
   ↓
4. User clicks Submit
   ↓
5. Form POSTs to /task/create/
   ↓
6. Django calls create_task(request) view
   ↓
7. View extracts form data:
   title = request.POST['title']
   description = request.POST['description']
   assignee = request.user  # AUTO-ASSIGN
   ↓
8. ORM creates Task object:
   Task.objects.create(
       title=title,
       description=description,
       assignee=request.user,
       status='todo',
       created_at=timezone.now()  # Auto timestamp
   )
   ↓
9. Task record inserted into database
   ↓
10. View redirects to dashboard (GET /)
   ↓
11. Dashboard view fetches all user's tasks:
    Task.objects.filter(assignee=request.user)
   ↓
12. Templates renders 3 columns (todo, inprogress, done)
   ↓
13. New task appears in "Todo" column on dashboard
```

**Database State After Creation:**
```
tasks_task table:
┌─────┬────────────────────┬──────────────────────┬─────────────┬───────────┬──────────────┬──────────────┐
│ id  │ title              │ description          │ assignee_id │ status    │ created_at   │ updated_at   │
├─────┼────────────────────┼──────────────────────┼─────────────┼───────────┼──────────────┼──────────────┤
│ 1   │ Write API docs     │ Document all...      │ 5           │ todo      │ 2026-02-22   │ 2026-02-22   │
└─────┴────────────────────┴──────────────────────┴─────────────┴───────────┴──────────────┴──────────────┘
```

---

### Use Case 2: User Changes Task Status (Todo → In Progress)

```
1. User on dashboard sees task "Write API docs" in "Todo" column
   ↓
2. User clicks button "Move to In Progress"
   ↓
3. Button triggers POST /task/1/status/inprogress/
   ↓
4. Django calls change_status(request, pk=1, status='inprogress')
   ↓
5. View fetches task:
   task = get_object_or_404(Task, pk=1, assignee=request.user)
   ↓
6. View updates status:
   task.status = 'inprogress'
   task.save()  # Triggers updated_at auto-update
   ↓
7. Database updates task record:
   UPDATE tasks_task
   SET status = 'inprogress', updated_at = NOW()
   WHERE id = 1
   ↓
8. View redirects to dashboard
   ↓
9. Dashboard refreshes:
   - "Todo" column: 4 tasks (removed 1)
   - "In Progress" column: 3 tasks (added 1)
   - "Done" column: 8 tasks (unchanged)
```

---

### Use Case 3: User Views Weekly Report

```
1. User clicks "Weekly Report" link from dashboard
   ↓
2. Browser navigates to GET /report/
   ↓
3. Django calls weekly_report(request)
   ↓
4. View calculates time window:
   today = timezone.now()
   week_ago = today - timedelta(days=7)
   ↓
5. View queries tasks created this week:
   tasks = Task.objects.filter(
       assignee=request.user,
       created_at__gte=week_ago
   )
   ↓
6. View calculates metrics:
   total_tasks = tasks.count()  # e.g., 12
   completed = tasks.filter(status='done').count()  # e.g., 8
   completion_rate = (completed / total_tasks * 100)  # 67%
   ↓
7. View renders report.html with context:
   {
       'total': 12,
       'completed': 8,
       'completion_rate': 67,
       'week_start': '2026-02-15',
       'week_end': '2026-02-22'
   }
   ↓
8. Template displays metrics:
   Total Tasks Created: 12
   Tasks Completed: 8
   Completion Rate: 67% ████████░░
   ↓
9. User sees visual report on screen
```

---

## 💾 Database Schema

### Entity Relationship Diagram

```
┌────────────────────────────────┐
│        auth_user (Built-in)    │ ← Django User Model
├────────────────────────────────┤
│ id (PK)                        │
│ username                       │
│ email                          │
│ password (hashed)              │
│ first_name                     │
│ last_name                      │
│ is_active                      │
│ is_staff                       │
│ date_joined                    │
│ last_login                     │
└────────────────────────────────┘
            ↑ (1:N)
            │ is assignee
            │
┌────────────────────────────────┐
│       tasks_task (Custom)      │
├────────────────────────────────┤
│ id (PK)                        │
│ title (CharField, max=200)     │
│ description (TextField)        │
│ assignee_id (FK→auth_user)    │
│ status (Choice)                │
│   - 'todo'                     │
│   - 'inprogress'               │
│   - 'done'                     │
│ created_at (DateTimeField)     │
│ updated_at (DateTimeField)     │
│ due_date (DateField, nullable) │
└────────────────────────────────┘
```

### Task Table DDL (SQL)

```sql
CREATE TABLE tasks_task (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    assignee_id INTEGER NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'todo',
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL,
    due_date DATE,
    FOREIGN KEY (assignee_id) REFERENCES auth_user(id)
);

-- Indices for performance
CREATE INDEX idx_tasks_assignee ON tasks_task(assignee_id);
CREATE INDEX idx_tasks_created_at ON tasks_task(created_at);
CREATE INDEX idx_tasks_status ON tasks_task(status);
```

### Data Types Reference

| Model Field | Database Type | Purpose | Example |
|------------|--------------|---------|---------|
| `title` | VARCHAR(200) | Task name | "Fix login bug" |
| `description` | TEXT | Detailed info | "Users report... Fix by..." |
| `assignee_id` | INTEGER (FK) | Task owner | 5 (User ID) |
| `status` | VARCHAR(20) | Current state | "inprogress" |
| `created_at` | DATETIME | Creation time | "2026-02-22 10:30:00" |
| `updated_at` | DATETIME | Last edit | "2026-02-22 14:45:00" |
| `due_date` | DATE | Deadline | "2026-03-01" |

---

## 🔐 Authentication Flow

### Session-Based Authentication Architecture

```
┌─────────────────────────────────────────┐
│       Unauthenticated User              │
└─────────────────────────────────────────┘
          │
          │ GET /login/
          ↓
┌─────────────────────────────────────────┐
│  Django LoginView                       │
│  • Displays login form                  │
│  • Template: login.html                 │
└─────────────────────────────────────────┘
          │
          │ POST /login/ (username, password)
          ↓
┌─────────────────────────────────────────┐
│  Django Authentication Backend          │
│  • Query User table: WHERE username=X   │
│  • Hash input password                  │
│  • Compare with stored hash             │
│  • If match → Valid                     │
│  • If no match → Invalid                │
└─────────────────────────────────────────┘
          │ (if Valid)
          ↓
┌─────────────────────────────────────────┐
│  Session Creation                       │
│  • Generate session_id (unique token)   │
│  • Store in django_session table        │
│  • Set HTTP response cookie             │
│    Set-Cookie: sessionid=abc123xyz      │
└─────────────────────────────────────────┘
          │
          │ HTTP Redirect → dashboard
          ↓
┌─────────────────────────────────────────┐
│       Authenticated User Dashboard      │
│  • Browser sends sessionid cookie       │
│  • Django verifies cookie matches DB    │
│  • request.user = logged-in user        │
│  • Access granted ✅                    │
└─────────────────────────────────────────┘
          │
          │ All subsequent requests include
          │ sessionid cookie automatically
          ↓
┌─────────────────────────────────────────┐
│  @login_required Decorator              │
│  Checks: is request.user authenticated? │
│  • Yes → Execute view ✅                │
│  • No → Redirect to login ❌            │
└─────────────────────────────────────────┘
```

### Session Storage

```python
# Django automatically creates session record
# In database table: django_session

django_session table:
┌────────────────────────────┬────────────────────────────┬──────────────┐
│ session_key                │ session_data                │ expire_date  │
├────────────────────────────┼────────────────────────────┼──────────────┤
│ abc123xyz789...            │ {user_id: 5, ...}          │ 2026-02-23   │
└────────────────────────────┴────────────────────────────┴──────────────┘

# Session expires:
# - After 2 weeks of inactivity (configurable)
# - When user logs out manually
# - Browser session ends if cookie deleted
```

### Protected View Pattern

```python
from django.contrib.auth.decorators import login_required

@login_required  # Decorator checks authentication
def dashboard(request):
    # request.user = currently logged-in User object
    # request.user.id = 5
    # request.user.username = "john_doe"
    
    # Fetch only THIS user's tasks
    tasks = Task.objects.filter(assignee=request.user)
    return render(request, 'dashboard.html', {'tasks': tasks})

# Flow:
# 1. Unauthenticated user tries GET /
# 2. @login_required intercepts
# 3. Redirects to /login/
# 4. After login, redirected back to /
# 5. View executes with authenticated request.user
```

---

## 🛣️ API/View Structure

### URL Routing Map

```
config/urls.py:
  ├─ /admin/                           → Django admin panel
  ├─ /login/                           → auth_views.LoginView (built-in)
  ├─ /logout/                          → auth_views.LogoutView (built-in)
  └─ (prefix empty)                    → tasks.urls

tasks/urls.py:
  ├─ /                                 → views.dashboard [GET]
  ├─ /task/create/                     → views.create_task [GET, POST]
  ├─ /task/<id>/update/                → views.update_task [GET, POST]
  ├─ /task/<id>/delete/                → views.delete_task [POST]
  ├─ /task/<id>/status/<status>/       → views.change_status [POST]
  └─ /report/                          → views.weekly_report [GET]
```

### View Request/Response Flow

```python
# Example: Dashboard View

# Request: GET /
# Method: GET
# User: Authenticated (session cookie)
# Parameters: None

@login_required
def dashboard(request):
    # Extract user from request
    user = request.user ideally would be john_doe (User with id=5)
    
    # Query database
    todo_tasks = Task.objects.filter(assignee=user, status='todo')
    inprogress_tasks = Task.objects.filter(assignee=user, status='inprogress')
    done_tasks = Task.objects.filter(assignee=user, status='done')
    
    # Prepare context (data to pass to template)
    context = {
        'todo': todo_tasks,         # QuerySet of Task objects
        'inprogress': inprogress_tasks,
        'done': done_tasks,
        'user': user,               # Current user
        'total_tasks': todo_tasks.count() + inprogress_tasks.count() + done_tasks.count()
    }
    
    # Render template with context
    return render(request, 'dashboard.html', context)

# Response: HTML page with tasks grouped by status
# Headers: Content-Type: text/html; charset=utf-8
# Body: dashboard.html rendered with context data
```

---

## 🎯 Design Patterns

### 1. **Model-View-Template (MVT) Pattern**

Django's built-in MVC variant:

```
┌─────────────┐
│   Models    │ (tasks/models.py) - Data structure
│  (Task, ..) │
└──────┬──────┘
       │ defines
       ↓
┌─────────────┐          ┌──────────────────┐
│   Views     │ queries  │   Database       │
│ (business   │ ←------→ │   (SQLite)       │
│  logic)     │          │                  │
└──────┬──────┘          └──────────────────┘
       │
       │ renders
       ↓
┌──────────────────┐
│    Templates     │ (HTML with Django template syntax)
│ (dashboard.html) │
└──────────────────┘
       │
       │ returns
       ↓
┌──────────────────┐
│  User Browser    │
│  (displays HTML) │
└──────────────────┘
```

### 2. **Decorator Pattern (Authentication)**

```python
@login_required  # Decorator wraps view function
def dashboard(request):
    # Decorator intercepts request
    # Checks: is user authenticated?
    # If no → redirect to login
    # If yes → continue to view
    pass

# Equivalent to:
def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('login')
    # actual view logic
    pass
```

### 3. **ORM Query Builder Pattern**

```python
# Instead of writing raw SQL:
# SELECT * FROM tasks_task WHERE assignee_id=5 AND status='todo'

# Use Django ORM:
tasks = Task.objects.filter(
    assignee=request.user,
    status='todo'
)

# Benefits:
# ✅ Database agnostic (SQLite → PostgreSQL → MySQL easily)
# ✅ SQL injection prevention (automatic escaping)
# ✅ Readable Python code
# ✅ Type hints possible
```

### 4. **ManyToOne Relationship (Foreign Key)**

```python
# Database:
# User (1) ──→ (Many) Task
#
# Task has assignee (User)
# Multiple tasks can belong to one user

assignee = models.ForeignKey(
    User,                           # Related model
    on_delete=models.CASCADE,       # Delete tasks if user deleted
    related_name='tasks'            # Reverse relation: user.tasks.all()
)

# Usage:
user = User.objects.get(id=5)
user_tasks = user.tasks.all()  # All tasks assigned to user
# Equivalent to: Task.objects.filter(assignee=user)
```

### 5. **QuerySet Lazy Evaluation**

```python
# When you write:
tasks = Task.objects.filter(assignee=request.user)

# Django does NOT query database yet!
# QuerySet is lazy → evaluated only when needed

# Evaluation triggers:
tasks.count()           # Executes: SELECT COUNT(*) ...
for task in tasks:      # Executes: SELECT * ...
tasks.exists()          # Executes: SELECT 1 ...
str(tasks.query)        # Shows SQL (debugging)
```

---

## ⚡ Performance Considerations

### 1. **Database Indexing**

```python
# In models.py, add indices:

class Task(models.Model):
    # ... fields ...
    
    class Meta:
        indexes = [
            models.Index(fields=['assignee']),        # Fast filter by user
            models.Index(fields=['created_at']),      # Fast date range queries
            models.Index(fields=['status']),          # Fast status filtering
            models.Index(fields=['assignee', 'status']),  # Combined index
        ]
```

**Impact:**
- Without index: `SELECT * FROM tasks WHERE assignee_id=5` scans all rows
- With index: Database uses B-tree, finds rows in O(log n) time

### 2. **Query Optimization**

```python
# ❌ Bad - N+1 Problem:
tasks = Task.objects.all()
for task in tasks:
    print(task.assignee.username)  # Separate query for each task!
    # Generates 1000 queries for 1000 tasks

# ✅ Good - select_related (for ForeignKey):
tasks = Task.objects.select_related('assignee')  # Joins user table
for task in tasks:
    print(task.assignee.username)  # No additional queries!
    # Only 2 queries total

# ✅ Good - prefetch_related (for reverse relations):
users = User.objects.prefetch_related('tasks')
for user in users:
    for task in user.tasks.all():
        print(task.title)  # Optimized queries
```

### 3. **Pagination (v1.5+)**

```python
# Current (all tasks at once):
tasks = Task.objects.filter(assignee=request.user)

# Future improvement:
from django.core.paginator import Paginator

tasks = Task.objects.filter(assignee=request.user)
paginator = Paginator(tasks, 25)  # 25 tasks per page
page_number = request.GET.get('page')
page_obj = paginator.get_page(page_number)

# Only loads 25 tasks per page (not thousands)
```

### 4. **Caching (v1.5+)**

```python
# Cache weekly report calculation:
from django.views.decorators.cache import cache_page

@cache_page(60 * 5)  # Cache for 5 minutes
@login_required
def weekly_report(request):
    # Calculation runs once, result cached
    # Subsequent requests use cached data
    pass
```

---

## 🔒 Security Architecture

### 1. **CSRF Protection**

```html
<!-- In all POST forms: -->
<form method="POST">
    {% csrf_token %}  <!-- Django generates unique token -->
    <!-- token value different for each user/session -->
    <!-- Prevents Cross-Site Request Forgery attacks -->
    <input type="submit" value="Submit">
</form>
```

### 2. **SQL Injection Prevention**

```python
# ❌ Vulnerable (raw SQL):
query = f"SELECT * FROM tasks WHERE assignee_id={user_id}"

# ✅ Safe (Django ORM):
tasks = Task.objects.filter(assignee_id=user_id)
# Django escapes user_id automatically

# ✅ Safe (parameterized query):
from django.db import connection
cursor = connection.cursor()
cursor.execute("SELECT * FROM tasks WHERE assignee_id=%s", [user_id])
# Prevents SQL injection at database level
```

### 3. **XSS Prevention**

```html
<!-- ❌ Vulnerable: -->
<p>{{ task.description|safe }}</p>  <!-- Renders raw HTML if task.description contains <script> -->

<!-- ✅ Safe (default): -->
<p>{{ task.description }}</p>  <!-- Django auto-escapes: <script> becomes &lt;script&gt; -->

<!-- Result if description contains: "<script>alert('xss')</script>" -->
<!-- Rendered as: "&lt;script&gt;alert('xss')&lt;/script&gt;" (plain text) -->
```

### 4. **Password Hashing**

```python
# Django handles password security:

user = User.objects.create_user(
    username='john',
    password='mypassword'  # Automatically hashed with PBKDF2
)

# Database stores:
# password: "pbkdf2_sha256$260000$salt$hashedvalue"

# Verification:
if user.check_password('mypassword'):  # Rehashes input, compares
    print("Password valid")
else:
    print("Password incorrect")
```

### 5. **Data Access Control**

```python
@login_required
def update_task(request, pk):
    # Only allow user to edit their own task
    task = get_object_or_404(
        Task,
        pk=pk,
        assignee=request.user  # ← Security check
    )
    
    # If another user tries to access user_id=1's task with task_id=5:
    # get_object_or_404() returns 404 (Not Found)
    # User cannot modify other's tasks
```

---

## 🚀 Future Architecture (v2.0)

### Upgrade Path: 1-Tier → 2-Tier + Microservices

```
Version 1.0 (Current):
┌─────────────────────────────┐
│  Monolithic Django App      │
│  + SQLite (single file)     │
└─────────────────────────────┘

          ↓ (upgrades to)

Version 2.0 (Planned):
┌─────────────────────────────┐
│   Frontend Layer            │
│ (React/Vue SPA)             │
└─────────────────────────────┘
          ↓ REST API
┌─────────────────────────────┐
│  API Gateway                │
│ (Kong/Nginx)                │
└─────────────────────────────┘
          ↓
┌──────────────────────────────────────────────────┐
│          Microservices Layer                     │
├──────────────────────────────────────────────────┤
│ ┌──────────────┐  ┌──────────────┐              │
│ │ Auth Service │  │ Task Service │              │
│ │ (Django JWT) │  │ (Django REST)│              │
│ └──────────────┘  └──────────────┘              │
│ ┌──────────────┐  ┌──────────────┐              │
│ │ Report Svc   │  │ Automation   │              │
│ │ (BI/Analytics)│  │ (Celery)     │              │
│ └──────────────┘  └──────────────┘              │
└──────────────────────────────────────────────────┘
          ↓ Database per service
┌──────────────────────────────────────────────────┐
│          Database Layer                         │
├──────────────────────────────────────────────────┤
│ ┌──────────────┐  ┌──────────────┐              │
│ │ PostgreSQL   │  │ MongoDB      │              │
│ │ (relational) │  │ (tasks data) │              │
│ └──────────────┘  └──────────────┘              │
│ ┌──────────────────────────────────┐            │
│ │ Redis Cache Layer                │            │
│ └──────────────────────────────────┘            │
└──────────────────────────────────────────────────┘
          ↓ Message Queue
┌──────────────────────────────────────────────────┐
│ Celery + RabbitMQ (Background Tasks)             │
└──────────────────────────────────────────────────┘
```

### Planned v2.0 Enhancements

| Improvement | Current (v1.0) | v2.0 | Benefit |
|------------|---------------|----|---------|
| **Frontend** | Django Templates | React/Vue SPA | Faster UX |
| **Database** | SQLite | PostgreSQL | Reliability |
| **API Style** | Server-side rendered | RESTful + GraphQL | Mobile ready |
| **Authentication** | Sessions | JWT tokens | Scalable |
| **Caching** | In-memory | Redis | Performance |
| **Task Automation** | Synchronous | Celery queue | Async processing |
| **Scalability** | Single server | Kubernetes | Multi-region |
| **Logging** | File-based | ELK stack | Monitoring |
| **Reports** | On-demand calc | Data warehouse | Real-time BI |

---

## 📌 Summary

**Team Task Manager v1.0** uses a **1-Tier Monolithic Architecture**:

✅ **Advantages:**
- Simple to build and deploy
- Fast development cycle
- Easy to debug
- Suitable for small teams
- Great learning foundation

⚠️ **Limitations:**
- Not for production scale (>10k users)
- Single point of failure
- Can't scale individual components
- Deployment requires downtime

🎯 **Perfect for:**
- MVP phase
- Learning Django
- Small team workflows
- Resume projects

**Next Steps (v2.0):**
- Separate frontend (React) + backend (Django REST)
- Microservices architecture
- PostgreSQL + Redis
- Horizontal scaling
- Real-time WebSockets
- Advanced analytics

---

**Document Created:** February 22, 2026  
**Last Updated:** February 22, 2026  
**Maintainer:** Development Team
