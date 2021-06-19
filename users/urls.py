from django.urls import path, include
from . import views
app_name = "users"

urlpatterns = [
    path('profile/<str:username>/',views.profile,name="profile"),
    path('register/',views.register,name="register"),
    path('activate/<str:key>/',views.activate,name="activate"),
    path('logout/',views.user_logout,name='logout'),
    path('login/',views.Userlogin.as_view(),name='login'),
    path('follow/',views.follow,name='follow'),
    path('emailconfirm/',views.emailconfirmresend,name="emailconfirm"),
    path('forgotPassword/',views.forgotPassword, name="forgotPassword"),
    path('match/qs/<str:qs>/',views.match, name="forgotPasswordMatch")
]
