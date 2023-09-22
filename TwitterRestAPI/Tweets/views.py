from datetime import datetime
from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.paginator import Paginator
import json
import logging
from Users.models import Users
from Users.views import Auth
from Tweets.models import Tweets
from Tweets.serializer import TweetsSerializer
from Users.serializer import UserSerializer
from django.db.models import Q

from rest_framework.views import APIView
from django.shortcuts import render

logger = logging.getLogger(__name__)
logging.basicConfig(filename="debug.log", level=logging.DEBUG)


class CreateTweetView(APIView):
    def post(self, request):
        try:
            username = Auth(request=request)["username"]
            user = Users.objects.get(username=username)
            tweet = request.data["tweet"]
            new_tweet = Tweets(username=user, tweet=tweet)
            new_tweet.save()
            serializer = TweetsSerializer(new_tweet)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(e, status=status.HTTP_400_BAD_REQUEST)


class ProfileTimelineView(APIView):
    def get(self, request):
        try:
            userid = Auth(request=request)["id"]
            # tweets = Tweets.objects.filter(username=userid)

            # last_tweets = Tweets.objects.filter(x for x in retweets if x == userid)
            retweets = Tweets.objects.filter(retweets__id=userid) | Tweets.objects.filter(
                username=userid
            )
            serializer = TweetsSerializer(retweets, many=True)
            print(retweets)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(e, status=status.HTTP_400_BAD_REQUEST)

class TimelineView(APIView):
    def get(self, request):
        try:
            userid = Auth(request=request)["id"]
            username = Auth(request=request)["username"]
            # tweets = Tweets.objects.filter(username=userid)

            # last_tweets = Tweets.objects.filter(x for x in retweets if x == userid)
            following_users = Users.objects.get(username=username).following
            user_serializer = UserSerializer(following_users, many=True)
            print(user_serializer)
            retweets = Tweets.objects.filter(retweets__id=userid) | Tweets.objects.filter(
                username=userid
            )
            serializer = TweetsSerializer(retweets, many=True)
            print(retweets)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(e, status=status.HTTP_400_BAD_REQUEST)


class RetweetView(APIView):
    def post(self,request):
        # try:
        username = Auth(request=request)["username"]
        user = Users.objects.get(username=username)
        tweet_username = request.data["tweet_user"]
        tweet_text = request.data["tweet_text"]
        tweet_user = Users.objects.get(username=tweet_username)
        retweeted = Tweets(username=tweet_user, tweet=tweet_text)
        retweeted.save()

        retweeted.retweets.add(user)
        retweeted.save()
        serializer = TweetsSerializer(retweeted)
        return Response(serializer.data, status=status.HTTP_200_OK)


# except Exception as e:
#     return Response(e, status=status.HTTP_400_BAD_REQUEST)


class ReplyView(APIView):
    def post(self,request):
        try:
            username = Auth(request=request)["username"]
            user = Users.objects.get(username=username)

            tweet_username = request.data["tweet_username"]
            tweet_user = Users.objects.get(username=tweet_username)
            tweet_text = request.data["tweet_text"]
            replied_tweet = Tweets.objects.get(username=tweet_user, tweet=tweet_text)

            reply_text = request.data["reply_text"]
            reply_tweet = Tweets(username=user, tweet=reply_text)

            replied_tweet.replies.add(reply_tweet)
            replied_tweet.save()

            serializer = TweetsSerializer(replied_tweet)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(e, status=status.HTTP_400_BAD_REQUEST)


