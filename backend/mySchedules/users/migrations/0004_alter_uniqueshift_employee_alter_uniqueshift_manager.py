# Generated by Django 5.1.3 on 2024-11-29 08:02

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0003_uniqueshift"),
    ]

    operations = [
        migrations.AlterField(
            model_name="uniqueshift",
            name="employee",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="employee_shifts",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="uniqueshift",
            name="manager",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="manager_shifts",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
