# Generated by Django 4.1.2 on 2022-11-10 11:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="CheckListSetup",
            fields=[
                (
                    "id",
                    models.AutoField(editable=False, primary_key=True, serialize=False),
                ),
                ("name", models.CharField(max_length=100, unique=True)),
                ("display_text", models.CharField(max_length=100)),
                ("description", models.TextField(blank=True, null=True)),
                ("display_image", models.ImageField(upload_to="static/checklist/")),
                ("is_active", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("modified_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "db_table": "checklist_setup",
                "ordering": ["-created_at"],
            },
        ),
        migrations.CreateModel(
            name="FloorSetup",
            fields=[
                (
                    "id",
                    models.AutoField(editable=False, primary_key=True, serialize=False),
                ),
                ("name", models.CharField(max_length=100, unique=True)),
                ("description", models.TextField(blank=True, null=True)),
                ("floor_map", models.ImageField(upload_to="static/floors/")),
                ("is_active", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("modified_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "db_table": "floor_setup",
                "ordering": ["-created_at"],
            },
        ),
        migrations.CreateModel(
            name="RestroomReasonSetup",
            fields=[
                (
                    "id",
                    models.AutoField(editable=False, primary_key=True, serialize=False),
                ),
                ("name", models.CharField(max_length=100, unique=True)),
                ("display_text", models.CharField(max_length=100)),
                ("description", models.TextField(blank=True, null=True)),
                ("display_image", models.ImageField(upload_to="static/reasons/")),
                ("is_active", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("modified_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "db_table": "reason_setup",
                "ordering": ["-created_at"],
            },
        ),
        migrations.CreateModel(
            name="RoomSetup",
            fields=[
                (
                    "id",
                    models.AutoField(editable=False, primary_key=True, serialize=False),
                ),
                ("name", models.CharField(max_length=100, unique=True)),
                ("description", models.TextField(blank=True, null=True)),
                ("room_shape", models.CharField(blank=True, max_length=100, null=True)),
                ("room_location", models.TextField(blank=True, null=True)),
                ("reason", models.TextField(blank=True, null=True)),
                ("is_active", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("modified_at", models.DateTimeField(auto_now=True)),
                (
                    "floor",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="rooms",
                        to="restroom.floorsetup",
                    ),
                ),
            ],
            options={
                "db_table": "room_setup",
                "ordering": ["-created_at"],
            },
        ),
        migrations.CreateModel(
            name="Tickets",
            fields=[
                (
                    "id",
                    models.AutoField(editable=False, primary_key=True, serialize=False),
                ),
                ("reason", models.JSONField()),
                ("feedback", models.BooleanField(default=False)),
                ("is_resolved", models.BooleanField(default=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("modified_at", models.DateTimeField(auto_now=True)),
                (
                    "room",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="tickets_room",
                        to="restroom.roomsetup",
                    ),
                ),
                (
                    "updated_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="ticket_update",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "db_table": "tickets",
                "ordering": ["-created_at"],
            },
        ),
        migrations.CreateModel(
            name="CheckList",
            fields=[
                (
                    "id",
                    models.AutoField(editable=False, primary_key=True, serialize=False),
                ),
                ("checklist", models.JSONField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("modified_at", models.DateTimeField(auto_now=True)),
                (
                    "created_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="checklist",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "room",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="checklist_room",
                        to="restroom.roomsetup",
                    ),
                ),
            ],
            options={
                "db_table": "checklist",
                "ordering": ["-created_at"],
            },
        ),
    ]
