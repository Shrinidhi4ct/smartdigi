# Generated by Django 4.1.2 on 2023-01-02 10:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("integration", "0006_alter_footfall_created_at"),
    ]

    operations = [
        migrations.AlterField(
            model_name="footfall",
            name="created_at",
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
