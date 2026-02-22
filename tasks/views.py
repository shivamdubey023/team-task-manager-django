from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Task
from .forms import TaskForm
from django.utils import timezone
from datetime import timedelta

@login_required
def weekly_report(request):

    today = timezone.now()
    week_ago = today - timedelta(days=7)

    created_this_week = Task.objects.filter(
        assignee=request.user,
        created_at__gte=week_ago
    ).count()

    completed_this_week = Task.objects.filter(
        assignee=request.user,
        status='done',
        updated_at__gte=week_ago
    ).count()

    completion_rate = 0
    if created_this_week > 0:
        completion_rate = (completed_this_week / created_this_week) * 100

    context = {
        'created_this_week': created_this_week,
        'completed_this_week': completed_this_week,
        'completion_rate': round(completion_rate, 2)
    }

    return render(request, 'report.html', context)

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


@login_required
def change_status(request, pk, new_status):
    
    task = get_object_or_404(Task, pk=pk, assignee=request.user)
    
    allowed_status = [ 'todo', 'in_progress', 'done' ]
    
    if new_status in allowed_status:
        task.status = new_status
        task.save()
        
    return redirect('dashboard')


@login_required
def update_task(request, pk):
    task = get_object_or_404(Task, pk=pk, assignee=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = TaskForm(instance=task)
    return render(request, 'create_task.html', {'form': form})


@login_required
def delete_task(request, pk):
    task = get_object_or_404(Task, pk=pk, assignee=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('dashboard')
    return render(request, 'confirm_delete.html', {'task': task})


