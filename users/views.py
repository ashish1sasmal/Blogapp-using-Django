
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm,UserForm,UserUpdateForm,ProfileUpdateForm
import requests
from django.conf import settings
import json
import urllib
from .models import Profile

def register(request):
    if request.method == 'POST':
        form = UserForm(data=request.POST)
        profile_form=UserRegisterForm(data=request.POST)

        if form.is_valid() and profile_form.is_valid():
            recaptcha_response = request.POST.get('g-recaptcha-response')
            data = {
                'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
                'response': recaptcha_response
            }
            r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
            result = r.json()
            print(result['success'])
            if result['success']:
                user=form.save()
                user.save()
                profile=profile_form.save(commit=False)
                profile.user=user
                if 'image' in request.FILES:
                    profile.image=request.FILES['image']
                profile.save()
                username = form.cleaned_data.get('username')
                messages.success(request, f'Your account has been created! You are now able to log in')
                return redirect('login')
    else:
        form = UserForm()
        profile_form=UserRegisterForm()
    return render(request, 'users/register.html', {'form': form,'profile_form':profile_form})


@login_required
def profile(request):
    if request.method=='POST':
        u_form=UserUpdateForm(request.POST,instance=request.user)
        p_form=ProfileUpdateForm(request.POST,request.FILES,instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()

            messages.success(request, f'Your account has been updated!')
            return redirect('profile')
    else:
        profile=Profile.objects.get_or_create(user=request.user)

        u_form=UserUpdateForm(instance=request.user)
        p_form=ProfileUpdateForm(instance=request.user.profile)

    return render(request, 'users/profile.html',{'u_form':u_form,'p_form':p_form})
