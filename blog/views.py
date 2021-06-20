from django.shortcuts import render,redirect

# Create your views here.
from .models import Blog,Comment
import uuid
from .s3 import s3_service
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth import get_user_model
User = get_user_model()
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator

@login_required
def autocomplete(request):
    if request.is_ajax():
        query = request.GET.get("term", "")
        results = []
        users = User.objects.filter(Q(username__icontains=query)|Q(first_name__icontains=query)|Q(last_name__icontains=query))
        for user in users:
            results.append({"label":f"{user.first_name} {user.last_name} {user.username}",
                            "value":user.username
                            })
        if results==[]:
            results.append({"label":"No Match Found","value":""})
        return JsonResponse(results,safe=False)
    elif request.method == "GET":
        username = request.GET.get("mysearch")
        return redirect('users:profile',username=username)

def blogPagination(page=1):
    blgs = Blog.objects.all().order_by('-created_on')
    paginator = Paginator(blgs, 5) # Show 10 blogs per page.
    page_obj = paginator.get_page(page)
    return page_obj

def home(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            content = request.POST.get("content")
            blogpic = request.FILES.get("blogpic",None)
            blg = Blog(content=content,user=request.user)
            blg.save(file=blogpic)
            messages.success(request,"Post uploaded successfully")
            return redirect("blog:home")
        else:
            page = request.GET.get("page",1)
            allblogs = blogPagination(page)
            content =  {}
            content["blgdetails"] = {
                "has_prev" : allblogs.has_previous(),
                "has_next" : allblogs.has_next()
            }

            content["blogs"] = allblogs
            return render(request,"blog/home2.html",content)
    else:
        return render(request,"blog/landing_page.html")

@login_required
def like(request):
    if request.method == "POST":
        try:
            id = request.POST.get("id")
            print(id)
            blg = Blog.objects.get(id=id)
            if request.user in blg.likes.all():
                print(request.user,"removed")
                blg.likes.remove(request.user)
            else:
                print(request.user,"added")
                blg.likes.add(request.user)
            return JsonResponse({"status":200},status=200)
        except Exception as e:
            print(e)
            return JsonResponse({"status":500},status=500)

from rest_framework import mixins
from rest_framework import generics
from .serializers import CommentSerializer

class CommentCBV(mixins.ListModelMixin,
                    mixins.CreateModelMixin,
                    generics.GenericAPIView,LoginRequiredMixin):

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    def get(self,request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self,request, *args, **kwargs):
        print(request.data,"Hi")
        return self.create(request, *args, **kwargs)

@login_required
def editPost(request,id):
    blg = Blog.objects.get(id = id)
    blg.content = request.POST.get("editcontent")
    blg.save()
    messages.success(request,"Post edited successfully.")
    return redirect("blog:home")

@login_required
def deletePost(request):
    blgid = request.GET.get("id")
    try:
        Blog.objects.get(id=int(blgid)).delete()
        return JsonResponse({"status":200})
    except Exception as e:
        print(e)
        return JsonResponse({"status":500})
