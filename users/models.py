from django.db import models

# Create your models here.
from django.contrib.auth import get_user_model
User = get_user_model()
from blog.s3 import s3_service
from django.db.models.signals import post_delete
from django.dispatch import receiver

class UserProfile(models.Model):
    user = models.OneToOneField(User,related_name="user_profile",on_delete=models.CASCADE)
    bio = models.TextField()
    birthday = models.DateField(blank=True,null=True)
    country = models.CharField(max_length=100,blank=True,null=True)
    mobile = models.CharField(max_length=20,blank=True,null=True)
    website = models.URLField(blank=True,null=True)
    twitter = models.URLField(blank=True,null=True)
    facebook= models.URLField(blank=True,null=True)
    google= models.URLField(blank=True,null=True)
    linkedin= models.URLField(blank=True,null=True)
    instagram = models.URLField(blank=True,null=True)

    emailconfirm = models.BooleanField(default=False)
    picdata = models.TextField()
    follow = models.ManyToManyField(User,related_name="follow_user",blank=True,null=True)

    def __str__(self):
        return self.user.username

# @receiver(post_delete, sender=UserProfile)
# def delete_file_s3(sender, instance, **kwargs):
#     if instance.s3pic:
#         s3_service.delete_file(instance.s3pic)
#         print("Doc deleted @")
