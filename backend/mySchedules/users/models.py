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
