
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm,UserForm,UserUpdateForm,ProfileUpdateForm
import requests
from django.conf import settings
import json
import urllib
from .models import Profile
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes, force_text
from .tokens import account_activation_token

from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import login,logout


def activate(request, uidb64, token, backend='django.contrib.auth.backends.ModelBackend'):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        return redirect('blog-home')
    else:
        return render(request, 'account_activation_invalid.html')


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
                user.is_active=False
                user.save()
                profile=profile_form.save(commit=False)
                profile.user=user
                if 'image' in request.FILES:
                    profile.image=request.FILES['image']
                profile.save()
                current_site = get_current_site(request)
                mail_subject = 'Activate your blog account.'
                message = render_to_string('users/acc_active_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                    'token':account_activation_token.make_token(user),
                })
                to_email = form.cleaned_data.get('email')
                email = EmailMessage(
                            mail_subject, message, to=[to_email]
                )
                email.send()
                # username = form.cleaned_data.get('username')
                return HttpResponse('Please confirm your email address to complete the registration')
    else:
        form = UserForm()
        profile_form=UserRegisterForm()
    return render(request, 'users/register.html', {'form': form,'profile_form':profile_form})


@login_required
def profile(request):
    current_site = get_current_site(request)
    print(current_site)
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
