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
# from django.contrib.auth import views as auth_views
from django.urls import path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from projects.views import (
    ProjectDetailView,
    ProjectCreateView,
    ProjectListView,
    TaskListView,
    TaskCreateView,
    TaskDetailView,
)

from users.views import (
    UserRegistrationView,
)

# from users.views import CustomLoginView


urlpatterns = [
    path(
        'admin/',
        admin.site.urls,
    ),
    # user authentication views
    # path(
    #     'logout/',
    #     auth_views.LogoutView.as_view(),
    #     name='logout'
    #),
    # jwt views
    path(
        'api/token/',
        TokenObtainPairView.as_view(),
        name='token-obtain-view',
    ),
    path(
        'api/token/refresh/',
        TokenRefreshView.as_view(),
        name='token-refresh-view',
    ),
    # user views
    path(
        'api/users/signup/',
        UserRegistrationView.as_view(),
        name='user-registration-view',
    ),
    # projects
    path(
        'api/projects/',
        ProjectListView.as_view(),
        name='project-list-view',
    ),
    path(
        'api/projects/<int:project_id>/',
        ProjectDetailView.as_view(),
        name='project-detail-view',
    ),
    path(
        'api/projects/new/',
        ProjectCreateView.as_view(),
        name='project-create-view',
    ),
    # project-tasks views
    path(
        'api/projects/<int:project_id>/tasks/',
        TaskListView.as_view(),
        name='project-tasks-list-view',
    ),
    path(
        'api/projects/<int:project_id>/tasks/new/',
        TaskCreateView.as_view(),
        name='task-create-view',
    ),
    path(
        'api/projects/<int:project_id>/tasks/<int:task_id>/',
        TaskDetailView.as_view(),
        name='project-tasks-detail-view',
    ),
]
