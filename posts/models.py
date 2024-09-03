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
    likes = models.ManyToManyField(User, related_name="like_posts", through="LikePost")

    def __str__(self) -> str:
        return str(self.title)

    class Meta:
        ordering = ["-created"]


class LikePost(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.user.username} liked {self.post.title}"


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

    likes = models.ManyToManyField(
        User, related_name="like_comments", through="LikeComment"
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Comment by {self.author.username if self.author.username else 'no author'} on {self.post.title}"


class LikeComment(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} liked {self.comment.content}"


class Reply(models.Model):
    comment = models.ForeignKey(
        Comment, on_delete=models.CASCADE, related_name="replies"
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="replies")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    likes = models.ManyToManyField(
        User, related_name="like_replies", through="LikeReply"
    )

    def __str__(self):
        return f"Reply by {self.author.username if self.author.username else 'no author'} on {self.comment.post.title}"


class LikeReply(models.Model):
    reply = models.ForeignKey(Reply, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
