from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name=''),
    path('home', views.home, name='home'),
    path('register', views.register, name='register'),
    path('login_view', views.login_view, name='login'),
    path('logout_view', views.logout_view, name='logout'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('student_list', views.student_list, name='student_list'),
    path('teacher_list', views.teacher_list, name='teacher_list'),
    path('attendance', views.attendance, name='attendance'),
    path('results', views.results, name='results'),
    path('tickets', views.tickets, name='tickets'),
    path("manage-users", views.manage_users, name="manage_users"),
    path('subjects', views.subjects, name='subjects'),
    path('notices', views.notices, name='notices'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)