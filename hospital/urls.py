from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path("dashboard/",views.dashboard,name="dashboard"),
    path('logout/', views.logout_view, name='logout'),
    path('doctor/dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
    path('patient/dashboard/', views.patient_dashboard, name='patient_dashboard'),
    path('', views.home, name='home'),

    path('doctor/', views.doctor_list, name='doctor_list'),
    path('doctor/add/', views.doctor_add, name='doctor_add'),
    path('doctor/edit/<int:id>/', views.doctor_edit, name='doctor_edit'),
    path("doctor/delete/<int:id>/", views.doctor_delete, name="doctor_delete"),

    path('patient/', views.patient_list, name='patient_list'),
    path('patient/add/', views.patient_add, name='patient_add'),
    path('patient/edit/<int:id>/', views.patient_edit, name='patient_edit'),
    path('patient/delete/<int:id>/', views.patient_delete, name='patient_delete'),

    path("group/",views.group_list,name="group_list"),
    path("group/add/",views.group_add,name="group_add"),
    path("group/edit/<int:id>/",views.group_edit,name="group_edit"),
    path("group/delete/<int:id>/",views.group_delete,name="group_delete"),
]