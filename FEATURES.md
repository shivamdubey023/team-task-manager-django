# FEATURES.md – Team Task Manager Feature Specification

**Version:** 1.0 (1-Tier Architecture)  
**Date:** February 22, 2026  
**Status:** Feature Specification Document

---

## 📑 Table of Contents

1. [Feature Overview](#feature-overview)
2. [Authentication System](#authentication-system)
3. [Task System](#task-system)
4. [Task Workflow](#task-workflow)
5. [Automation](#automation)
6. [Sprint Reports](#sprint-reports)
7. [User Interface](#user-interface)
8. [Constraints & Limitations](#constraints--limitations)

---

## 🎯 Feature Overview

### Feature Scope (MVP – Minimum Viable Product)

| Feature | Priority | Status | v1.0 |
|---------|----------|--------|------|
| User Authentication | Critical | Planned | ✅ |
| Task Creation | Critical | Planned | ✅ |
| Task Assignment | Critical | Planned | ✅ |
| Task Status Management | Critical | Planned | ✅ |
| Weekly Sprint Report | High | Planned | ✅ |
| Task Automation | Medium | Planned | ✅ |
| Task Deletion | High | Planned | ✅ |
| Task Editing | High | Planned | ✅ |
| User Dashboard | Critical | Planned | ✅ |
| Admin Panel | Medium | Planned | ✅ |

---

## 🔐 Authentication System

### 1.1 User Login

**Feature ID:** AUTH-001  
**Priority:** Critical

#### Functional Requirements
- Users can log in using username/email and password
- Invalid credentials show error message
- Successful login creates session
- Redirects to dashboard after login
- Session expires after inactivity (30 minutes – configurable)

#### User Flow
```
User → Login Page → Enter Credentials → Django validates → 
Create Session → Redirect to Dashboard
```

#### Technical Details
- **View:** `auth_views.LoginView`
- **Template:** `login.html`
- **Auth Method:** Django session-based authentication
- **Redirect:** `LOGIN_REDIRECT_URL = 'dashboard'`

#### Acceptance Criteria
- ✅ Login form displays username and password fields
- ✅ Submit shows error if credentials invalid
- ✅ Success redirects to dashboard
- ✅ Session stored in database
- ✅ User profile displayed in dashboard header

---

### 1.2 User Logout

**Feature ID:** AUTH-002  
**Priority:** Critical

#### Functional Requirements
- Users can log out from any page
- Session destroyed after logout
- Redirects to login page
- "Logout" button visible in dashboard

#### User Flow
```
Logged-in User → Click Logout → Session Destroyed → 
Redirect to Login Page
```

#### Technical Details
- **View:** `auth_views.LogoutView`
- **Redirect:** `LOGOUT_REDIRECT_URL = 'login'`
- **Decorator:** `@login_required` on protected views

#### Acceptance Criteria
- ✅ Logout button present on dashboard
- ✅ Session cookie removed after logout
- ✅ Redirects to login page
- ✅ User cannot access dashboard without new login

---

### 1.3 Session Management

**Feature ID:** AUTH-003  
**Priority:** High

#### Functional Requirements
- Unauthenticated users redirected to login
- All protected views require `@login_required` decorator
- User can only view/modify own tasks
- Admin can view all tasks (Django admin)

#### Acceptance Criteria
- ✅ Direct access to `/` redirects to login if not authenticated
- ✅ Direct access to dashboard without login shows login page
- ✅ User A cannot view User B's tasks
- ✅ All views properly decorated with `@login_required`

---

## 📝 Task System

### 2.1 Create Task

**Feature ID:** TASK-001  
**Priority:** Critical

#### Functional Requirements
- Users can create task with title and description
- Assignee field defaults to current user (auto-assign)
- Due date is optional
- Task status defaults to "todo"
- System generates created_at timestamp automatically
- User redirected to dashboard after creation

#### Task Creation Form Fields
| Field | Type | Required | Default | Validation |
|-------|------|----------|---------|-----------|
| title | CharField | Yes | None | Max 200 chars |
| description | TextField | No | Empty | Max 5000 chars |
| due_date | DateField | No | None | Future date only |
| assignee | ForeignKey | No | Current User | Must be valid User |

#### User Flow
```
Dashboard → Click "Create Task" → Fill Form → Submit → 
Task Created with Status="todo" → Redirect to Dashboard
```

#### Technical Details
- **View:** `create_task(request)`
- **Template:** `task_form.html`
- **Method:** POST
- **Auto-assignment:** `assignee=request.user`

#### Acceptance Criteria
- ✅ Create task form displays correctly
- ✅ Title field is mandatory
- ✅ Description field is optional
- ✅ Due date field accepts date input
- ✅ Assignee defaults to logged-in user
- ✅ Task created in database
- ✅ User redirected to dashboard
- ✅ New task visible in "Todo" column

---

### 2.2 View Tasks

**Feature ID:** TASK-002  
**Priority:** Critical

#### Functional Requirements
- Dashboard displays all user's tasks
- Tasks grouped by status (Todo, In Progress, Done)
- Each task shows: title, description, assignee, due date
- Total task count displayed
- Completed task count displayed

#### Dashboard View Layout
```
┌─────────────────────────────────────────┐
│  Welcome, [Username]                    │
├─────────────────────────────────────────┤
│  Total Tasks: 15  │  Completed: 8      │
├─────────────────────────────────────────┤
│   Todo (5)    │  In Progress (2)  │ Done (8) │
│  ┌─────────┐  │  ┌──────────────┐ │ ┌──────┐ │
│  │ Task 1  │  │  │ Task 2       │ │ │Task 3│ │
│  │ Task 4  │  │  └──────────────┘ │ │Task 5│ │
│  └─────────┘  │                    │ └──────┘ │
└─────────────────────────────────────────┘
```

#### User Flow
```
Login → Dashboard Loads → Display User's Tasks Grouped by Status
```

#### Technical Details
- **View:** `dashboard(request)`
- **Query:** `Task.objects.filter(assignee=request.user)`
- **Template:** `dashboard.html`
- **Grouping:** Filter by `status` field

#### Acceptance Criteria
- ✅ Dashboard loads for authenticated user
- ✅ Only user's tasks displayed
- ✅ Tasks grouped by status (3 columns)
- ✅ Task details visible (title, description)
- ✅ Task count stats shown
- ✅ No tasks visible for other users

---

### 2.3 Update Task

**Feature ID:** TASK-003  
**Priority:** High

#### Functional Requirements
- Users can edit task title, description, due date
- Assignee can be changed (optional – for team collaboration)
- Only task owner can edit their own tasks
- Updated timestamp auto-generated
- Redirects to dashboard after update

#### Editable Fields
| Field | Can Edit | If Already Assigned? |
|-------|----------|---------------------|
| title | Yes | Yes |
| description | Yes | Yes |
| due_date | Yes | Yes |
| assignee | Yes | Yes (reassign to another user) |
| status | No | Other feature handles this |

#### User Flow
```
Dashboard → Click Edit Task → Modify Fields → Submit → 
Task Updated → Redirect to Dashboard
```

#### Technical Details
- **View:** `update_task(request, pk)`
- **Template:** `task_form.html` (reused)
- **Method:** GET (display) / POST (submit)
- **Query Check:** `get_object_or_404(Task, pk=pk, assignee=request.user)`

#### Acceptance Criteria
- ✅ Edit button visible on each task
- ✅ Form pre-fills existing task data
- ✅ User can modify title, description, due date
- ✅ User gets confirmation message
- ✅ Updated task reflected on dashboard
- ✅ Only owner can edit their task
- ✅ updated_at timestamp changes

---

### 2.4 Delete Task

**Feature ID:** TASK-004  
**Priority:** High

#### Functional Requirements
- Users can delete their own tasks
- Confirmation dialog before deletion
- Only task owner can delete
- Deleted tasks removed from database permanently
- Redirect to dashboard after deletion

#### User Flow
```
Dashboard → Click Delete → Confirm Deletion → Task Removed → 
Updated Dashboard Shown
```

#### Technical Details
- **View:** `delete_task(request, pk)`
- **Method:** POST (with CSRF protection)
- **Query Check:** `get_object_or_404(Task, pk=pk, assignee=request.user)`
- **Template:** `task_confirm_delete.html` (optional)

#### Acceptance Criteria
- ✅ Delete button visible on each task
- ✅ Confirmation dialog appears before deletion
- ✅ Task removed from database if confirmed
- ✅ Dashboard refreshes without deleted task
- ✅ Only owner can delete their task
- ✅ Cannot delete other user's task

---

## 🔄 Task Workflow – Status Management

### 3.1 Task Status States

**Feature ID:** WORKFLOW-001  
**Priority:** Critical

#### Status Definitions

| Status | Code | Description | Next States |
|--------|------|-------------|------------|
| **Todo** | `todo` | Task created, not started | In Progress |
| **In Progress** | `inprogress` | Work actively being done | Done |
| **Done** | `done` | Task completed | Todo (if recurring) |

#### State Transition Diagram
```
    ┌─────────────┐
    │    Todo     │
    └──────┬──────┘
           │
           ↓
    ┌─────────────┐
    │ In Progress │
    └──────┬──────┘
           │
           ↓
    ┌─────────────┐
    │    Done     │
    └─────────────┘
```

---

### 3.2 Change Task Status

**Feature ID:** WORKFLOW-002  
**Priority:** Critical

#### Functional Requirements
- Users can move tasks between statuses via buttons
- Status change is immediate (no form submission)
- Only task owner can change task status
- Status transition is one-way (Todo → In Progress → Done)
- System logs when status changed (updated_at)

#### User Flow
```
Dashboard (Task in Todo) → Click "Move to In Progress" → 
Status Changes → Dashboard Refreshes → Task Now in "In Progress"
```

#### Technical Details
- **View:** `change_status(request, pk, status)`
- **Method:** POST (AJAX-friendly)
- **URL Pattern:** `/task/<pk>/status/<status>/`
- **Status Values:** `todo`, `inprogress`, `done`
- **Query Check:** `get_object_or_404(Task, pk=pk, assignee=request.user)`

#### Button Implementation (Dashboard)
```
Todo Column:
  ├─ Task Title
  └─ [Move to In Progress] button

In Progress Column:
  ├─ Task Title
  └─ [Move to Done] button

Done Column:
  ├─ Task Title
  └─ [Completed] (badge)
```

#### Acceptance Criteria
- ✅ "Move to In Progress" button visible on Todo tasks
- ✅ "Move to Done" button visible on In Progress tasks
- ✅ Status updates immediately without page reload
- ✅ Task appears in correct column after status change
- ✅ Only owner can change their task status
- ✅ updated_at field auto-updates
- ✅ Cannot move Done task back to Todo (unless automation triggers)

---

## 🤖 Automation

### 4.1 Auto-Assign Task to Creator

**Feature ID:** AUTO-001  
**Priority:** Critical

#### Functional Requirements
- When user creates a task, it's automatically assigned to the creator
- No UI selection required for self-assignment
- Assignee field not visible in creation form (fixed to current user)
- Can reassign to another user after creation via edit form

#### Implementation
```python
Task.objects.create(
    title=title,
    description=description,
    assignee=request.user,  # Always current user
    status='todo'
)
```

#### Acceptance Criteria
- ✅ Task automatically assigned to creator
- ✅ Creator sees task in their dashboard immediately
- ✅ Task assignee field shows creator's name
- ✅ Task can be reassigned to other users via edit

---

### 4.2 Auto-Create Recurring Weekly Task (Optional v1.0)

**Feature ID:** AUTO-002  
**Priority:** Medium

#### Functional Requirements
- When task marked as "done", system can create recurring task for next week
- Configurable per task (checkbox: "Repeat Weekly")
- New task created with same title, description, assignee
- Original task remains in "done" status
- Recurring task created at configured time (e.g., Monday 9 AM)

#### Configuration
```python
# In settings.py
AUTOMATION_ENABLED = True
RECURRING_TASK_DAY = 'MONDAY'  # Next week creation
RECURRING_TASK_TIME = '09:00'  # 9 AM
```

#### User Flow
```
Task Status Changed to Done → Check if "Repeat Weekly" → 
If Yes, Create New Task for Next Week → Creator Notified (future feature)
```

#### Acceptance Criteria
- ✅ "Repeat Weekly" checkbox optional on task form
- ✅ When enabled, recurring task created 7 days later
- ✅ Recurring task has same title and description
- ✅ Recurring task assigned to same user
- ✅ Recurring task starts in "Todo" status
- ✅ Both tasks appear in weekly report

---

## 📊 Sprint Reports

### 5.1 Weekly Sprint Report

**Feature ID:** REPORT-001  
**Priority:** High

#### Functional Requirements
- Report shows past 7 days of task activity
- Report displays for current logged-in user only
- Shows metrics: total tasks created, completed, completion percentage
- Report generated on-demand (no pre-generation)
- Time period: Last 7 days from today

#### Report Metrics

| Metric | Definition | Calculation |
|--------|-----------|------------|
| **Total Tasks Created** | Count of tasks created in last 7 days | `Task.objects.filter(created_at__gte=week_ago).count()` |
| **Tasks Completed** | Count of tasks marked as "done" in last 7 days | `Task.objects.filter(status='done', updated_at__gte=week_ago).count()` |
| **Completion Rate %** | Percentage of created tasks completed | `(completed / total) * 100` |
| **Pending Tasks** | Tasks still in Todo or In Progress | `total - completed` |

#### Report Display Layout
```
┌──────────────────────────────────┐
│  WEEKLY SPRINT REPORT            │
│  Week of: Feb 15 - Feb 22, 2026  │
├──────────────────────────────────┤
│  Total Tasks Created:      12    │
│  Tasks Completed:          8     │
│  Completion Rate:          67%   │
│  Pending Tasks:            4     │
├──────────────────────────────────┤
│  Performance Trend:              │
│  ████████░░░░  67% Complete     │
└──────────────────────────────────┘
```

#### User Flow
```
Dashboard → Click "View Report" → Weekly Report Page → 
Displays Metrics → User Can Navigate Back to Dashboard
```

#### Technical Details
- **View:** `weekly_report(request)`
- **Template:** `report.html`
- **Method:** GET
- **Time Calculation:** `today = timezone.now()` → `week_ago = today - timedelta(days=7)`
- **Query:** `Task.objects.filter(assignee=request.user, created_at__gte=week_ago)`

#### Acceptance Criteria
- ✅ Report page accessible from dashboard
- ✅ Shows correct date range (last 7 days)
- ✅ Total tasks count accurate
- ✅ Completed tasks count accurate
- ✅ Completion percentage calculated correctly
- ✅ Only user's data shown (no other user's data visible)
- ✅ Report updates daily with current data
- ✅ Progress bar visual representation

---

## 🎨 User Interface

### 6.1 Templates Required

| Template | Purpose | Route | Status |
|----------|---------|-------|--------|
| `login.html` | User authentication | `/login/` | Planned |
| `dashboard.html` | Task management (main) | `/` | Planned |
| `task_form.html` | Create/Edit tasks | `/task/create/`, `/task/<id>/update/` | Planned |
| `report.html` | Weekly sprint report | `/report/` | Planned |
| `base.html` | Template inheritance | All pages | Planned |

### 6.2 Design Principles

- ✅ Clean, professional layout
- ✅ Responsive (works on desktop, tablet, mobile)
- ✅ Consistent navigation header/footer
- ✅ Color-coded task statuses (visual clarity)
- ✅ Accessible (WCAG 2.1 guidelines)
- ✅ Bootstrap 5 compatible
- ✅ No dark UI (professional business appearance)

### 6.3 Navigation Structure

```
Header (All Pages):
├─ Logo / Project Name (left)
├─ Navigation Links (center)
│  ├─ Dashboard
│  ├─ My Tasks
│  └─ Weekly Report
└─ User Menu (right)
   ├─ [Username] dropdown
   ├─ Profile (future)
   └─ Logout

Footer (All Pages):
├─ © 2026 Team Task Manager
├─ Quick Links
└─ Support
```

---

## ⚠️ Constraints & Limitations

### 6.1 1-Tier Architecture Limitations

| Limitation | Reason | Future Solution (v2.0) |
|------------|--------|----------------------|
| SQLite only | Single server, no distributed access | PostgreSQL cloud DB |
| No real-time updates | Session-based refresh | WebSockets/SignalR |
| Basic reporting | Manual query-based | BI dashboard tools |
| Single server instance | No high availability | Load balancing |
| No task comments | Scope creep for MVP | Comment system |
| No file attachments | Storage complexity | Cloud storage integration |

### 6.2 Scalability Notes

- **Current Limit:** ~1,000 concurrent users
- **Task Volume:** Supports 100,000+ tasks before optimization needed
- **Database:** SQLite fine for single instance, upgrade to PostgreSQL at v2.0

### 6.3 Security Considerations (v1.0)

- ✅ CSRF protection enabled
- ✅ SQL injection prevented (Django ORM)
- ✅ XSS prevention (template auto-escaping)
- ⚠️ HTTPS (required for production)
- ⚠️ Rate limiting (future feature)
- ⚠️ Two-factor authentication (future feature)

---

## 📋 Feature Completion Checklist

- [ ] Authentication system (login/logout)
- [ ] Task creation and auto-assignment
- [ ] Task editing and deletion
- [ ] Task status management (workflow)
- [ ] Dashboard with task grouping
- [ ] Weekly sprint report
- [ ] HTML templates
- [ ] CSS styling (professional)
- [ ] Admin panel access
- [ ] Testing suite
- [ ] Documentation complete
- [ ] Code deployed and verified

---

**Version History:**
- v1.0 – Initial feature specification (Feb 22, 2026)

**Next Review:** Before development begins
