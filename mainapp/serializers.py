from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'type', 'email', 'full_name', 'username', 'password', 'submitted_by']
        
    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            full_name=validated_data.get('full_name', ''),
            username=validated_data.get('username', ''),
            submitted_by=validated_data.get('submitted_by', None),
            is_active=validated_data.get('is_active', True),
            is_staff=validated_data.get('is_staff', False),
            is_admin_user=validated_data.get('is_admin_user', False),
            type=validated_data.get('type', 'student')
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class DepartmentSerializer(serializers.ModelSerializer):
    submitted_by = serializers.StringRelatedField()
    
    class Meta:
        model = Department
        fields = ['id','department_name', 'submitted_by', 'updated_at']
        
        
        
class StudentSerializer(serializers.ModelSerializer):
    submitted_by = serializers.StringRelatedField()
    
    class Meta:
        model = Students
        fields = ['id','full_name', 'department', 'student_class', 'submitted_by', 'updated_at']
     
        


class CourseSerializer(serializers.ModelSerializer):
    submitted_by = serializers.StringRelatedField()
    
    class Meta:
        model = Courses
        fields = ['id','course_name','department', 'course_class', 'semester', 'lecture_hours', 'submitted_by', 'updated_at']
        
   
    
class AttendanceLogSerializer(serializers.ModelSerializer):
    submitted_by = serializers.StringRelatedField()
   
    class Meta:
        model = AttendanceLog
        fields = ['id','student', 'course', 'present', 'submitted_by', 'updated_at']
  