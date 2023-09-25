from django.urls import path
from rest_framework import routers
# from api import views
from .views import *
# from .views import CreateTweetView, ProfileTimelineView, RetweetView, ReplyView,TimelineView
app_name = 'api'

router = routers.DefaultRouter()
router.register(r'tweet', TweetView, basename="create")  # NOQA
# router.register(r'get_queryset', TweetView, basename="get_queryset")  # NOQA

urlpatterns = router.urls


# urlpatterns = [
#     path('create/', CreateTweetView.as_view()),
    # path('profile_timeline', ProfileTimelineView.as_view()),
#     path('timeline', TimelineView.as_view()),
#     path('retweet/', RetweetView.as_view()),
#     path('reply/', ReplyView.as_view()),

# ]

