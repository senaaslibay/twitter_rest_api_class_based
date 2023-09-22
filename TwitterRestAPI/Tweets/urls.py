from django.urls import path
from .views import CreateTweetView, ProfileTimelineView, RetweetView, ReplyView,TimelineView



urlpatterns = [
    path('create/', CreateTweetView.as_view()),
    path('profile_timeline', ProfileTimelineView.as_view()),
    path('timeline', TimelineView.as_view()),
    path('retweet/', RetweetView.as_view()),
    path('reply/', ReplyView.as_view()),

]

