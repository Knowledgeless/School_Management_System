from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Teacher, Student, Ticket

class UserForm(UserCreationForm):
    """Form for creating new users."""
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class ProfileForm(forms.ModelForm):
    """Form for user profile (role)."""
    class Meta:
        model = Profile
        fields = ['role']  # Enum choices for role (Admin, Teacher, Student)

class TeacherForm(forms.ModelForm):
    """Form for teacher-specific details."""
    class Meta:
        model = Teacher
        fields = ['subject', 'department']

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['class_name', 'section', 'roll_no', 'full_name', 'year_of_admission', 'photo']  # Add 'photo' field here

class TicketForm(forms.ModelForm):
    """Form for raising tickets."""
    ISSUE_CHOICES = [
        ('Technical Issue', 'Technical Issue'),
        ('Account Issue', 'Account Issue'),
        ('Other', 'Other')
    ]
    
    issue_type = forms.ChoiceField(choices=ISSUE_CHOICES)
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 4, 'placeholder': 'Describe your issue here...'}))

    class Meta:
        model = Ticket
        fields = ['issue_type', 'description']
