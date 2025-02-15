import datetime
from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('teacher', 'Teacher'),
        ('staff', 'Staff'),
    ]
    
    CLASS_CHOICES = [(str(i), str(i)) for i in range(6, 11)]
    SECTION_CHOICES = [('A', 'A'), ('B', 'B')]
    BLOOD_GROUP_CHOICES = [('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'),
                           ('O+', 'O+'), ('O-', 'O-'), ('AB+', 'AB+'), ('AB-', 'AB-')]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')

    # Student Fields
    student_class = models.CharField(max_length=2, choices=CLASS_CHOICES, blank=True, null=True)
    section = models.CharField(max_length=1, choices=SECTION_CHOICES, blank=True, null=True)
    admission_date = models.DateField(blank=True, null=True)
    permanent_address = models.CharField(max_length=255, blank=True, null=True)
    father_name = models.CharField(max_length=100, blank=True, null=True)
    mother_name = models.CharField(max_length=100, blank=True, null=True)
    mobile_number = models.CharField(max_length=15, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUP_CHOICES, blank=True, null=True)

    # Teacher Fields
    subject = models.CharField(max_length=100, blank=True, null=True)
    joining_date = models.DateField(blank=True, null=True)
    teacher_address = models.TextField(blank=True, null=True)

    # Staff Fields
    department = models.CharField(max_length=100, blank=True, null=True)
    staff_mobile = models.CharField(max_length=11, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.user.username:  # Only generate if username is empty
            current_year = datetime.datetime.now().year

            # Determine prefix based on role
            prefix = ""
            if self.role == "teacher":
                prefix = "T"
            elif self.role == "staff":
                prefix = "S"

            # Find last user with the same prefix and year
            last_user = User.objects.filter(username__startswith=f"{prefix}{current_year}").order_by('-username').first()

            if last_user:
                last_number = int(last_user.username[-4:])  # Extract last 4 digits
                new_number = last_number + 1
            else:
                new_number = 1

            new_username = f"{prefix}{current_year}{str(new_number).zfill(4)}"
            self.user.username = new_username  # Assign username

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.role}"