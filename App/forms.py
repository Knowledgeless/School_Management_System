from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile

class CustomUserCreationForm(UserCreationForm):
    ROLE_CHOICES = [('student', 'Student'), ('teacher', 'Teacher'), ('staff', 'Staff')]

    full_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Full Name'}), required=True)
    role = forms.ChoiceField(choices=ROLE_CHOICES, required=True)

    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}))

    student_class = forms.ChoiceField(choices=[('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'), ('10', '10')],
                                      widget=forms.Select(attrs={'placeholder': 'Class'}), required=False)
    section = forms.ChoiceField(choices=[('A', 'A'), ('B', 'B')], widget=forms.Select(), required=False)
    admission_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False)
    permanent_address = forms.CharField(widget=forms.TextInput(attrs={'placeholder': "Permanent Address"}), required=False)
    father_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': "Father's Name"}), required=False)
    mother_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': "Mother's Name"}), required=False)
    mobile_number = forms.CharField(widget=forms.TextInput(attrs={'placeholder': "Mobile Number"}), required=False)
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False)
    BLOOD_GROUP_CHOICES = [
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('O+', 'O+'), ('O-', 'O-'),
        ('AB+', 'AB+'), ('AB-', 'AB-')
    ]
    blood_group = forms.ChoiceField(choices=BLOOD_GROUP_CHOICES, widget=forms.Select(), required=False)

    subject = forms.CharField(widget=forms.TextInput(attrs={'placeholder': "Subject"}), required=False)
    joining_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False)
    teacher_address = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Teacher Address'}), required=False)

    department = forms.CharField(widget=forms.TextInput(attrs={'placeholder': "Department"}), required=False)
    staff_mobile = forms.CharField(widget=forms.TextInput(attrs={'placeholder': "Mobile Number"}), required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'role',
                  'student_class', 'section', 'admission_date', 'permanent_address',
                  'father_name', 'mother_name', 'mobile_number', 'date_of_birth', 'blood_group',
                  'subject', 'joining_date', 'teacher_address',
                  'department', 'staff_mobile']

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            profile = UserProfile.objects.create(
                user=user,
                role=self.cleaned_data['role'],
                student_class=self.cleaned_data.get('student_class', '6'),
                section=self.cleaned_data.get('section', 'A'),
                admission_date=self.cleaned_data.get('admission_date', None),
                permanent_address=self.cleaned_data.get('permanent_address', "Enter permanent address"),
                father_name=self.cleaned_data.get('father_name', "Father's Name"),
                mother_name=self.cleaned_data.get('mother_name', "Mother's Name"),
                mobile_number=self.cleaned_data.get('mobile_number', "01xxxxxxxxx"),
                date_of_birth=self.cleaned_data.get('date_of_birth', None),
                blood_group=self.cleaned_data.get('blood_group', 'O+'),
                subject=self.cleaned_data.get('subject', "Enter Subject"),
                joining_date=self.cleaned_data.get('joining_date', None),
                teacher_address=self.cleaned_data.get('teacher_address', "Enter Teacher Address"),
                department=self.cleaned_data.get('department', "Enter Department"),
                staff_mobile=self.cleaned_data.get('staff_mobile', "01xxxxxxxxx"),
            )
            profile.save()
        return user


'''
let create the username automatically. If there is any user except the admin, for students follow the pattern as, admission_year + 000 + last user number+1 . if there are no users, and a student is admitting in class 8 it will be for this year like 20250001
'''