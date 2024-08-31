from uuid import uuid4

from django.db import models

# Create your models here.

class Post(models.Model):
  id = models.UUIDField(default= uuid4(), primary_key=True)
  title = models.CharField(max_length=255)
  image = models.URLField()
  body = models.CharField(max_length=255)
  created = models.DateTimeField(auto_now_add=True)