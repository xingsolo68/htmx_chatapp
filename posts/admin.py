from django.contrib import admin

from .models import Comment, LikePost, Post, Reply, Tag

# Register your models here.
admin.site.register(Post)
admin.site.register(Tag)
admin.site.register(Comment)
admin.site.register(Reply)
admin.site.register(LikePost)
