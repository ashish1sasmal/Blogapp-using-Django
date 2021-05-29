from django.urls import path, include
from . import views
app_name = "blog"

urlpatterns = [
    path('',views.home,name="home"),
    path('liked/',views.like,name="like"),
    path('editpost/<int:id>/',views.editPost,name="editpost"),
    path('comment/<int:id>/',views.CommentCBV.as_view(),name="comment")
]
