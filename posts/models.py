from uuid import uuid4

from django.db import models

# Create your models here.

class Post(models.Model):
  id = models.UUIDField(default= uuid4(), primary_key=True, unique=True, editable=True)
  title = models.CharField(max_length=500)
  image = models.URLField(max_length=512)
  body = models.TextField()
  created = models.DateTimeField(auto_now_add=True)

  def __str__(self) -> str:
    return str(self.title)