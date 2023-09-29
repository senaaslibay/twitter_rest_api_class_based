from rest_framework import status
from rest_framework.decorators import  action
from rest_framework.response import Response
import logging
from Users.models import Users
from Users.views import Auth
from Tweets.models import Tweets
from Tweets.serializer import TweetsSerializer, CreateTweetsSerializer

from rest_framework import viewsets, permissions


logger = logging.getLogger(__name__)
logging.basicConfig(filename="debug.log", level=logging.DEBUG)


class TweetView(viewsets.ModelViewSet):
    queryset = Tweets.objects.all()
    serializer_class = TweetsSerializer
    permission_classes = [permissions.AllowAny]

    def get_serializer_class(self):
        if self.action == "create":
            return CreateTweetsSerializer
        else:
            return self.serializer_class

    def create(self, request, *args, **kwargs):
        userid = Auth(request=request)["id"]
        request.data["username"] = userid
        serializer = self.get_serializer_class()(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
    def list(self, request):
        try:
            userdata = Auth(request=request)
            userid = userdata["id"]
            username = userdata["username"]

            user_id_list = Users.objects.get(username=username).following.values_list("id", flat=True)
            query_set = Tweets.objects.filter(username__id__in=user_id_list) | Tweets.objects.filter(username=userid) | Tweets.objects.filter(retweets__id=userid)
            return Response(self.get_serializer_class()(query_set, many=True).data,status=status.HTTP_200_OK)  
        except Exception as e:
            return Response(e, status=status.HTTP_400_BAD_REQUEST)


    @action(detail=False, methods=["get"],url_path="my_profile_timeline_list",)
    def my_profile_timeline_list(self,request):
        try:
            userid = Auth(request=request)["id"]
            query_set = Tweets.objects.filter(retweets__id=userid) | Tweets.objects.filter(username=userid)
            return Response(self.get_serializer_class()(query_set, many=True).data,status=status.HTTP_200_OK)  

        except Exception as e:
            return Response(e, status=status.HTTP_400_BAD_REQUEST)


    @action(detail=True, methods=["get"],url_path=f"user_profile_timeline_list",)
    def user_profile_timeline_list(self,request,pk=None):
        try:
            userid = Auth(request=request)["id"]
            if (checkUserAllowness(pk,userid)["allowness"]):
                query_set = Tweets.objects.filter(retweets__id=pk) | Tweets.objects.filter(username=pk)
                return Response(self.get_serializer_class()(query_set, many=True).data,status=status.HTTP_200_OK) 
            return Response("You dont have permission to see this.",status=status.HTTP_423_LOCKED) 
            
        except Exception as e:
            return Response(e, status=status.HTTP_400_BAD_REQUEST)

    
    
    @action(detail=False, methods=["post"],url_path=f"retweet",)
    def retweet(self, request):
        try:
            username = Auth(request=request)["username"]
            user = Users.objects.get(username=username)

            tweet_username = request.data["tweet_user"]
            tweet_text = request.data["tweet_text"]

            tweet_user = Users.objects.get(username=tweet_username)
            retweeted = Tweets.objects.get(username=tweet_user, tweet=tweet_text)

            if (checkUserAllowness(tweet_user.id,user.id)["allowness"]):
                # if user.id in retweeted.values_list("id", flat=True):
                #     return Response("You already retweeted this tweet.",status=status.HTTP_200_OK) buna gerek yok gibi çünkü set olarak saklıyo.
                retweeted.retweets.add(user)
                retweeted.save()
                return Response(self.get_serializer_class()(retweeted).data,status=status.HTTP_200_OK)
            return Response("You don't have permission to retweet this tweet.",status=status.HTTP_200_OK)

        except Exception as e:
            return Response(e, status=status.HTTP_400_BAD_REQUEST)
        


    @action(detail=False, methods=["post"],url_path=f"reply",)
    def reply(self, request):
        try:
            username = Auth(request=request)["username"]
            user = Users.objects.get(username=username)

            tweet_username = request.data["tweet_username"]
            tweet_user = Users.objects.get(username=tweet_username)
            tweet_text = request.data["tweet_text"]
            replied_tweet = Tweets.objects.get(username=tweet_user, tweet=tweet_text)

            reply_text = request.data["reply_text"]
            reply_tweet = Tweets(username=user, tweet=reply_text)

            if (checkUserAllowness(tweet_user.id,user.id)["allowness"]):
                replied_tweet.replies.add(reply_tweet)
                replied_tweet.save()
                return Response(self.get_serializer_class()(replied_tweet).data,status=status.HTTP_200_OK)
            return Response("You don't have permission to reply this tweet.",status=status.HTTP_200_OK)

        except Exception as e:
            return Response(e, status=status.HTTP_400_BAD_REQUEST)
        




def checkUserAllowness(targetuserid,userid):
    locked= Users.objects.get(id=targetuserid).locked
    if locked:
        userid_list = Users.objects.get(id=targetuserid).following.values_list("id", flat=True)
        if userid in userid_list:
            return {"locked":True, "allowness":True}
        return {"locked":True, "allowness":False}
    return {"locked":False, "allowness":True}     