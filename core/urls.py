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

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from posts import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.home_view, name="home"),
    path("posts/category/<slug:tag_slug>", views.home_view, name="post_category"),
    path("posts/create/", views.post_create_view, name="post_create"),
    path("posts/<uuid:post_id>/delete/", views.post_delete_view, name="post_delete"),
    path("posts/<uuid:post_id>/edit/", views.post_edit_view, name="post_edit"),
    path("posts/<uuid:post_id>/", views.post_page_view, name="post"),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
