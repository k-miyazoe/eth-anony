from dataclasses import field
from rest_framework import serializers
from .models import User,Question,Answer

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__' 
        #idを更新不可にできる
        read_only_fields = ('id',)
        extra_kwargs = {'password': {'required': False}}

    def create(self,validated_data):
        #パスワードをハッシュ化する
        user = User.objects.create_user(**validated_data)
        return user
    
class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'
        read_only_fields = ('id',)

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = '__all__'
        read_only_fields = ('id',)

