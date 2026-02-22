from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views 


urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Authentication URLs
    
    # Login and Logout
    
    # Login view
    path('login/', auth_views.LoginView.as_view(
        template_name = 'login.html'
    ), name='login'),
    
    # Logout view
    path('logout/', auth_views.LogoutView.as_view(
        template_name = 'logout.html'
    ), name='logout'),
    
    # App Urls
    path('', include('tasks.urls')),
]
