from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from mainapp.models import *
from rest_framework.test import APITestCase, APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from mainapp.serializers import *

User = get_user_model()

class UserCreateAPIViewTests(APITestCase):
    
    def setUp(self):
        # Optional: Create any setup data or users needed for tests
        pass

    def test_create_user_success(self):
        url = reverse('user-create')  # Ensure this matches your URL configuration
        data = {
            'email': 'testuser@example.com',
            'full_name': 'Test User',
            'username': 'testuser',
            'password': 'testpassword',
            'type': 'student',  # Adjust this field based on your model's choices
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().email, 'testuser@example.com')

    def test_create_user_missing_field(self):
        url = reverse('user-create')  # Ensure this matches your URL configuration
        data = {
            'email': 'testuser@example.com',
            'username': 'testuser',
            # Missing required fields like 'password'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data)

    def test_create_user_invalid_email(self):
        url = reverse('user-create')  # Ensure this matches your URL configuration
        data = {
            'email': 'invalid-email',
            'full_name': 'Test User',
            'username': 'testuser',
            'password': 'testpassword',
            'type': 'student',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)

    def test_create_user_duplicate_email(self):
        # First, create a user
        User.objects.create_user(
            email='testuser@example.com',
            full_name='Test User',
            username='testuser',
            password='testpassword'
        )
        url = reverse('user-create')  # Ensure this matches your URL configuration
        data = {
            'email': 'testuser@example.com',  # Duplicate email
            'full_name': 'Another User',
            'username': 'anotheruser',
            'password': 'anotherpassword',
            'type': 'teacher',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)
        


class DepartmentListCreateAPIViewTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(email='testuser@gmail.com', password='testpassword')
        self.client = APIClient()

        # Obtain the JWT token for the test user
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        self.url = reverse('department-list-create') 

    def test_list_departments(self):
        # Create a department
        Department.objects.create(
            department_name='Science',
            submitted_by=self.user
        )
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['department_name'], 'Science')

    def test_create_department_success(self):
        data = {
            'department_name': 'Mathematics',
            'submitted_by': self.user.id  # Ensure this matches the field name in your serializer
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Department.objects.count(), 1)
        self.assertEqual(Department.objects.get().department_name, 'Mathematics')

    def test_create_department_missing_field(self):
        data = {
            # Missing 'department_name'
            'submitted_by': self.user.id
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('department_name', response.data)

    def test_create_department_unauthorized(self):
        # Logout the user
        self.client.logout()
        data = {
            'department_name': 'Biology',
            'submitted_by': self.user.id
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)




class DepartmentRetrieveUpdateDestroyAPIViewTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(email='testuser@gmail.com', password='testpassword')
        self.client = APIClient()

        # Obtain the JWT token for the test user
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

        # Create a test department
        self.department = Department.objects.create(
            department_name='Science',
            submitted_by=self.user
        )
        self.url = reverse('department-detail', kwargs={'pk': self.department.pk})  # Ensure this matches your URL configuration

    def test_retrieve_department(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['department_name'], 'Science')

    def test_update_department(self):
        data = {
            'department_name': 'Mathematics'
        }
        response = self.client.put(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.department.refresh_from_db()
        self.assertEqual(self.department.department_name, 'Mathematics')

    def test_partial_update_department(self):
        data = {
            'department_name': 'Biology'
        }
        response = self.client.patch(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.department.refresh_from_db()
        self.assertEqual(self.department.department_name, 'Biology')


    def test_retrieve_department_unauthorized(self):
        # Logout the user
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_department_unauthorized(self):
        # Logout the user
        self.client.logout()
        data = {
            'department_name': 'Updated Department'
        }
        response = self.client.put(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        
        


class StudentListCreateAPIViewTest(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(email='testuser@gmail.com', password='testpassword')
        self.client = APIClient()

        # Obtain the JWT token for the test user
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        self.department = Department.objects.create(department_name='Computer Science')

        self.url = reverse('student-list-create')  # Ensure this matches the name of your URL pattern

    def test_get_student_list(self):
        # Create some student instances for testing
        student1 = Students.objects.create(full_name='John Doe',student_class=1,department=self.department,submitted_by=self.user)
        student2 = Students.objects.create(full_name='Jane Smith',student_class=1, department=self.department,submitted_by=self.user)

        response = self.client.get(self.url)
        students = Students.objects.all()
        serializer = StudentSerializer(students, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_create_student_success(self):
        # Ensure `self.department` is set up correctly in setUp
        data = {
            'full_name': 'New Student',
            'department': self.department.id,  # Ensure `self.department` is created in `setUp`
            'student_class': 1
        }
        response = self.client.post(self.url, data, format='json')
        
        # Verify response status
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Verify the response data
        self.assertEqual(response.data['full_name'], data['full_name'])
        self.assertEqual(response.data['department'], data['department'])
        self.assertEqual(response.data['student_class'], data['student_class'])
        
        # Verify that a new student instance was created
        self.assertEqual(Students.objects.count(), 1)
        new_student = Students.objects.first()
        self.assertEqual(new_student.full_name, data['full_name'])
        self.assertEqual(new_student.department.id, data['department'])
        self.assertEqual(new_student.student_class, data['student_class'])


    def test_create_student_missing_name(self):
        data = {
            'age': 18,
            'department': self.department.id
        }
        response = self.client.post(self.url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('full_name', response.data)

    def test_create_student_unauthenticated(self):
        # Remove the credentials to simulate an unauthenticated request
        self.client.credentials()

        data = {
            'full_name': 'New Student',
            'department': self.department.id
        }
        response = self.client.post(self.url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        
        
        
        
class StudentRetrieveUpdateDestroyAPIViewTest(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(email='testuser@gmail.com', password='testpassword')
        self.client = APIClient()

        # Obtain the JWT token for the test user
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

        self.department = Department.objects.create(department_name='Computer Science')  # Create a department
        self.student = Students.objects.create(
            full_name='John Doe',
            student_class=1,
            department=self.department,
            submitted_by=self.user
        )
        self.url = reverse('student-detail', kwargs={'pk': self.student.pk})  # Ensure this matches the name of your URL pattern

    def test_get_student(self):
        response = self.client.get(self.url)
        student = Students.objects.get(pk=self.student.pk)
        serializer = StudentSerializer(student)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_update_student_put(self):
        data = {
            'full_name': 'John Doe Updated',
            'student_class': 2,
            'department': self.department.id,
        }
        response = self.client.put(self.url, data, format='json')

        self.student.refresh_from_db()  # Refresh the student instance from the database
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.student.full_name, data['full_name'])
        self.assertEqual(self.student.student_class, data['student_class'])

    def test_partial_update_student_patch(self):
        data = {
            'full_name': 'John Doe Patched'
        }
        response = self.client.patch(self.url, data, format='json')

        self.student.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.student.full_name, data['full_name'])


    def test_get_student_not_found(self):
        url = reverse('student-detail', kwargs={'pk': 9999})  # Non-existent PK
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_student_unauthenticated(self):
        self.client.credentials()  # Remove authentication
        data = {
            'full_name': 'John Doe Updated',
            'student_class': 2,
            'department': self.department.id,
        }
        response = self.client.put(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)





class CourseListCreateAPIViewTest(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(email='testuser@gmail.com', password='testpassword')
        self.client = APIClient()

        # Obtain the JWT token for the test user
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        
        self.department = Department.objects.create(department_name='Computer Science')

        self.url = reverse('course-list-create')  # Ensure this matches the name of your URL pattern

    def test_get_course_list(self):
        # Create some course instances for testing
        course1 = Courses.objects.create(
            course_name='Mathematics',
            submitted_by=self.user,
            course_class=1,
            semester=1,
            lecture_hours=1,
            department=self.department
        )
        course2 = Courses.objects.create(
            course_name='Physics',
            submitted_by=self.user,
            course_class=1,
            semester=1,
            lecture_hours=1,
            department=self.department
        )

        response = self.client.get(self.url)
        courses = Courses.objects.all()
        serializer = CourseSerializer(courses, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_create_course_success(self):
        # Ensure `self.department` is set up correctly in setUp
        data = {
            'course_name': 'Chemistry',
            'department': self.department.id,  # Ensure `self.department` is created in `setUp`
            'course_class': 1,
            'semester': 1,
            'lecture_hours': 1
        }
        response = self.client.post(self.url, data, format='json')

        # Verify response status
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Verify the response data
        self.assertEqual(response.data['course_name'], data['course_name'])
        self.assertEqual(response.data['department'], data['department'])
        self.assertEqual(response.data['course_class'], data['course_class'])
        self.assertEqual(response.data['semester'], data['semester'])
        self.assertEqual(response.data['lecture_hours'], data['lecture_hours'])
        
        # Verify that a new course instance was created
        self.assertEqual(Courses.objects.count(), 1)
        new_course = Courses.objects.first()
        self.assertEqual(new_course.course_name, data['course_name'])
        self.assertEqual(new_course.department.id, data['department'])
        self.assertEqual(new_course.course_class, data['course_class'])
        self.assertEqual(new_course.semester, data['semester'])
        self.assertEqual(new_course.lecture_hours, data['lecture_hours'])

    def test_create_course_missing_name(self):
        data = {
            'description': 'A course with no name'
        }
        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('course_name', response.data)

    def test_create_course_unauthenticated(self):
        # Remove the credentials to simulate an unauthenticated request
        self.client.credentials()

        data = {
            'course_name': 'Biology',
        }
        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)




class CourseRetrieveUpdateDestroyAPIViewTest(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(email='testuser@gmail.com', password='testpassword')
        self.client = APIClient()

        # Obtain the JWT token for the test user
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        self.department = Department.objects.create(department_name='Computer Science')

        self.course = Courses.objects.create(
            course_name='Mathematics',
            submitted_by=self.user,
            course_class=1,
            semester=1,
            lecture_hours=1,
            department=self.department
        )
        
        self.url = reverse('course-detail', kwargs={'pk': self.course.pk})  # Ensure this matches the name of your URL pattern

    def test_get_course(self):
        response = self.client.get(self.url)
        course = Courses.objects.get(pk=self.course.pk)
        serializer = CourseSerializer(course)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_update_course_put(self):
        data = {
            'course_name': 'Mathematics Advanced',
            'course_class': 1,
            'submitted_by': self.user.id,
            'semester': 1,
            'lecture_hours':1,
            'department':self.department.id
            
        }
        
        response = self.client.put(self.url, data, format='json')

        self.course.refresh_from_db()  # Refresh the course instance from the database
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.course.course_name, data['course_name'])

    def test_partial_update_course_patch(self):
        data = {
            'course_class': 1
        }
        response = self.client.patch(self.url, data, format='json')

        self.course.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.course.course_class, data['course_class'])


    def test_get_course_not_found(self):
        url = reverse('course-detail', kwargs={'pk': 9999})  # Non-existent PK
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_course_unauthenticated(self):
        self.client.credentials()  # Remove authentication
        data = {
            'course_name': 'Unauthorized Update',
            'course_class': 1
        }
        response = self.client.put(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)





class AttendanceLogListCreateAPIViewTest(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(email='testuser@gmail.com', password='testpassword')
        self.client = APIClient()

        # Obtain the JWT token for the test user
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        self.department = Department.objects.create(department_name='Computer Science')
        
        self.student = Students.objects.create(full_name='John Doe',student_class=1,department=self.department,submitted_by=self.user)
        
        self.student1 = Students.objects.create(full_name='hennery',student_class=1,department=self.department,submitted_by=self.user)
        self.course = Courses.objects.create(
            course_name='Mathematics',
            submitted_by=self.user,
            course_class=1,
            semester=1,
            lecture_hours=1,
            department=self.department
        )

        self.url = reverse('attendance-log-list-create')  # Ensure this matches the name of your URL pattern

    def test_get_attendance_log_list(self):
        # Create some attendance logs for testing
        log1 = AttendanceLog.objects.create(
            student=self.student,
            present=True,
            submitted_by=self.user,
            course=self.course
        )
        log2 = AttendanceLog.objects.create(
            student=self.student1,
            present=False,
            submitted_by=self.user,
            course=self.course
        )

        response = self.client.get(self.url)
        logs = AttendanceLog.objects.all()
        serializer = AttendanceLogSerializer(logs, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_create_attendance_log_success(self):
        data = {
            'student': 'New Student',
            'present': True,
            'student': self.student.id,
            'submitted_by': self.user.id,
            'course': self.course.id
        }
        
        
        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['student'], data['student'])
        self.assertEqual(response.data['present'], data['present'])
        self.assertEqual(AttendanceLog.objects.count(), 1)



    def test_create_attendance_log_unauthenticated(self):
        # Remove the credentials to simulate an unauthenticated request
        self.client.credentials()

        data = {
            'student_name': 'Unauthorized Student',
            'status': 'Absent'
        }
        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        
        
        
class AttendanceLogRetrieveUpdateDestroyAPIViewTest(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(email='testuser@gmail.com', password='testpassword')
        self.client = APIClient()

        # Obtain the JWT token for the test user
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

        self.department = Department.objects.create(department_name='Computer Science')
        
        self.student = Students.objects.create(full_name='John Doe',student_class=1,department=self.department,submitted_by=self.user)
        self.course = Courses.objects.create(
            course_name='Mathematics',
            submitted_by=self.user,
            course_class=1,
            semester=1,
            lecture_hours=1,
            department=self.department
        )
        
        self.attendance_log = AttendanceLog.objects.create(
            student=self.student,
            present=True,
            submitted_by=self.user,
            course=self.course
        )
        self.url = reverse('attendance-log-detail', kwargs={'pk': self.attendance_log.pk})  # Ensure this matches the name of your URL pattern

    def test_get_attendance_log(self):
        response = self.client.get(self.url)
        log = AttendanceLog.objects.get(pk=self.attendance_log.pk)
        serializer = AttendanceLogSerializer(log)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_update_attendance_log_put(self):
        # Prepare data for the PUT request
        data = {
            'student': self.student.id,
            'present': True,
            'course': self.course.id
        }
        response = self.client.put(self.url, data, format='json')
        self.attendance_log.refresh_from_db()
        
        # Verify response status
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.attendance_log.student, self.student) 
        self.assertEqual(self.attendance_log.present, data['present'])
        self.assertEqual(self.attendance_log.course, self.course)  


    def test_partial_update_attendance_log_patch(self):
        data = {
            'present': True
        }
        response = self.client.patch(self.url, data, format='json')

        self.attendance_log.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.attendance_log.present, data['present'])


    def test_get_attendance_log_not_found(self):
        url = reverse('attendance-log-detail', kwargs={'pk': 9999})  # Non-existent PK
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        
    def test_update_attendance_log_unauthenticated(self):
        self.client.credentials()
        # Prepare data for the PUT request
        data = {
            'student': self.attendance_log.student.id,  
            'present': True,
            'course': self.attendance_log.course.id
        }
        
        response = self.client.put(self.url, data, format='json')

        # Verify that the response status is unauthorized
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
