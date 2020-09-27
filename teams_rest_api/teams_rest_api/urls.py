"""teams_rest_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.contrib.auth import views as auth_views
from django.urls import path

from projects.views import (
    ProjectDetailView,
    ProjectCreateView,
    ProjectUpdateView,
    ProjectDeleteView,
    ProjectListView,
)

from tasks.views import (
    TaskListView,
    TaskCreateView,
    change_priority,
)

from users.views import CustomLoginView


urlpatterns = [
    path(
        'admin/',
        admin.site.urls,
    ),
    # user authentication views
    path(
        'login/',
        CustomLoginView.as_view(),
        name='login'
    ),
    path(
        'logout/',
        auth_views.LogoutView.as_view(),
        name='logout'
    ),
    # projects
    path(
        'projects/',
        ProjectListView.as_view(),
        name='project-list-view',
    ),
    path(
        'project/create/',
        ProjectCreateView.as_view(),
        name='project-create-view',
    ),
    path(
        'project/<int:pk>/delete/',
        ProjectDeleteView.as_view(),
        name='project-delete-view',
    ),
    path(
        'project/<int:pk>/update/',
        ProjectUpdateView.as_view(),
        name='project-update-view',
    ),
    path(
        'project/<int:pk>/',
        ProjectDetailView.as_view(),
        name='project-detail-view',
    ),
    # project-tasks views
    path(
        'project/<int:pk>/tasks/',
        TaskListView.as_view(),
        name='project-tasks-list-view',
    ),
    path(
        'project/<int:pk>/task/create/',
        TaskCreateView.as_view(),
        name='task-create-view',
    ),
    path(
        'task/<int:pk>/change_priority/',
        change_priority,
        name='task-change-priority',
    ),
]
