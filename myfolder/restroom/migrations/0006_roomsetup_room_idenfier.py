# Generated by Django 4.1.2 on 2022-11-28 09:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("restroom", "0005_ratingsetup_is_active"),
    ]

    operations = [
        migrations.AddField(
            model_name="roomsetup",
            name="room_idenfier",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]