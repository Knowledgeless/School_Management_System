from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden
from .models import Profile, Student, Class, Section, Result, Attendance, Ticket, Teacher
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
            user.set_password(user_form.cleaned_data["password1"])
            user.save()

            # Create and save the profile with the user
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()

            # Set the user's full name and handle role-specific data
            full_name = f"{user.first_name} {user.last_name}"
            if profile.role == "Teacher" and teacher_form.is_valid():
                teacher = teacher_form.save(commit=False)
                teacher.profile = profile
                teacher.year_of_joining = request.POST.get("year_of_joining")
                teacher.save()

            elif profile.role == "Student" and student_form.is_valid():
                student = student_form.save(commit=False)
                student.profile = profile
                student.year_of_admission = request.POST.get("year_of_admission")
                student.full_name = full_name
                student.save()

            return redirect("login")  # Redirect to login page
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
            # Check if the user has a profile
            if not hasattr(user, 'profile'):
                # Create a profile for the admin user automatically
                Profile.objects.create(user=user, role='Admin')
            
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
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        # Automatically create a profile for users without one
        profile = Profile.objects.create(user=request.user, role="Admin")
        return render(request, "html/dashboard.html", {"role": "Admin", "full_name": request.user.get_full_name()})

    if profile.role == "Student":
        try:
            student = Student.objects.get(profile=profile)
            return render(
                request, 
                "html/dashboard.html", 
                {"role": "Student", "student": student, "full_name": student.full_name}
            )
        except Student.DoesNotExist:
            # Redirect or show a message if no student instance is linked
            return render(
                request,
                "html/error.html",
                {"message": "Student profile not found. Contact Admin."},
            )

    elif profile.role == "Teacher":
        try:
            teacher = Teacher.objects.get(profile=profile)
            full_name = teacher.full_name
            return render(
                request, 
                "html/dashboard.html", 
                {"role": "Teacher", "teacher": teacher, "full_name": full_name}
            )
        except Teacher.DoesNotExist:
            # Redirect or show a message if no teacher instance is linked
            return render(
                request,
                "html/error.html",
                {"message": "Teacher profile not found. Contact Admin."},
            )

    elif profile.role == "Admin":
        full_name = request.user.get_full_name()
        if full_name:
            return render(request, "html/dashboard.html", {"role": "Admin", "full_name": full_name})
        else:
            return render(request, "html/dashboard.html", {"role": "Admin", "full_name": "Admin"})

    else:
        return HttpResponseForbidden("You are not authorized to access this page.")

@login_required
def student_list(request):
    """View to manage students."""
    if request.user.profile.role not in ["Teacher", "Admin"]:
        return HttpResponseForbidden()

    students = Student.objects.all()
    return render(request, "html/student_list.html", {"students": students})

@login_required
def teacher_list(request):
    """View to manage students."""
    if request.user.profile.role not in ["Admin"]:
        return HttpResponseForbidden()

    teacher = Teacher.objects.all()
    return render(request, "html/teacher_list.html", {"students": teacher})

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
        student_form = StudentForm(request.POST, request.FILES)  # Handle file uploads

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

@login_required
def manage_users(request):
    """View for managing users (Admin only)."""
    if request.user.profile.role != "Admin":
        return HttpResponseForbidden("You are not authorized to view this page.")

    users = User.objects.all()
    return render(request, "html/manage_users.html", {"users": users})


@login_required
def subjects(request):
    """View subjects for students or teachers."""
    if request.user.profile.role == "Student":
        student = Student.objects.get(profile=request.user.profile)
        subjects = Subject.objects.filter(class_name=student.class_name)
    elif request.user.profile.role == "Teacher":
        teacher = Teacher.objects.get(profile=request.user.profile)
        subjects = Subject.objects.filter(teacher=request.user.profile)
    elif request.user.profile.role == "Admin":
        subjects = Subject.objects.all()
    else:
        return HttpResponseForbidden("Unauthorized Access")
    return render(request, "html/subjects.html", {"subjects": subjects})

@login_required
def notices(request):
    """Display notices."""
    notices = [
        {"title": "Annual Day", "description": "Details about the event."},
        {"title": "Exam Schedule", "description": "Midterm exam dates."},
    ]
    return render(request, "html/notices.html", {"notices": notices})
