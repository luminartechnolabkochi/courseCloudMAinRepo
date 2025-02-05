from django.shortcuts import render,redirect


from django.views.generic import View,TemplateView,FormView,CreateView

from student.forms import StudentCreateForm,LoginForm

from django.contrib.auth import authenticate,login

from django.urls import reverse_lazy,reverse

from instructor.models import Course

class StudentRegistrationView(CreateView):

    template_name="student_register.html"

    form_class=StudentCreateForm

    success_url=reverse_lazy("signin")



class SignInView(FormView):

    template_name="signin.html"

    form_class=LoginForm

    def post(self,request,*args,**kwargs):

        form_data=request.POST

        form_instance=self.form_class(form_data)

        if form_instance.is_valid():

            data=form_instance.cleaned_data #{}

            uname=data.get("username")

            pwd=data.get("password")

            user_instance=authenticate(request,username=uname,password=pwd)

            if user_instance:

                login(request,user_instance)

                return redirect("index")
            
            else:

                return render(request,self.template_name,{"form":form_instance})

                



class IndexView(View):

   def get(self,request,*args,**kwargs):
       
       all_courses=Course.objects.all()

       return render(request,"home.html",{"courses":all_courses})
   

# localhost:8000/student/courses/2

class CourseDetailView(View):

    def get(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        course_instance=Course.objects.get(id=id)

        return render(request,"course_retrieve.html",{"course":course_instance})