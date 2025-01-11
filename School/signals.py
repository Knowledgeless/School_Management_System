from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile, Student, Teacher

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Signal to create a Profile and related models (Student, Teacher) automatically
    when a User is created.
    """
    if created:
        # Create a Profile with a default role if not explicitly set
        profile = Profile.objects.create(user=instance, role='Student')  # Default role
        
        # Automatically create related models based on the role
        if profile.role == 'Student':
            Student.objects.create(profile=profile, class_name='DefaultClass', section='A', roll_no=0)
        elif profile.role == 'Teacher':
            Teacher.objects.create(profile=profile, subject='DefaultSubject')
        # Add cases for other roles if needed
