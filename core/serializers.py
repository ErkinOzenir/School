from rest_framework import serializers
from .models import User, Group, Student, Lesson, Homework, Exercise, Topic

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_teacher', 'is_student']

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name', 'level', 'code', 'teacher', 'lessons_per_week', 'lesson_time']

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'user', 'group', 'progress']

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'group', 'topic', 'description', 'date', 'is_online']

class HomeworkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Homework
        fields = ['id', 'lesson', 'due_date', 'description']

class ExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise
        fields = ['id', 'lesson', 'question', 'options', 'correct_option', 'is_correct']

class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = ['id', 'name', 'description', 'pdf']
