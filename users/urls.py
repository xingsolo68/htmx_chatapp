"""
URL configuration for htmx_chatapp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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

from django.urls import path

from users import views

app_name = "users"

urlpatterns = [
    path("", views.detail_view, name="profile"),
    path("edit/", views.edit_view, name="edit"),
    path("delete/", views.delete_view, name="delete"),
    path("onboarding/", views.edit_view, name="onboarding"),
    path("<str:username>/", views.detail_view, name="profile"),
]
