from django.db import models
from Users.models import Users
from HashTags.models import HashTags
from datetime import datetime


get_time = datetime.now().strftime('%m/%d/%Y %I:%M:%S %p')

class Tweets(models.Model):
    username = models.ForeignKey(Users, on_delete = models.CASCADE)
    tweet = models.CharField(max_length=280)
    time = models.CharField(max_length=50,default=get_time)
    retweets = models.ManyToManyField(Users,related_name="retweeted_users")
    likes = models.ManyToManyField(Users,related_name="liked_users")
    replies= models.ManyToManyField("self",related_name="reply_text",symmetrical=False)
    hashtags = models.ManyToManyField(HashTags, related_name="hahstag")

    def __str__(self):
        return f"{self.tweet}, {self.username}"
#hashtagclass 
