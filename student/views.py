from django.shortcuts import render,redirect


from django.views.generic import View,TemplateView,FormView,CreateView

from student.forms import StudentCreateForm,LoginForm

from django.contrib.auth import authenticate,login

from django.urls import reverse_lazy,reverse

from instructor.models import Course,Cart,Order,Lesson,Module

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

       purchased_courses=Order.objects.filter(student=request.user).values_list("course_objects",flat=True)
       print(purchased_courses,"=========================")      
      

       return render(request,"home.html",{"courses":all_courses,"purchased_courses":purchased_courses})
   

# localhost:8000/student/courses/2

class CourseDetailView(View):

    def get(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        course_instance=Course.objects.get(id=id)

        return render(request,"course_retrieve.html",{"course":course_instance})

# url:localhost:8000/student/courses/2/add-to-cart/


class AddToCartView(View):

    def get(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        course_instance=Course.objects.get(id=id)

       

        user_instance=request.user

        # Cart.objects.create(course_object=course_instance,user=user_instance)

        cart_instance,created=Cart.objects.get_or_create(course_object=course_instance,user=user_instance)
        print(created,"=====================")
        return redirect("index")



# url:localhost:8000/student/cart-summary/
# CartSummaryView

from django.db.models import Sum

class CartSummaryView(View):


    def get(self,request,*args,**kwargs):

        qs=request.user.basket.all()
        # qs=Cart.objects.filter(user=request.user)

        cart_total=qs.values("course_object__price").aggregate(total=Sum("course_object__price")).get("total")


        print(cart_total,"*************************")#{"total":59999}

       


        return render(request,"cart-summary.html",{"carts":qs,"basket_total":cart_total})
    

# localhost:8000/student//carts/2/remove/

class CartItemDeleteView(View):

    def get(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        Cart.objects.get(id=id).delete()

        return redirect("cart-summary")
    


class CheckOutView(View):

    def get(self,request,*args,**kwargs):

        cart_items=request.user.basket.all()

        order_total=sum([ci.course_object.price for ci in cart_items])


        order_instance=Order.objects.create(student=request.user,total=order_total)

        for ci in cart_items:

            order_instance.course_objects.add(ci.course_object)

            ci.delete()
        
        order_instance.save()

        
        return redirect("index")

class MyCoursesView(View):

    def get(self,request,*args,**kwargs):

        qs=request.user.purchase.all()

        return render(request,"mycourses.html",{"orders":qs})
    
# localhost:8000/student/courses?category=webdevelopent
# requet.GET {category:webdevelopent}

# localhost:8000/students/courses/1/watch?module=1&lesson=5
#?optional  query parameter

class LessonDetailView(View):

    def get(self,request,*args,**kwargs):

        course_id=kwargs.get("pk")

        course_instance=Course.objects.get(id=course_id)
        # request.GET={"module":2,"lesson":2}

        module_id=request.GET.get("module") if "module" in request.GET else course_instance.modules.all().first()


        module_instance=Module.objects.get(id=module_id,course_object=course_instance)
        
        lesson_id=request.GET.get("lesson") if "lesson" in request.GET else module_instance.lessons.all().first()

        lesson_instance=Lesson.objects.get(id=lesson_id,module_object=module_instance)

        return render(request,"lesson_detail.html",{"course":course_instance,"lesson":lesson_instance})








        





   











        

