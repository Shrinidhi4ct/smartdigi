# Generated by Django 4.1.3 on 2022-11-15 08:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("restroom", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="RatingSetup",
            fields=[
                (
                    "id",
                    models.AutoField(editable=False, primary_key=True, serialize=False),
                ),
                ("name", models.CharField(max_length=100, unique=True)),
                ("display_text", models.CharField(max_length=100)),
                ("description", models.TextField(blank=True, null=True)),
                ("display_image", models.ImageField(upload_to="static/rating/")),
                ("is_active", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("modified_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "db_table": "rating_setup",
                "ordering": ["-created_at"],
            },
        ),
    ]