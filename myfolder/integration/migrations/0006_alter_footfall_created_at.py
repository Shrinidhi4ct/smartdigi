# Generated by Django 4.1.2 on 2023-01-02 10:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("integration", "0005_footfall"),
    ]

    operations = [
        migrations.AlterField(
            model_name="footfall",
            name="created_at",
            field=models.DateTimeField(blank=True, default=None, null=True),
        ),
    ]
