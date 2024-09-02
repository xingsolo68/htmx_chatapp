from uuid import uuid4

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
