from django.urls import path, include
from .import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'teachers', views.TeacherViewSet, basename='teacher')

urlpatterns = [
    path("", views.home, name="home"),
    path("login/", views.login_Page, name="login-page"),
    path("logout/", views.logout_Page, name="logout-page"),
    path("register/", views.register_Page.as_view(), name="register-page"),
    
    
    path("bulk/upload", views.csv_upload, name="file-upload"),
    path("teachers/", views.TeacherView.as_view(), name="all-teacher-view"),
    path("teachers/update/<int:pk>/", views.TeacherUpdateView.as_view(), name="teacher-update"),
    path("teachers/create/", views.TeacherCreateView.as_view(), name="teacher-create"),
    path('api/', include(router.urls)),
    ]