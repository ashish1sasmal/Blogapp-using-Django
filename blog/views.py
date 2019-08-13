from django.shortcuts import render
from .models import Post
# Create your views here.

from django.views.generic import TemplateView,ListView

class HomeView(ListView):
	template_name='blog/home.html'
	context_object_name='posts'
	model=Post
	# def get_context_data(self, **kwargs):
	# 	d = {'posts':self.posts}
	# 	return d

class AboutView(TemplateView):
	template_name='blog/about.html'
