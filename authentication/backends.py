from asyncio import exceptions
from asyncio.log import logger
from email import header
from sys import prefix
from tkinter.messagebox import NO
import jwt,logging
from rest_framework import authentication
from django.conf import settings
from django.contrib.auth.models import User

class JWTAuthentication(authentication.BaseAuthentication) :
    
    def authenticate(self, request):
        auth_data = authentication.get_authorization_header(request)
        # logging.info(auth_data)
        
        if not auth_data:
            return None
        
        token = auth_data.decode('utf-8')
        
        # splitting bearer from token
        if 'Bearer' in token :
            prefix,token = token.split(' ')
        
        try:
            payload = jwt.decode(token,settings.JWT_SECRET_KEY)
            
            user = User.objects.get(username=payload['username'])
            
            return (user,token)
            
        except jwt.DecodeError as e:
            raise exceptions.AuthenticationFailed('Token Invalid')
        except jwt.ExpiredSignatureError as e:
            raise exceptions.AuthenticationFailed('Token Expired')
        
        return super().authenticate(request)