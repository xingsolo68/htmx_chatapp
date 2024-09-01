# Generated by Django 5.1 on 2024-08-31 07:11

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Post",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.UUID("f52d9e62-3050-43db-a954-8c5df2f231c2"),
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("title", models.CharField(max_length=255)),
                ("image", models.URLField()),
                ("body", models.CharField(max_length=255)),
                ("created", models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
