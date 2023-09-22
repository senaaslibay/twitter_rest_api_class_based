from django.db import models

class HashTags(models.Model):
    name= models.CharField(max_length=280)
    