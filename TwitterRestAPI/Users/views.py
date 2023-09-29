from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.shortcuts import get_object_or_404

from rest_framework.authtoken.models import Token
from Users.models import Users
from Users.serializer import UserSerializer
import datetime
from django.conf import settings
import jwt
import json
from rest_framework import status
from rest_framework.views import APIView
from django.shortcuts import render




EXP_TIME = datetime.timedelta(hours=1)

class SignupView(APIView):
    def post(self,request):
        print(request.data)
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response( status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    #dönen veriler düzeltilecek
    def post(self,request):
        username = request.data["username"]
        password = request.data["password"]

        user = get_object_or_404(Users, username=username)

        if user.password != password:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        payload = {
            "id": user.id,
            "username": user.username,
            "exp": datetime.datetime.utcnow() + EXP_TIME,
        }
        token = {"token": jwt.encode(payload, settings.AUTH_TOKEN).decode("utf8")}
        user.token = token["token"]
        user.save()
        request.session["authtoken"] = token
        serializer = UserSerializer(instance=user)
        return Response( {"token":serializer.data["token"]})

class FollowUserView(APIView):
    def post(self,request, user):
        loggedin_username = Auth(request=request)["username"]

        cur_user = Users.objects.get(username=loggedin_username)
        fol_user = Users.objects.get(username=user)

        if (checkUserAllowness(targetuserid=fol_user.id,userid=cur_user.id)["locked"]):
            fol_user.follow_requests.add(cur_user)
            return Response("Your request has been sended.",status=status.HTTP_200_OK)
        
        follower_id_list = Users.objects.get(username=user).followers.values_list("id", flat=True)

        # if (cur_user.id in follower_id_list):
        #     return Response("You are already following this user.",status=status.HTTP_200_OK) buna gerek yok gibi zaten set tutuyo 
        cur_user.following.add(fol_user)
        cur_user.save()
        cur_serializer = UserSerializer(cur_user)

        fol_user.followers.add(cur_user)
        fol_user.save()
        fol_serializer = UserSerializer(fol_user)

        return Response(
            {"cur_following": cur_serializer.data["following"], "fol_followers": fol_serializer.data["followers"]},
            status=status.HTTP_204_NO_CONTENT,
        )


def Auth(request):
    try:
        token = request.session.get("authtoken").get("token")
        payload = jwt.decode(token, settings.AUTH_TOKEN)
        print(payload)
        username = payload.get("username")
        user = Users.objects.get(username= username)
        serializer = UserSerializer(user)
        return serializer.data
    except:
        return Response(status=status.HTTP_403_FORBIDDEN)
from Tweets.views import checkUserAllowness