from django.db import models
from django.contrib.auth.models import User

# Class Model
class Class(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

# Section Model
class Section(models.Model):
    class_name = models.ForeignKey(Class, on_delete=models.CASCADE)
    name = models.CharField(max_length=1)

    def __str__(self):
        return f"{self.class_name.name} - {self.name}"

# User Profile for Role Management
class Profile(models.Model):
    """Profile model to store user role (Admin, Teacher, Student)."""
    ROLE_CHOICES = [
        ('Admin', 'Admin'),
        ('Teacher', 'Teacher'),
        ('Student', 'Student'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.user.username} ({self.role})"

# Student Model
class Student(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    class_name = models.CharField(max_length=20)
    section = models.CharField(max_length=2)
    roll_no = models.IntegerField()
    full_name = models.CharField(max_length=255, default="give_me_name")
    year_of_admission = models.IntegerField(null=True, blank=True)  # Add this field
    photo = models.ImageField(upload_to='student_photos/', null=True, blank=True)  # Add this field

    def __str__(self):
        return f"{self.profile.user.username} - {self.class_name} {self.section}"

    def save(self, *args, **kwargs):
        # Automatically set the full name to user's full name if it's not set
        if self.full_name == "give_me_name":
            self.full_name = f"{self.profile.user.first_name} {self.profile.user.last_name}"
        super().save(*args, **kwargs)

# Attendance Model
class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=10, choices=[('Present', 'Present'), ('Absent', 'Absent')])

    def __str__(self):
        return f"{self.student.profile.user.username} - {self.date} - {self.status}"

# Subject Model
class Subject(models.Model):
    name = models.CharField(max_length=100)
    teacher = models.ForeignKey(Profile, on_delete=models.CASCADE, limit_choices_to={'role': 'Teacher'})

    def __str__(self):
        return self.name

# Result Model
class Result(models.Model):
    SEMESTER_CHOICES = [
        ('Sem1', 'Semester 1'),
        ('Sem2', 'Semester 2'),
        ('Sem3', 'Semester 3'),
    ]
    student = models.ForeignKey('Student', on_delete=models.CASCADE)
    subject = models.ForeignKey('Subject', on_delete=models.CASCADE)
    semester = models.CharField(max_length=5, choices=SEMESTER_CHOICES, default='Sem1')  # Default to Semester 1
    marks = models.FloatField()
    total_marks = models.FloatField()
    grade = models.CharField(max_length=2, blank=True, default='F')  # Default to 'F'

    def calculate_grade(self):
        if self.marks <= 32:
            return 'F'
        elif self.marks >= 80:
            return 'A+'
        elif 70 <= self.marks < 80:
            return 'A'
        elif 60 <= self.marks < 70:
            return 'A-'
        elif 50 <= self.marks < 60:
            return 'B'
        elif 40 <= self.marks < 50:
            return 'C'
        else:
            return 'D'

    def save(self, *args, **kwargs):
        self.grade = self.calculate_grade()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.student.profile.user.username} - {self.subject.name} ({self.semester})"

class TotalGrade(models.Model):
    student = models.OneToOneField('Student', on_delete=models.CASCADE)
    grade = models.CharField(max_length=2, blank=True)

    def calculate_total_grade(self):
        results = Result.objects.filter(student=self.student)
        grades = [result.grade for result in results]
        if 'F' in grades:
            return 'F'
        average_mark = sum(result.marks for result in results) / len(results)
        if average_mark >= 80:
            return 'A+'
        elif 70 <= average_mark < 80:
            return 'A'
        elif 60 <= average_mark < 70:
            return 'A-'
        elif 50 <= average_mark < 60:
            return 'B'
        elif 40 <= average_mark < 50:
            return 'C'
        else:
            return 'D'

    def save(self, *args, **kwargs):
        self.grade = self.calculate_total_grade()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Total Grade: {self.grade} for {self.student.profile.user.username}"

# Ticket Model
class Ticket(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    issue = models.TextField()
    date_raised = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[('Open', 'Open'), ('Resolved', 'Resolved')], default='Open')

    def __str__(self):
        return f"Ticket by {self.student.profile.user.username} - {self.status}"

# Teacher Model
class Teacher(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)  # e.g., "Math", "Science"
    year_of_joining = models.IntegerField(null=True, blank=True)
    department = models.CharField(max_length=100, blank=True, null=True)  # New department field
    
    def __str__(self):
        return f"{self.profile.user.username} - {self.subject}"

    @property
    def full_name(self):
        # Return the full name from the related user profile
        return f"{self.profile.user.first_name} {self.profile.user.last_name}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)