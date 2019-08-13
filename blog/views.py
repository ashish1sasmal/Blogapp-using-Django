from django.shortcuts import render

# Create your views here.

from django.views.generic import TemplateView

class HomeView(TemplateView):
	template_name='blog/home.html'
	posts = [
    {
        'author': 'CoreyMS',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'August 27, 2018'
    },
    {
        'author': 'Jane Doe',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'August 28, 2018'
    }
]

	def get_context_data(self, **kwargs):
		d = {'posts':self.posts}
		return d

class AboutView(TemplateView):
	template_name='blog/about.html'
