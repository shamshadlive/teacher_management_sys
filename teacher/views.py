from django.shortcuts import render,redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Teacher,File
from django.db.models import Q
from rest_framework.generics import CreateAPIView
from django.contrib.auth import logout,authenticate,login
from .serializers import TeacherSerializer
from django.urls import reverse,reverse_lazy
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from django.contrib import messages
import pandas as pd
from accounts.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import UserForm
# Create your views here.


# ==============BASIC AUTH FUNCTION STARTS HERE =================

@login_required(login_url='login-page')
def home (request):
    
    teacher_count = Teacher.objects.count()
    context = {'teacher_count':teacher_count}
    return render(request, 'teacher/index.html',context)


def login_Page (request):
    if request.user.is_authenticated:
        return redirect('/')
    
    if request.method =='POST':
        phone_number = request.POST.get('phone_number')
        password = request.POST.get('password')
        
        if not User.objects.filter(phone_number=phone_number).exists():
            messages.error(request, "Invalid Phone Number")
            return redirect('login-page')
        
        if not User.objects.filter(phone_number=phone_number,is_active=True).exists():
            messages.error(request, "You are blocked by admin ! Please contact admin")
            return redirect('login-page')
        
        
        user = authenticate(username=phone_number,password=password)
        if user is None:
            messages.error(request, "Invalid Password")
            return redirect('login-page')
        else:
            messages.success(request, f'Welcome Back {user.first_name}')
            login(request,user)
            return redirect('home')
        
    return render(request, 'teacher/login.html')


class register_Page(CreateView):
    model = User
    form_class = UserForm
    template_name = 'teacher/register.html'
    success_url = reverse_lazy('login-page')
    
    def form_valid(self, form):
        messages.success(self.request, 'Registration successful. You can now log in.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Registration failed. Please correct the errors')
        return super().form_invalid(form)
    
    
    

def logout_Page(request):
    logout(request)
    return redirect('login-page')



# ==============MANAGEMENT STARTS HERE =================

class TeacherView(LoginRequiredMixin,ListView):
    model = Teacher
    template_name = 'teacher/teacher-view.html'  
    context_object_name = 'teachers'  
    paginate_by = 12  

    def get_queryset(self):
        queryset = Teacher.objects.filter().order_by('-updated_at')
        search_query = self.request.GET.get('search', None)
        if search_query:
            # Filter the queryset based on the search query
            queryset = queryset.filter(Q(tchr_last_name__startswith=search_query)    )
        
        return queryset
  

class TeacherUpdateView(LoginRequiredMixin,UpdateView):
    model = Teacher
    template_name = 'teacher/teacher-create.html'
    context_object_name = 'teacher'
    fields = '__all__'
    
    def form_valid(self, form):
        # Perform any additional actions here if needed
        messages.success(self.request, 'Teacher details updated successfully.')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('teacher-update', kwargs={'pk': self.object.id})
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        for field_name, field in form.fields.items():
            if field_name not in ['is_active']:
                field.widget.attrs['class'] = 'form-control'
        
        return form
    
 #create state 
class TeacherCreateView(LoginRequiredMixin,CreateView):
    model = Teacher
    template_name = 'teacher/teacher-create.html'
    fields = '__all__'
    success_url = reverse_lazy('all-teacher-view')
  
    def get_form(self, form_class=None):
            form = super().get_form(form_class)
            for field_name, field in form.fields.items():
                if field_name not in ['is_active']:
                    field.widget.attrs['class'] = 'form-control'
            
            return form
        
    def form_valid(self, form):

        messages.success(self.request, 'Teacher Created successfully.')
        return super().form_valid(form)


class TeacherViewSet(viewsets.ModelViewSet):
    """
    API simple ViewSet for creating , editing teachers.
    
    """
    permission_classes = []
    queryset = Teacher.objects.all()  # Define the queryset for the viewset.
    serializer_class = TeacherSerializer
    
    
    
def create_db(file_path):
    """
   File uploading to db
    
    """
    df = pd.read_csv(file_path,delimiter=',')
    data = df.dropna(how='all')
    list_of_csv = [list(row) for row in data.values] 
    print(list_of_csv)
    
    for teacher in list_of_csv:
        if str(teacher[0]) !='nan': 
            try:
                Teacher.objects.create(
                    teacher_first_name=teacher[0],
                    teacher_last_name=teacher[1],
                    # teacher_profile_pic=teacher[3],
                    teacher_email=teacher[3],
                    teacher_phone_number=teacher[4],
                    teacher_room=teacher[5],
                    teacher_subjects=teacher[6],
                )
            except Exception as e:
                messages.error(request, f'Invalid data {teacher[0]} Not uploaded')
                
@login_required             
def csv_upload(request):
    """
   File upload
    
    """
    if request.method == "POST":
        file = request.FILES['file']
        obj = File.objects.create(file=file)
        create_db(obj.file)
        
    messages.success(request, 'Teachers Created successfully.')
    return redirect('all-teacher-view')