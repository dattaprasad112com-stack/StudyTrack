"""
URL configuration for studytrack project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from planner import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.home, name='home'),

    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),

    path('subjects/', views.subjects, name='subjects'),
    path('add-subject/', views.add_subject, name='add_subject'),
    path('edit-subject/<int:id>/', views.edit_subject, name='edit_subject'),
    path('delete-subject/<int:id>/', views.delete_subject, name='delete_subject'),
    path('schedule/', views.schedule_list, name='schedule'),
    path('add-schedule/', views.add_schedule, name='add_schedule'),
    path('tasks/', views.task_list, name='tasks'),
    path('add-task/', views.add_task, name='add_task'),
    path('complete-task/<int:id>/', views.complete_task, name='complete_task'),
    path('delete-task/<int:id>/', views.delete_task, name='delete_task'),
    path('progress/', views.progress_report, name='progress'),
    path('study-hours/', views.study_hours, name='study_hours'),
    path('add-study-session/', views.add_study_session, name='add_study_session'),
    path('settings/', views.account_settings, name='settings'),
]
