from datetime import datetime
from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from django.core.paginator import Paginator
import json
import logging
from Users.models import Users
from Users.views import Auth
from Tweets.models import Tweets
from Tweets.serializer import TweetsSerializer, CreateTweetsSerializer
from Users.serializer import UserSerializer
from django.db.models import Q

from rest_framework.views import APIView
from django.shortcuts import render

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

    

# class RetweetView(APIView):
#     def post(self, request):
#         # try:
#         username = Auth(request=request)["username"]
#         user = Users.objects.get(username=username)
#         tweet_username = request.data["tweet_user"]
#         tweet_text = request.data["tweet_text"]
#         tweet_user = Users.objects.get(username=tweet_username)
#         retweeted = Tweets(username=tweet_user, tweet=tweet_text)
#         retweeted.save()

#         retweeted.retweets.add(user)
#         retweeted.save()
#         serializer = TweetsSerializer(retweeted)
#         return Response(serializer.data, status=status.HTTP_200_OK)


# # except Exception as e:
# #     return Response(e, status=status.HTTP_400_BAD_REQUEST)


# class ReplyView(APIView):
#     def post(self, request):
#         try:
#             username = Auth(request=request)["username"]
#             user = Users.objects.get(username=username)

#             tweet_username = request.data["tweet_username"]
#             tweet_user = Users.objects.get(username=tweet_username)
#             tweet_text = request.data["tweet_text"]
#             replied_tweet = Tweets.objects.get(username=tweet_user, tweet=tweet_text)

#             reply_text = request.data["reply_text"]
#             reply_tweet = Tweets(username=user, tweet=reply_text)

#             replied_tweet.replies.add(reply_tweet)
#             replied_tweet.save()

#             serializer = TweetsSerializer(replied_tweet)
#             return Response(serializer.data, status=status.HTTP_200_OK)

#         except Exception as e:
#             return Response(e, status=status.HTTP_400_BAD_REQUEST)
