from django.db import models
# from rest_framework.authtoken.models import Token
# from django.contrib.auth.models import AbstractUser


class Users(models.Model):
    username= models.CharField(max_length=100, unique=True)
    password= models.CharField(max_length=100)
    following = models.ManyToManyField('self',related_name="following_users",symmetrical=False,blank=True)
    followers = models.ManyToManyField('self', related_name="followers_users",symmetrical=False,blank=True)
    token = models.CharField(max_length=10000, null=True)

        
