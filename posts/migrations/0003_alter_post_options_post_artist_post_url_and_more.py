# Generated by Django 5.1 on 2024-08-31 11:51

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("posts", "0002_alter_post_body_alter_post_id_alter_post_image_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="post",
            options={"ordering": ["-created"]},
        ),
        migrations.AddField(
            model_name="post",
            name="artist",
            field=models.CharField(max_length=500, null=True),
        ),
        migrations.AddField(
            model_name="post",
            name="url",
            field=models.URLField(max_length=512, null=True),
        ),
        migrations.AlterField(
            model_name="post",
            name="id",
            field=models.UUIDField(
                default=uuid.UUID("c9bac7f7-cee9-4643-a8f6-8d62152bc853"),
                primary_key=True,
                serialize=False,
                unique=True,
            ),
        ),
    ]
