from django.urls import path
from . import views


urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('create/', views.create_task, name='create_task'),
    path('task/<int:pk>/<str:new_status>/', views.change_status, name='change_status'),
    path('report/', views.weekly_report, name='weekly_report'),
    path('task/<int:pk>/update/', views.update_task, name='update_task'),
    path('task/<int:pk>/delete/', views.delete_task, name='delete_task'),
]