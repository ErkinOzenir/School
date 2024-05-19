from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .models import User, Group, Student, Lesson, Homework, Exercise, Topic
from .serializers import UserSerializer, GroupSerializer, StudentSerializer, LessonSerializer, HomeworkSerializer, ExerciseSerializer, TopicSerializer

# User Login View
class UserLoginView(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': UserSerializer(user).data
            })
        return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)

# Group Create View
class GroupCreateView(generics.CreateAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(teacher=self.request.user)

# Group Add Student View
class GroupAddStudentView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        student_id = request.data.get('student_id')
        group_code = request.data.get('group_code')
        try:
            student = Student.objects.get(user__id=student_id)
            group = Group.objects.get(code=group_code)
            student.group = group
            student.save()
            return Response({'status': 'Student added to group'})
        except (Student.DoesNotExist, Group.DoesNotExist):
            return Response({'error': 'Invalid student ID or group code'}, status=status.HTTP_400_BAD_REQUEST)

# Teacher Schedule View
class TeacherScheduleView(generics.ListAPIView):
    serializer_class = LessonSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_teacher:
            return Lesson.objects.filter(group__teacher=user)
        return Lesson.objects.none()

# Lesson Transfer View
class LessonTransferView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        lesson_id = request.data.get('lesson_id')
        new_teacher_id = request.data.get('new_teacher_id')
        try:
            lesson = Lesson.objects.get(id=lesson_id)
            new_teacher = User.objects.get(id=new_teacher_id, is_teacher=True)
            lesson.group.teacher = new_teacher
            lesson.group.save()
            return Response({'status': 'Lesson transferred to new teacher'})
        except (Lesson.DoesNotExist, User.DoesNotExist):
            return Response({'error': 'Invalid lesson ID or teacher ID'}, status=status.HTTP_400_BAD_REQUEST)

# Student Progress View
class StudentProgressView(generics.RetrieveAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Student.objects.filter(user=self.request.user)

# Lesson Detail View
class LessonDetailView(generics.RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [permissions.IsAuthenticated]

# Homework Detail View
class HomeworkDetailView(generics.RetrieveAPIView):
    queryset = Homework.objects.all()
    serializer_class = HomeworkSerializer
    permission_classes = [permissions.IsAuthenticated]

# Exercise List View
class ExerciseListView(generics.ListAPIView):
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        lesson_id = self.request.query_params.get('lesson_id')
        if lesson_id:
            return Exercise.objects.filter(lesson__id=lesson_id)
        return Exercise.objects.none()

# Topic List View
class TopicListView(generics.ListAPIView):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Topic.objects.all()
