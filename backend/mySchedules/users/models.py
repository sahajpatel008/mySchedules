from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class User(AbstractUser):

    ROLE_CHOICES = (
        ('manager', "Manager"),
        ('employee', "Employee")
    )
    username = models.CharField(max_length=100, primary_key=True, unique=True)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='employee')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'users'  # This should match the table name in PostgreSQL


class UniqueShift(models.Model):
    shift_id = models.AutoField(primary_key=True)
    employee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='employee_shifts', null=True, blank=True)
    manager = models.ForeignKey(User, on_delete=models.CASCADE, related_name='manager_shifts', null=True, blank=True)
    date = models.DateField()
    location = models.CharField(max_length=100)
    start_time = models.TimeField()
    end_time = models.TimeField()

    #input: date, location, start_time, end_time
    

    def __str__(self):
        return f"Shift {self.shift_id} at {self.location} on {self.date}"


# Shift model
class Shift(models.Model):
    STATUS_CHOICES = [
        ('New', 'New'),
        ('Request', 'Request'),
        ('Swap Request', 'Swap Request'),
        ('Approved', 'Approved'),
        ('Declined', 'Declined'),
        ('Completed', 'Completed'),
        ('Release', 'Release'),
    ]
    shift_id = models.ForeignKey(UniqueShift, on_delete=models.CASCADE)
    employee = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['shift_id', 'employee'], name='unique_normalShift_employee')
        ]
        
        # Use this as the logical primary key for ordering or queries
        unique_together = ('shift_id', 'employee')

    def __str__(self):
        return f"Shift {self.shift_id} for Employee {self.employee}"


# Pickup model
class Pickup(models.Model):
    REQUEST_STATUS_CHOICES = [
        ('Approved', 'Approved'),
        ('Request', 'Request'),
        ('Declined', 'Declined'),
    ]

    shift = models.ForeignKey(UniqueShift, on_delete=models.CASCADE)
    employee = models.ForeignKey(User, on_delete=models.CASCADE)
    request_status = models.CharField(max_length=10, choices=REQUEST_STATUS_CHOICES)

    class Meta:
        # Enforce the combination of shift and employee to be unique
        constraints = [
            models.UniqueConstraint(fields=['shift', 'employee'], name='unique_pickupShift_employee')
        ]

    def __str__(self):
        return f"Pickup {self.shift_id} by Employee {self.employee}"
