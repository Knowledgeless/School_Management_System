from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name=''),
    path('home', views.home, name='home'),
    path('register', views.register, name='register'),
    path('login_view', views.login_view, name='login'),
    path('logout_view', views.logout_view, name='logout'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('student_list', views.student_list, name='student_list'),
    path('attendance', views.attendance, name='attendance'),
    path('results', views.results, name='results'),
    path('tickets', views.tickets, name='tickets'),
]
