from rest_framework import serializers
from Tweets.models import Tweets
from django import forms

class TweetsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tweets
        fields = '__all__'

class CreateTweetsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tweets
        fields = ('username', 'tweet',)