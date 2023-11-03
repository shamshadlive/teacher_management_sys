from django.shortcuts import render,redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Teacher,File,Subject
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
from django.template.loader import render_to_string
from django.http import JsonResponse
from .forms import UserForm
from django.http import HttpResponseRedirect
from django.core.files import File as objFile
import os
# Create your views here.


# ==============BASIC AUTH FUNCTION STARTS HERE =================

@login_required(login_url='login-page')
def home (request):
    """ Home page functionality """
    
    teacher_count = Teacher.objects.count()
    context = {'teacher_count':teacher_count}
    return render(request, 'teacher/index.html',context)


def login_Page (request):
    
    """ Login for users """
    
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
    
    """ Register New users """
    
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
    
    """ To view all the teachers """
    
    model = Teacher
    template_name = 'teacher/teacher-view.html'  
    context_object_name = 'teachers'  
    paginate_by = 12  

    def get_queryset(self):
        queryset = Teacher.objects.filter().order_by('-updated_at')
        search_query = self.request.GET.get('search', None)
        if search_query:
            # Filter the queryset based on the search query
            queryset = queryset.filter(Q(teacher_last_name__startswith=search_query)    )
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Add additional context data here
        context['subjects'] = Subject.objects.filter(is_active=True).order_by('sub_name')

        return context
    
def teacher_filter_data(request):
    get_subjects = request.GET.getlist('subject[]')
    

    if get_subjects:
       teachers = Teacher.objects.filter(teacher_subjects__id__in=get_subjects).order_by('-updated_at')
    else:
       teachers = Teacher.objects.all().order_by('-updated_at')

    updated_data = render_to_string('teacher/teacher_data.html', {'teachers': teachers})

    return JsonResponse({'data': updated_data})


class TeacherUpdateView(LoginRequiredMixin,UpdateView):
    
    """ Update details of a single teacher """
    
    model = Teacher
    template_name = 'teacher/teacher-create.html'
    context_object_name = 'teacher'
    fields = '__all__'
    
    def form_valid(self, form):
        selected_subjects = form.cleaned_data.get('teacher_subjects')
        if selected_subjects.count() > 5:
            form.add_error('teacher_subjects', 'You can select a maximum of 5 subjects.')
            return self.form_invalid(form)
        else:
            messages.success(self.request, 'Teacher Updated successfully.')
            return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('teacher-update', kwargs={'pk': self.object.id})
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        for field_name, field in form.fields.items():
            if field_name not in ['is_active']:
                field.widget.attrs['class'] = 'form-control'
        
        return form
    

class TeacherCreateView(LoginRequiredMixin,CreateView):
    
    """ Create a  single teacher """
    
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

        selected_subjects = form.cleaned_data.get('teacher_subjects')
        if selected_subjects.count() > 5:
            form.add_error('teacher_subjects', 'You can select a maximum of 5 subjects.')
            return self.form_invalid(form)
        else:
            messages.success(self.request, 'Teacher Created successfully.')
            return super().form_valid(form)


class TeacherDeleteView(DeleteView):
    """ delete a  single teacher """
    model = Teacher
    success_url = reverse_lazy('all-teacher-view')
    
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return HttpResponseRedirect(self.get_success_url())



class TeacherViewSet(viewsets.ModelViewSet):
    """
    API simple ViewSet for creating , editing teachers.
    
    """
    permission_classes = []
    queryset = Teacher.objects.all()  
    serializer_class = TeacherSerializer
    
    
    
def create_db(file_path):
    """
    File uploading to db to sort out the csv file
    
    """
    df = pd.read_csv(file_path,delimiter=',')
    data = df.dropna(how='all')
    list_of_csv = [list(row) for row in data.values] 
    
    for teacher in list_of_csv:
        if str(teacher[0]) !='nan': 
            try:
                teacher_obj = Teacher.objects.create(
                    teacher_first_name=teacher[0],
                    teacher_last_name=teacher[1],
                    # teacher_profile_pic=teacher[2],
                    teacher_email=teacher[3],
                    teacher_phone_number=teacher[4],
                    teacher_room=teacher[5],
                )
                
                # image_filename = teacher[2]
               
                # if image_filename and os.path.exists(image_filename):
                #     with open(image_filename, 'rb') as image_file:
                #         teacher_obj.teacher_profile_pic.save(image_filename, objFile(image_file), save=True)
                        
                
                #setting subject by checking the count 
                subject_names = [subject.strip() for subject in teacher[6].split(',')]
               
                if len(subject_names) <= 5 :
                    for subject in subject_names:
                       
                        item = Subject.objects.filter(sub_name__istartswith=subject).exists()
                        if item:
                            sub= Subject.objects.filter(sub_name__istartswith=subject).first()
                            teacher_obj.teacher_subjects.add(sub)
                    
                    
            except Exception as e:
                print(e)
                continue
                return False
    return True
            
@login_required             
def csv_upload(request):
    """
    CSV file uplaod handled here
    
    """
    if request.method == "POST":
        file = request.FILES['file']
        obj = File.objects.create(file=file)
        created = create_db(obj.file)
        
        if not created:
            messages.error(request, 'Please check the csv data uploaded')
            return redirect('all-teacher-view')
        
    messages.success(request, 'Teachers Created successfully.')
    return redirect('all-teacher-view')




class SubjectCreateView(LoginRequiredMixin,CreateView):
    
    """ Create a  Subject """
    
    model = Subject
    template_name = 'teacher/subject-create.html'
    fields = '__all__'
    success_url = reverse_lazy('all-teacher-view')
  
    def get_form(self, form_class=None):
            form = super().get_form(form_class)
            for field_name, field in form.fields.items():
                if field_name not in ['is_active']:
                    field.widget.attrs['class'] = 'form-control'
            
            return form
        
    def form_valid(self, form):
            messages.success(self.request, 'Subject Created successfully.')
            return super().form_valid(form)

