from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Task
from .forms import TaskForm


@login_required
def dashboard(request):
    tasks = Task.objects.filter(assignee=request.user)
    
    todo_tasks = tasks.filter(status='todo')
    inprogress_tasks = tasks.filter(status='in_progress')
    done_tasks = tasks.filter(status='done')
    
    context = {
        'todo_tasks': todo_tasks,
        'inprogress_tasks': inprogress_tasks,
        'done_tasks': done_tasks,
    }
    
    return render(request, 'dashboard.html', context)

@login_required
def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.assignee = request.user
            task.save()
            return redirect('dashboard')
    else:
        form = TaskForm()
        
    return render(request, 'create_task.html', {'form': form})

