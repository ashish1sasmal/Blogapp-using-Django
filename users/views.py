from django.shortcuts import render, redirect

# Create your views here.
from .models import UserProfile
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import get_user_model
User = get_user_model()

from django.template.loader import render_to_string
from django.contrib.auth import login,logout
from django.contrib.auth.decorators import login_required
from blog.s3 import s3_service

from django.contrib.auth import authenticate
from django.views.generic import View

from cryptography.fernet import Fernet
from djangoblogs.settings import FERNET_KEY
from .email import emailSend
from django.contrib.auth import login,logout
from django.http import HttpResponse
from django.contrib import messages
import os
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse

from django.core.cache import cache
import string
import random

def encode(id):
    FK = bytes(FERNET_KEY, 'utf-8')
    fernet = Fernet(FK)
    message = str(id)
    encMessage = fernet.encrypt(message.encode())
    encMessage = str(encMessage)
    return encMessage[2:len(encMessage)-1]

@login_required
def user_logout(request):
    logout(request)
    return redirect('blog:home')

from base64 import b64decode
import face_recognition as fr

def gen(n):

    var2 = ""
    for i in range(n):
        var2 += random.choice(string.ascii_letters)
    return var2

def genDigit(n):
    string = ""
    for i in range(n):
        string+=str(chr(random.randint(48,57)))
    return string

import face_recognition as fr
def compareFace(img1,img2):
    known_image = fr.load_image_file("media/"+img1)
    unknown_image = fr.load_image_file("media/"+img2)
    try:
        enc1  = fr.face_encodings(known_image)[0]
        enc2 = fr.face_encodings(unknown_image)[0]

        results = fr.compare_faces([enc1], enc2)
        if results[0]:
            return 200,True
        else:
            return 400,False
    except:
        return 500,False

class Userlogin(View):
    def post(self,request,*args,**kwargs):
        email = request.POST.get('email')
        password = request.POST.get('password')
        print(password)
        user=authenticate(email=email,password=password)
        if user:
            if request.POST.get("face_login")=="on":
                code1 = gen(6)+'.png'
                data1 = b64decode(user.user_profile.picdata)
                with open("media/"+code1, "wb") as f:
                    f.write(data1)
                f.close()

                logpic_data = request.POST.get("logpic")

                header, encoded = logpic_data.split(",", 1)
                data2 = b64decode(encoded)
                code2 = gen(6)+'.png'

                with open("media/"+code2, "wb") as a:
                    a.write(data2)

                status,res = compareFace(code1,code2)
                os.remove("media/"+code1)
                os.remove("media/"+code2)
            else:
                res = True
            if res:
                login(request,user)
                print("logged in")
                messages.success(request,"You have been logged in!")
                return redirect("blog:home")

            elif status == 400:
                messages.warning(request,"Face not matched, Please Try Again")
            else:
                messages.warning(request,"Face not clear, Please Try Again")

            # if os.path.exists("media/"+code2):
            #     os.remove("media/"+code2)
            # else:
            #     print("The file does not exist")

            return redirect("users:register")
        else:
            messages.warning(request,'Wrong input!')
        return redirect("users:register")


def profile(request,username):
    user = User.objects.get(username=username)
    profile = user.user_profile
    # if request.method == "POST":

    context = {}
    context["profile"] = profile
    return render(request,"users/profile.html",context)

def activate(request,key):
    print(key)
    key = bytes(key, 'utf-8')
    FK = bytes(FERNET_KEY, 'utf-8')
    fernet = Fernet(FK)
    id = fernet.decrypt(key).decode()
    try:
        user = User.objects.get(id=id)
    except User.DoesNotExist:
        user = None
    if user is not None:
        user.is_active = True
        up = user.user_profile
        up.emailconfirm = True
        user.save()
        up.save()
        login(request, user)
        messages.success(request,"Email confirmation done!")
        return redirect('blog:home')
    else:
        return HttpResponse("<h2>Invalid Request</h2>")


def forgotPassword(request):
    if request.method=="POST":
        email = request.POST.get("email")
        user = User.objects.filter(email=email)
        print(user)
        if user.exists():
            user = user.first()
            message =f'''
            Hey! Use this Link to set new password.
            Link : {os.environ.get("HOST")}/auth/match/qs/{encode(user.id)}
            This will expire in 5 minutes.

            Thank You
            '''
            emailSend("Password Recovery for Blog Account", message, [user.email])
            cache.set(user.username, user.username, 60*5)
            messages.success(request,"Password reset mail sent.")
            return redirect("blog:home")
        else:
            return JsonResponse({"status":404},status=404)

def match(request,qs):
    otp = qs
    key = bytes(otp, 'utf-8')
    FK = bytes(FERNET_KEY, 'utf-8')
    fernet = Fernet(FK)
    id = fernet.decrypt(key).decode()
    user = User.objects.filter(id=int(id))
    if user.exists():
        user = user.first()
        if cache.get(user.username, None):
            if request.method=="GET":
                print("Hererrr")
                return render(request, "users/forgot.html")
            else:
                if request.POST.get("inputPassword")==request.POST.get("inputPassword2"):
                    user.set_password(request.POST.get("inputPassword"))
                    user.save()
                    cache.delete(user.username)
                    messages.success(request,"Password changed successfully")
                    return redirect("blog:home")
                else:
                    messages.warning(request,"Passwords did not matched")
                    return redirect("users:forgotPasswordMatch")
        else:
            return HttpResponse("Link Expired")
    else:
        return HttpResponse("User doesn't exists.")






def emailconfirm(user):
    mail_subject = 'Activate your blog account.'
    message = f"{os.environ.get('HOST')}/auth/activate/"+encode(user.id)
    email = emailSend(
                mail_subject, message, [user.email]
    )
    print("after email")

def emailconfirmresend(request):
    emailconfirm(request.user)
    return JsonResponse({"status":200})

def register(request):
    if request.user.is_authenticated:
        return redirect("blog:home")
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get("email")
        user_count = User.objects.filter(email=email).count()
        if user_count==0:
            password = request.POST.get("password")
            username = email.split("@")[0]+"_"+gen(6)
            user = User(first_name=first_name,last_name=last_name,username=username,email=email)
            user.set_password(password)
            user.save()
            up = UserProfile(user=user)
            if request.POST.get("regpic"):
                regpic_data = request.POST.get("regpic")
                header, encoded = regpic_data.split(",", 1)
                print(type(encoded))
                up.picdata = encoded
            up.save()
            emailconfirm(user, email)
            # email.send()
            login(request,user)
            messages.success(request,"Email confirmation has been sent. Please check it.")
            return redirect("blog:home")
        else:
            messages.warning(request, "User already exist with this email id.")
            return redirect("users:register")
    else:
        return render(request,"users/register.html")


def follow(request):
    if request.method=="GET":
        try:
            flw_id = request.GET.get("flw_id")
            flw_user = User.objects.get(id=flw_id)
            profile = request.user.user_profile
            if flw_user in profile.follow.all():
                profile.follow.remove(flw_user)
                msg = f"You have un-followed {flw_user}"
            else:
                profile.follow.add(flw_user)
                msg = f"You are following {flw_user}"
            return JsonResponse({"msg":msg,"status":200},status=200)
        except Exception as e:
            return JsonResponse({"msg":"Some error occured","status":400})
