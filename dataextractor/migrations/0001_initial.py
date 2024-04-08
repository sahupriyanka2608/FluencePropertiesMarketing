# Generated by Django 4.1.7 on 2024-04-06 20:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Post",
            fields=[
                ("created_time", models.DateTimeField()),
                (
                    "post_id",
                    models.CharField(max_length=200, primary_key=True, serialize=False),
                ),
                ("message", models.TextField(blank=True, null=True)),
                ("attachments", models.JSONField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="User",
            fields=[
                (
                    "user_id",
                    models.CharField(max_length=200, primary_key=True, serialize=False),
                ),
                ("username", models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name="Comment",
            fields=[
                (
                    "comment_id",
                    models.CharField(max_length=200, primary_key=True, serialize=False),
                ),
                ("message", models.CharField(max_length=200, null=True)),
                ("created_time", models.DateTimeField(null=True)),
                (
                    "post_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="comments",
                        to="dataextractor.post",
                    ),
                ),
                (
                    "user_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="commentsbyuser",
                        to="dataextractor.user",
                    ),
                ),
            ],
        ),
    ]
