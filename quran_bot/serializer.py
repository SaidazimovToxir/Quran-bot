from rest_framework.serializers import ModelSerializer
from .models import BotUser, Feedback

class BotUserSerializer(ModelSerializer):
    class Meta:
        model = BotUser
        fields = ('name', 'username', 'user_id', 'created_dt')
        
        
class BotFeedbackSerializer(ModelSerializer):
    class Meta:
        model = Feedback
        fields = ('name', 'user_id', 'created_dt', 'body')
        