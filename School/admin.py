from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Class, Section, Profile, Student, Attendance, Subject, Result, Ticket, Teacher

# Inline Profile Admin for User
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'

# Custom User Admin to integrate Profile
class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)

    # Display role in the user list
    def role(self, obj):
        return obj.profile.role
    role.short_description = 'Role'
    role.admin_order_field = 'profile__role'

    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'profile__role')

    # Allow filtering by role
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.select_related('profile')
        return queryset

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
    list_display = ('id', 'student', 'subject', 'marks', 'total_marks', 'grade')
    list_filter = ('subject', 'grade')
    search_fields = ('student__profile__user__username', 'subject__name')

# Register Ticket
@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('id', 'student', 'issue', 'date_raised', 'status')
    list_filter = ('status', 'date_raised')
    search_fields = ('student__profile__user__username', 'issue')


# Teacher Admin
@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    # Fields to display in the list view
    list_display = ('profile', 'subject', 'full_name', 'year_of_joining', 'department')  # Added 'department'
    
    # Fields to filter by in the admin panel
    list_filter = ('subject', 'department')  # Added 'department' to filter options
    
    # Fields to search by in the admin panel
    search_fields = ('profile__user__username', 'subject', 'full_name', 'department')  # Added 'department' to search
    
    # Optionally, make 'subject' and 'department' editable directly in the list view
    list_editable = ('subject', 'department')

    # Ordering by year_of_joining
    ordering = ('year_of_joining',)


# Unregister the default User and re-register it with the custom UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
