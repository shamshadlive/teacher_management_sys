from django.urls import path, include
from .import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'teachers', views.TeacherViewSet, basename='teacher')

urlpatterns = [
    path("", views.home, name="home"),
    path("teachers/", views.TeacherView.as_view(), name="all-teacher-view"),
    path("teachers/update/<int:pk>/", views.TeacherUpdateView.as_view(), name="teacher-update"),
    path("teachers/create/", views.TeacherCreateView.as_view(), name="teacher-create"),
    path('api/', include(router.urls)),
    ]