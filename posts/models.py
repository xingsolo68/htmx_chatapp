from uuid import uuid4

from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Post(models.Model):
    id = models.UUIDField(default=uuid4, primary_key=True, unique=True, editable=True)
    artist = models.CharField(max_length=500, null=True)
    title = models.CharField(max_length=500)
    image = models.URLField(max_length=512)
    url = models.URLField(max_length=512, null=True)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    tags = models.ManyToManyField("Tag", blank=True)
    author = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="posts"
    )

    def __str__(self) -> str:
        return str(self.title)

    class Meta:
        ordering = ["-created"]


class Tag(models.Model):
    name = models.CharField(max_length=20)
    slug = models.SlugField(max_length=20, unique=True)
    image = models.FileField(upload_to="icons/", null=True, blank=True)
    order = models.IntegerField(null=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ["order"]


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Comment by {self.author.username if self.author.username else 'no author'} on {self.post.title}"


class Reply(models.Model):
    comment = models.ForeignKey(
        Comment, on_delete=models.CASCADE, related_name="replies"
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="replies")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reply by {self.author.username if self.author.username else 'no author'} on {self.comment.post.title}"
