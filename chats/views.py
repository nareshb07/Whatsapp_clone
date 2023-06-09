from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse,Http404,HttpResponseRedirect

from .models import  User
from django.views import generic



from django.urls import reverse 


class LandingPageView(generic.TemplateView):

    
    template_name = "landing.html"








# Create your views here.



# ...


from django.contrib.auth import login, authenticate, logout
from django.shortcuts import redirect, render
from django.contrib import messages
from django.views.generic import CreateView
from .forms import FollowerSignUpForm, CreatorSignUpForm
from django.contrib.auth.forms import AuthenticationForm
from .models import User

def register(request):
    return render(request, '../templates/register.html')

class Follower_register(CreateView):
    model = User
    form_class = FollowerSignUpForm
    template_name = '../templates/Follower_register.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user, backend='chats.authentication.EmailAuthBackend')
        return redirect('/')

class Creator_register(CreateView):
    model = User
    form_class = CreatorSignUpForm
    template_name = '../templates/creator_register.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user,backend='chats.authentication.EmailAuthBackend')
        return redirect('/')    


def login_request(request):
    if request.method=='POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(email=email, password=password)
            if user is not None :
                if user.is_active:
                    login (request, user,backend='chats.authentication.EmailAuthBackend')
                    return redirect('/')
                else:
                    return HttpResponse('Disabled Account')
                
                
            else:
                messages.error(request,"Invalid username or password")
        else:
                messages.error(request,"Invalid username or password")
    return render(request, '../templates/login.html',
    context={'form':AuthenticationForm()})

def Logout(request):
    logout(request)
    return redirect('/')


from django.contrib.auth.password_validation import validate_password
#from .validator import CustomPasswordValidator 
#validate_password = CustomPasswordValidator() 

def ChangePassword(request , token):
    
    context = {}
    
    try:
        profile_obj = get_object_or_404(User, token = token)
        context = {'user_id' : profile_obj.id}
        
   
        if request.method == 'POST':
            
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('reconfirm_password')
            user_id = request.POST.get('user_id')
            
            if user_id is  None:
                messages.success(request, 'No user id found.')
                return redirect(f'/chats/change-password/{token}/')
                
            
            if  new_password != confirm_password:
                messages.success(request, 'both should  be equal.')
                return redirect(f'/chats/change-password/{token}/')
            
            try:
                validate_password(new_password, profile_obj)
            except Exception as e:
                for error in e:

                #messages.success(request, e)
                #return redirect(f'/chats/change-password/{token}/')
                    messages.success(request, error)
                    return redirect(f'/chats/change-password/{token}/') 


            ### validation problem hai                       
            
            user_obj = User.objects.get(id = user_id)
            user_obj.set_password(new_password)
            user_obj.token = ""
            user_obj.save()
            messages.success(request, "Login with new password id")
            return redirect('/chats/login/') 
               
    except Exception as e:
       #print(e,"hello")

       raise Http404("url not found")
    

    
    return render(request , 'change-password.html' , context)


import uuid
from .helper import send_forget_password_mail


def ForgetPassword(request):
    try:
        if request.method == 'POST':
            email = request.POST.get('username')

            if not email :
                messages.success(request, 'Please Enter email')
                return redirect('/chatss/forget-password/')
                
            
            if not User.objects.filter(email=email).first():
                
                messages.success(request, 'No user found with this username.')
                return redirect('/chats/forget-password/')
            
            user_obj = User.objects.get(email=email)
            token = str(uuid.uuid4())
            profile_obj= User.objects.get(email = user_obj)
            profile_obj.token = token
            profile_obj.save()
            send_forget_password_mail(user_obj.email , token)
            messages.success(request, 'An email is sent.')
            return redirect('/chats/forget-password/')
            
            #Cannot resolve keyword 'user' into field. Choices are: creator, email,
            #first_name, follower, groups, id, is_Creator, is_Follower, is_active, is_staff,
            #is_superuser, last_login, last_name, logentry, password, token, user_permissions
    
    
    except Exception as e:
        print(e)

    return render(request , 'forget-password.html')



from django.shortcuts import render
from .models import User

from chats.models import ChatModel
# Create your views here.





def index(request):
    users = User.objects.exclude(id=request.user.id)
    return render(request, 'index.html', context={'users': users})

""" 
def chatPage(request, username):
    user_obj = User.objects.get(username=username)
    users = User.objects.exclude(username=request.user.username)"""


def chatPage(request, id):
    user_obj = User.objects.get(id=id)
    users = User.objects.exclude(id=request.user.id)

    if request.user.id > user_obj.id:
       thread_name = f'chat_{request.user.id}-{user_obj.id}'
    else:
        thread_name = f'chat_{user_obj.id}-{request.user.id}'
    message_objs = ChatModel.objects.filter(thread_name=thread_name) 
    return render(request, 'main_chat.html', context={'user': user_obj, 'users': users, 'messages':message_objs }) 
