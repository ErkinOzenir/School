from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from core.views import (
    UserLoginView, GroupCreateView, GroupAddStudentView, TeacherScheduleView,
    LessonTransferView, StudentProgressView, LessonDetailView, HomeworkDetailView,
    ExerciseListView, TopicListView
)

urlpatterns = [
    # JWT authentication endpoints
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Application endpoints
    path('group/create/', GroupCreateView.as_view(), name='group-create'),
    path('group/add-student/', GroupAddStudentView.as_view(), name='group-add-student'),
    path('teacher/schedule/', TeacherScheduleView.as_view(), name='teacher-schedule'),
    path('lesson/transfer/', LessonTransferView.as_view(), name='lesson-transfer'),
    path('student/progress/', StudentProgressView.as_view(), name='student-progress'),
    path('lesson/<int:pk>/', LessonDetailView.as_view(), name='lesson-detail'),
    path('homework/<int:pk>/', HomeworkDetailView.as_view(), name='homework-detail'),
    path('exercises/', ExerciseListView.as_view(), name='exercises'),
    path('topics/', TopicListView.as_view(), name='topics'),
]
