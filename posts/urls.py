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
from django.urls import path

from posts import views

app_name = "posts"

urlpatterns = [
    path("category/<slug:tag_slug>", views.home_view, name="category"),
    path("create/", views.post_create_view, name="create"),
    path(
        "comment/<str:comment_id>/delete/", views.comment_delete, name="comment_delete"
    ),
    path("reply/<str:reply_id>/delete/", views.reply_delete, name="reply_delete"),
    path("post/<uuid:pk>/like", views.like_post, name="like_post"),
    path("comment/<pk>/like", views.like_comment, name="like_comment"),
    path("reply/<pk>/like", views.like_reply, name="like_reply"),
    path("comment/<str:post_id>/", views.comment_sent, name="comment_sent"),
    path("reply/<str:comment_id>/", views.reply_sent, name="reply_sent"),
    path("<uuid:post_id>/delete/", views.post_delete_view, name="delete"),
    path("<uuid:post_id>/edit/", views.post_edit_view, name="edit"),
    path("<pk>/", views.post_page_view, name="detail"),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
