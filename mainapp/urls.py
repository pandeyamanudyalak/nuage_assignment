from django.contrib import admin
from django.urls import path
from mainapp.views import *

urlpatterns = [
    path('token',TokenObtainPairView.as_view(),name='get_token_view'),
    path('users', UserCreateAPIView.as_view(), name='user-create'),
    path('departments/', DepartmentListCreateAPIView.as_view(), name='department-list-create'),
    path('departments/<int:pk>/', DepartmentRetrieveUpdateDestroyAPIView.as_view(), name='department-detail'),
    path('students/', StudentListCreateAPIView.as_view(), name='student-list-create'),
    path('students/<int:pk>/', StudentRetrieveUpdateDestroyAPIView.as_view(), name='student-detail'),
    path('attendance_logs/', AttendanceLogListCreateAPIView.as_view(), name='attendance-log-list-create'),
    path('attendance_logs/<int:pk>/', AttendanceLogRetrieveUpdateDestroyAPIView.as_view(), name='attendance-log-detail'),
    path('courses/', CourseListCreateAPIView.as_view(), name='course-list-create'),
    path('courses/<int:pk>/', CourseRetrieveUpdateDestroyAPIView.as_view(), name='course-detail'),
]
