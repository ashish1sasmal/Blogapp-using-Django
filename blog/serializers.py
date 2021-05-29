from rest_framework import serializers
from .models import Comment,Blog
from rest_framework.response import Response
from rest_framework import status
import json
from django.contrib.auth import get_user_model
User = get_user_model()


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(many=False, write_only=True,queryset=User.objects.all())
    username = serializers.SerializerMethodField()
    class Meta:
        model = Comment
        fields = '__all__'

    def get_username(self,obj):
        return obj.user.username
