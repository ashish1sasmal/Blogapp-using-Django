from django.shortcuts import render
from .models import Post
# Create your views here.

from django.views.generic import TemplateView,ListView,UpdateView,DetailView,CreateView,DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
class HomeView(ListView):
	template_name='blog/home.html'
	context_object_name='posts'
	model=Post
	ordering=['-date_posted']
	# def get_context_data(self, **kwargs):
	# 	d = {'posts':self.posts}
	# 	return d

class PostDetailView(DetailView):
	model = Post

class PostCreateView(LoginRequiredMixin,CreateView):
	model=Post
	fields=['title','content']

	def form_valid(self,form):  #NOT NULL constraint failed: blog_post.author_id
		form.instance.author=self.request.user    #saving user before creating post i.e., we are overriding it
		return super().form_valid(form)	

class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
	model=Post
	fields=['title','content']

	def form_valid(self,form):  #NOT NULL constraint failed: blog_post.author_id
		form.instance.author=self.request.user    #saving user before creating post i.e., we are overriding it
		return super().form_valid(form)	

	def test_func(self):
		post=self.get_object()
		if self.request.user==post.author:
			return True
		return False

class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
	model = Post

	def test_func(self):
		post=self.get_object()
		if self.request.user==post.author:
			return True
		return False

	success_url=reverse_lazy('blog-home')


class AboutView(TemplateView):
	template_name='blog/about.html'
