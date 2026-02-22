from django.db import models
from django.contrib.auth.models import User


class Task(models.Model):
    
    STATUS_CHOICES = [
        ('todo', 'To Do'),
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
    ]
    
    
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    assignee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assigned_tasks')
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='todo')
    
    due_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title