from django.db import models

# Create your models here.
from django.contrib.auth import get_user_model
User = get_user_model()
import uuid
from .s3 import s3_service
from django.db.models.signals import post_delete
from django.dispatch import receiver

class Blog(models.Model):
    content = models.TextField()
    image = models.CharField(max_length=100,blank=True, null=True)
    user = models.ForeignKey(User,related_name="blog_user",on_delete=models.CASCADE)
    likes = models.ManyToManyField(User,related_name="liked_users")
    created_on = models.DateTimeField(auto_now=True)

    def save(self,file=None ,**kwargs):
        if file:
            self.image = f"{uuid.uuid1()}.{file.name.split('.')[-1]}"
            s3_service.upload_file_obj(file,self.image)
        super(Blog, self).save(**kwargs)

    def download_temp_url(self):
        return s3_service.create_temp_url(self.image)

    def image_url(self):
        return f"https://secretblogs.s3.ap-south-1.amazonaws.com/{self.image}"

class Comment(models.Model):
    blog = models.ForeignKey(Blog, related_name="blog_comment", on_delete=models.CASCADE)
    user = models.ForeignKey(User,related_name="comment_user",on_delete=models.CASCADE)
    text = models.TextField()
    created_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.blog}_{self.user}_{self.id}"
    

@receiver(post_delete, sender=Blog)
def delete_file_s3(sender, instance, **kwargs):
    if instance.image:
        s3_service.delete_file(instance.image)
        print("Doc deleted @")
