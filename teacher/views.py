from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Teacher
from django.db.models import Q
from rest_framework.generics import CreateAPIView
from .serializers import TeacherSerializer
from django.urls import reverse,reverse_lazy
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from django.contrib import messages
# Create your views here.
def home (request):
    
    return render(request, 'teacher/index.html')


class TeacherView(ListView):
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
  

class TeacherUpdateView(UpdateView):
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
class TeacherCreateView(CreateView):
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
    A simple ViewSet for creating , editing teachers.
    
    """
    permission_classes = []
    queryset = Teacher.objects.all()  # Define the queryset for the viewset.
    serializer_class = TeacherSerializer
    
    # def list(self, request):
    #     queryset = Teacher.objects.all()
    #     serializer = TeacherSerializer(queryset, many=True)
    #     return Response(serializer.data)

    # def retrieve(self, request, pk=None):
    #     queryset = Teacher.objects.all()
    #     teacher = get_object_or_404(queryset, pk=pk)
    #     serializer = TeacherSerializer(teacher)
    #     return Response(serializer.data)
    
    # def create(self, request):
    #     serializer = TeacherSerializer(data=request.data)
        
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
        
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # def update(self, request, pk=None):
    #     queryset = Teacher.objects.all()
    #     teacher = get_object_or_404(queryset, pk=pk)
        
    #     serializer = TeacherSerializer(teacher, data=request.data, partial=True)
        
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
        
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    