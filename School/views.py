from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden
from .models import Profile, Student, Class, Section, Result, Attendance, Ticket
from .forms import UserForm, ProfileForm, StudentForm, TicketForm, TeacherForm

def home(request):
    """Landing page."""
    return render(request, "html/home.html")

def register(request):
    """User registration view for Admin to create users."""
    if request.method == "POST":
        user_form = UserForm(request.POST)
        profile_form = ProfileForm(request.POST)
        teacher_form = TeacherForm(request.POST)
        student_form = StudentForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            # Save the user and profile
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data["password"])
            user.save()

            # Create and save the profile with the user
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()

            # Based on role, save role-specific data
            if profile.role == "Teacher" and teacher_form.is_valid():
                teacher = teacher_form.save(commit=False)
                teacher.profile = profile
                teacher.save()

            if profile.role == "Student" and student_form.is_valid():
                student = student_form.save(commit=False)
                student.profile = profile
                student.save()

            # After creating user, redirect to login page
            return redirect("login")
    else:
        user_form = UserForm()
        profile_form = ProfileForm()
        teacher_form = TeacherForm()
        student_form = StudentForm()

    return render(
        request,
        "html/register.html",
        {
            "user_form": user_form,
            "profile_form": profile_form,
            "teacher_form": teacher_form,
            "student_form": student_form,
        },
    )

def login_view(request):
    """User login view."""
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("dashboard")
        else:
            return render(request, "html/login.html", {"error": "Invalid credentials."})
    return render(request, "html/login.html")

@login_required
def logout_view(request):
    """User logout view."""
    logout(request)
    return redirect("home")

@login_required
def dashboard(request):
    """Dashboard view for different user roles."""
    profile = request.user.profile
    if profile.role == "Student":
        return render(request, "html/dashboard.html", {"role": "Student"})
    elif profile.role == "Teacher":
        return render(request, "html/dashboard.html", {"role": "Teacher"})
    elif profile.role == "Admin":
        return render(request, "html/dashboard.html", {"role": "Admin"})
    else:
        return HttpResponseForbidden()

@login_required
def student_list(request):
    """View to manage students."""
    if request.user.profile.role not in ["Teacher", "Admin"]:
        return HttpResponseForbidden()

    students = Student.objects.all()
    return render(request, "html/student_list.html", {"students": students})

@login_required
def attendance(request):
    """View attendance."""
    if request.user.profile.role == "Student":
        attendance_records = Attendance.objects.filter(student=request.user.profile.student)
        return render(request, "html/attendance.html", {"attendance_records": attendance_records})
    elif request.user.profile.role in ["Teacher", "Admin"]:
        # For teachers/admins to mark or view attendance
        students = Student.objects.all()
        return render(request, "html/attendance.html", {"students": students})
    else:
        return HttpResponseForbidden()

@login_required
def results(request):
    """View results for students."""
    if request.user.profile.role == "Student":
        results = Result.objects.filter(student=request.user.profile.student)
        return render(request, "html/results.html", {"results": results})
    elif request.user.profile.role in ["Teacher", "Admin"]:
        # Allow teachers/admins to view or manage results
        return render(request, "html/results.html", {"manage_results": True})
    else:
        return HttpResponseForbidden()

@login_required
def tickets(request):
    """Raise or view tickets."""
    if request.method == "POST":
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect("tickets")
    else:
        form = TicketForm()
        tickets = Ticket.objects.filter(user=request.user)
        return render(request, "html/tickets.html", {"form": form, "tickets": tickets})



def create_student(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = ProfileForm(request.POST)
        student_form = StudentForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid() and student_form.is_valid():
            # Create user instance
            user = user_form.save()

            # Create profile and link it to user
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()

            # Create student instance and link it to the profile
            student = student_form.save(commit=False)
            student.profile = profile

            # If student has no full name, set it based on the user's first and last name
            if student.full_name == "give_me_name":
                student.full_name = f"{user.first_name} {user.last_name}"

            student.save()

            # Log the user in after registration
            login(request, user)
            return redirect('student_dashboard')  # Redirect to the student dashboard or desired page
    else:
        user_form = UserForm()
        profile_form = ProfileForm()
        student_form = StudentForm()

    return render(request, 'create_student.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'student_form': student_form
    })