from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import *
from .serializers import *
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated 
from rest_framework_simplejwt.views import TokenObtainPairView



class UserCreateAPIView(APIView):
    def post(self, request, *args, **kwargs):
        # Create a new UserSerializer instance with the data from the request
        serializer = UserSerializer(data=request.data)
        
        if serializer.is_valid():
            # Save the new user instance to the database
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GetTokenView(TokenObtainPairView):
    # Allow any user to access this view without authentication
    permission_classes = [permissions.AllowAny]


class DepartmentListCreateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    
    def get(self, request):
        # Retrieve all Department instances from the database
        departments = Department.objects.all()
        serializer = DepartmentSerializer(departments, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = DepartmentSerializer(data=request.data)
        if serializer.is_valid():
            # Save the new Department instance with the submitted_by field set to the current user
            serializer.save(submitted_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class DepartmentRetrieveUpdateDestroyAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, pk):
        # Retrieve the Department instance by its primary key or return a 404 error if not found
        department = get_object_or_404(Department, pk=pk)
        serializer = DepartmentSerializer(department)
        return Response(serializer.data)

    def put(self, request, pk):
        # Retrieve the Department instance by its primary key or return a 404 error if not found
        department = get_object_or_404(Department, pk=pk)
        serializer = DepartmentSerializer(department, data=request.data)
        if serializer.is_valid():
            # Update the Department instance with the new data
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        # Retrieve the Department instance by its primary key or return a 404 error if not found
        department = get_object_or_404(Department, pk=pk)
        serializer = DepartmentSerializer(department, data=request.data, partial=True)
        if serializer.is_valid():
            # Update the Department instance with the new data
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

   
    
class StudentListCreateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        # Retrieve all Students instances from the database
        students = Students.objects.all()
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            # Save the new Students instance with the submitted_by field set to the current user
            serializer.save(submitted_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class StudentRetrieveUpdateDestroyAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, pk):
        # Retrieve the Students instance by its primary key or return a 404 error if not found
        student = get_object_or_404(Students, pk=pk)
        serializer = StudentSerializer(student)
        return Response(serializer.data)

    def put(self, request, pk):
        # Retrieve the Students instance by its primary key or return a 404 error if not found
        student = get_object_or_404(Students, pk=pk)
        serializer = StudentSerializer(student, data=request.data)
        if serializer.is_valid():
            # Update the Courses instance with the new data
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        # Retrieve the Students instance by its primary key or return a 404 error if not found
        student = get_object_or_404(Students, pk=pk)
        serializer = StudentSerializer(student, data=request.data, partial=True)
        if serializer.is_valid():
            # Update the Students instance with the new data
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

   
    
    
class CourseListCreateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        # Retrieve all Courses instances from the database
        courses = Courses.objects.all()
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CourseSerializer(data=request.data)
        if serializer.is_valid():
            # Save the new log instance with the submitted_by field set to the current user
            serializer.save(submitted_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class CourseRetrieveUpdateDestroyAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, pk):
        # Retrieve the Courses instance by its primary key or return a 404 error if not found
        course = get_object_or_404(Courses, pk=pk)
        serializer = CourseSerializer(course)
        return Response(serializer.data)

    def put(self, request, pk):
        # Retrieve the Courses instance by its primary key or return a 404 error if not found
        course = get_object_or_404(Courses, pk=pk)
        serializer = CourseSerializer(course, data=request.data)
        if serializer.is_valid():
            # Update the log instance with the new data
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        course = get_object_or_404(Courses, pk=pk)
        serializer = CourseSerializer(course, data=request.data, partial=True)
        if serializer.is_valid():
            # Update the Courses instance with the new data
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

 
    
    

class AttendanceLogListCreateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        # Retrieve all AttendanceLog instances from the database
        logs = AttendanceLog.objects.all()
        serializer = AttendanceLogSerializer(logs, many=True)
        return Response(serializer.data)

    def post(self, request):
        #Initialize the serializer with the request data
        
        serializer = AttendanceLogSerializer(data=request.data)
        if serializer.is_valid():
            # Save the new log instance with the submitted_by field set to the current user
            serializer.save(submitted_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class AttendanceLogRetrieveUpdateDestroyAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, pk):
        # Retrieve the AttendanceLog instance by its primary key or return a 404 error if not found

        log = get_object_or_404(AttendanceLog, pk=pk)
        serializer = AttendanceLogSerializer(log)
        return Response(serializer.data)

    def put(self, request, pk):
        # Retrieve the AttendanceLog instance by its primary key or return a 404 error if not found

        log = get_object_or_404(AttendanceLog, pk=pk)
        serializer = AttendanceLogSerializer(log, data=request.data)
        if serializer.is_valid():
            # Update the log instance with the new data
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        log = get_object_or_404(AttendanceLog, pk=pk)
        serializer = AttendanceLogSerializer(log, data=request.data, partial=True)
        if serializer.is_valid():
            # Update the log instance with the new data
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
