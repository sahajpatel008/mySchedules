# Generated by Django 5.1.3 on 2024-11-29 23:58

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0004_alter_uniqueshift_employee_alter_uniqueshift_manager"),
    ]

    operations = [
        migrations.CreateModel(
            name="Shift",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("New", "New"),
                            ("Request", "Request"),
                            ("Swap Request", "Swap Request"),
                            ("Approved", "Approved"),
                            ("Declined", "Declined"),
                            ("Completed", "Completed"),
                            ("Release", "Release"),
                        ],
                        max_length=20,
                    ),
                ),
                (
                    "employee",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "shift_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="users.uniqueshift",
                    ),
                ),
            ],
            options={
                "constraints": [
                    models.UniqueConstraint(
                        fields=("shift_id", "employee"), name="unique_shift_employee"
                    )
                ],
                "unique_together": {("shift_id", "employee")},
            },
        ),
    ]
