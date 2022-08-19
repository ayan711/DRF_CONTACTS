
from rest_framework import serializers
from django.contrib.auth.models import User
import logging

logging.basicConfig(level=logging.info) # Here
# logging.debug("Log message goes here.")
# logging.info("Log message goes here.")
# logging.warning("Log message goes here.")
# logging.error("Log message goes here.")
# logging.critical("Log message goes here.")


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=65, min_length=8, write_only=True)
    email = serializers.EmailField(max_length=255, min_length=4),
    first_name = serializers.CharField(max_length=255, min_length=2)
    last_name = serializers.CharField(max_length=255, min_length=2)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']

    def validate(self, attrs):
        
        # validate method gets called bf instance gets created
        # we can add custom checks here
        
        email = attrs.get('email', '')
        logging.info(email)
        
        if len(email) != 0:
        
            if User.objects.filter(email=email).exists():
                raise serializers.ValidationError(
                    {'email': ('Email is already in use')})
            
        return super().validate(attrs)

    def create(self, validated_data):

        logging.info(validated_data)
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=65, min_length=8, write_only=True)
    username = serializers.CharField(max_length=255, min_length=2)

    class Meta:
        model = User
        fields = ['username', 'password']

