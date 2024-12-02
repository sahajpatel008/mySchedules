# Generated by Django 5.1.3 on 2024-11-30 00:43

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0005_shift"),
    ]

    operations = [
        migrations.CreateModel(
            name="Pickup",
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
                    "request_status",
                    models.CharField(
                        choices=[
                            ("Approved", "Approved"),
                            ("Pending", "Pending"),
                            ("Declined", "Declined"),
                        ],
                        max_length=10,
                    ),
                ),
            ],
        ),
        migrations.RemoveConstraint(
            model_name="shift",
            name="unique_shift_employee",
        ),
        migrations.AddConstraint(
            model_name="shift",
            constraint=models.UniqueConstraint(
                fields=("shift_id", "employee"), name="unique_normalShift_employee"
            ),
        ),
        migrations.AddField(
            model_name="pickup",
            name="employee",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AddField(
            model_name="pickup",
            name="shift",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="users.uniqueshift"
            ),
        ),
        migrations.AddConstraint(
            model_name="pickup",
            constraint=models.UniqueConstraint(
                fields=("shift", "employee"), name="unique_pickupShift_employee"
            ),
        ),
    ]
