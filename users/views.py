from django.shortcuts import render,redirect
from django.contrib import messages
from .forms import RegisterationForm
from django.contrib.auth.decorators import login_required

# Create your views here.

def Register(request):
	
	if request.method=='POST':
		form=RegisterationForm(request.POST)
		if form.is_valid():
			form.save()
			username=form.cleaned_data.get('username')
			messages.success(request,f'Account Created for {username}!')
			return redirect('login')
	else:
		form=RegisterationForm()

	return render(request,'users/register.html',{'form':form})
@login_required
def profile(request):
	return render(request,'users/profile.html')