from django.urls import path
from .views import BotUserApiView, FeedbackApiView

urlpatterns = [
    path('bot-users', BotUserApiView.as_view(), name='bot-users'),
    path('feedbacks', FeedbackApiView.as_view(), name='feedbacks'),
]
