from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Class, Section, Profile, Student, Attendance, Subject, Result, Ticket, Teacher
from django.db import transaction


# Inline Profile Admin for User
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'


# Custom User Admin to integrate Profile
class UserAdmin(BaseUserAdmin):
    inlines = [ProfileInline]

    # Display role in the user list
    def role(self, obj):
        return obj.profile.role
    role.short_description = 'Role'
    role.admin_order_field = 'profile__role'

    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'profile__role')

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.select_related('profile')
        return queryset

    def save_model(self, request, obj, form, change):
        """
        Ensure a Profile is created or retrieved, and roles are handled correctly.
        """
        # First, save the user
        super().save_model(request, obj, form, change)

        # Use transaction.atomic to ensure both user and profile are saved correctly
        with transaction.atomic():
            # Ensure Profile exists or is retrieved
            profile, created = Profile.objects.get_or_create(user=obj)

            # Only create Teacher or Student if Profile is created
            if created:
                if profile.role == "Teacher":
                    Teacher.objects.get_or_create(profile=profile)
                elif profile.role == "Student":
                    Student.objects.get_or_create(profile=profile)

    def save_related(self, request, form, formsets, change):
        """
        Avoid creating profiles again, as it's handled in `save_model`.
        """
        super().save_related(request, form, formsets, change)

        # No need to create the Profile here since it is already created in save_model
        profile = form.instance.profile

        # Ensure the profile is not duplicated
        if profile.user is not None:
            # Handle Teacher/Student relation if not created before
            if profile.role == "Teacher":
                Teacher.objects.get_or_create(profile=profile)
            elif profile.role == "Student":
                Student.objects.get_or_create(profile=profile)
        else:
            # If profile doesn't have a user associated, you might want to raise an error or handle it
            raise ValueError("Profile must be associated with a User before creating Teacher/Student.")

# Register Class
@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

# Register Section
@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ('id', 'class_name', 'name')
    list_filter = ('class_name',)
    search_fields = ('class_name__name', 'name')

# Register Profile
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'role')
    list_filter = ('role',)
    search_fields = ('user__username', 'role')

# Register Student
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('profile', 'full_name', 'class_name', 'section', 'roll_no', 'year_of_admission')  # Add the field here
    list_filter = ('class_name', 'section', 'year_of_admission')  # Add the field to the filter

# Register Attendance
@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('id', 'student', 'date', 'status')
    list_filter = ('date', 'status')
    search_fields = ('student__profile__user__username',)

# Register Subject
@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'teacher')
    search_fields = ('name', 'teacher__user__username')

# Register Result
@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ('student', 'subject', 'semester', 'marks', 'total_marks', 'grade')
    list_filter = ('semester', 'grade')  # Filters for semester and grade
    search_fields = ('student__profile__user__username', 'subject__name')  # Search by student username or subject name
    ordering = ('semester', 'student')  # Default ordering in the admin panel
    readonly_fields = ('grade',)  # Grade is calculated automatically and should not be editable

    def save_model(self, request, obj, form, change):
        """
        Ensure the grade is recalculated whenever the result is saved.
        """
        obj.grade = obj.calculate_grade()  # Recalculate the grade
        super().save_model(request, obj, form, change)

# Register Ticket
@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('id', 'student', 'issue', 'date_raised', 'status')
    list_filter = ('status', 'date_raised')
    search_fields = ('student__profile__user__username', 'issue')


# Teacher Admin
@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ['profile', 'subject', 'full_name', 'year_of_joining', 'department', 'phone_number', 'email']
    list_filter = ('subject', 'department', 'year_of_joining')
    search_fields = ('profile__user__username', 'subject', 'full_name', 'department', 'phone_number', 'email')
    list_editable = ('subject', 'department', 'phone_number', 'email')
    ordering = ('year_of_joining',)


# Unregister the default User and re-register it with the custom UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
