from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Event
from django.utils.timezone import now

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username', 'password', 'email']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username', 'email']



class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'
        read_only_fields = ['owner']

    def validate_start_date(self, value):
        if value <= now():
            raise serializers.ValidationError("Start time must be in the future.")
        return value

    def validate(self, data):
        if data['duration'] <= 0:
            raise serializers.ValidationError("Duration must be greater than zero.")
        return data

    