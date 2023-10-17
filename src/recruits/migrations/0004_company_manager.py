# Generated by Django 4.2.6 on 2023-10-17 03:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("recruits", "0003_remove_company_manager"),
    ]

    operations = [
        migrations.AddField(
            model_name="company",
            name="manager",
            field=models.OneToOneField(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="company",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
