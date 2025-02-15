from django.urls import path
from . import views


urlpatterns = [
    path("", views.home, name="home"),
    path("add_person/", views.add_person, name="add_person"),
    path("teachers_list/", views.teachers_list, name="teachers_list"),
    path("students_list/", views.students_list, name="students_list"),
    path("grade/", views.grade, name="grade"),
    path("attendence/", views.attendence, name="attendence"),
    path("admit_card/", views.admit_card, name="admit_card"),
    path("tickets/", views.tickets, name="tickets"),
]
