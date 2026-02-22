from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Task

@login_required
def dashboard(request):
    tasks = Task.objects.filter(assignee=request.user)
    
    todo_tasks = tasks.filter(status='todo')
    inprogress_tasks = tasks.filter(status='inprogress')
    done_tasks = tasks.filter(status='done')
    
    context = {
        'todo_tasks': todo_tasks,
        'inprogress_tasks': inprogress_tasks,
        'done_tasks': done_tasks,
    }
    
    return render(request, 'dashboard.html', context)

