from django.shortcuts import render
from rest_framework import status 

from rest_framework.decorators import api_view 
from rest_framework.response import Response 
from rest_framework.parsers import JSONParser 
from django.views.decorators.csrf import csrf_exempt 

from django.contrib.auth.models import User 
from django.contrib.auth.hashers import check_password 
from rest_framework.authtoken.models import Token  
from django.core.exceptions import ValidationError
from rest_framework.permissions import IsAdminUser
from rest_framework.decorators import api_view, permission_classes




@api_view(['POST', 'GET' ])
def login(request):
    data = JSONParser().parse(request)

    username = data['username'] 
    password = data['password']

    try : 
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return Response({'error': 'Usuario Inválido'}, status=status.HTTP_404_NOT_FOUND)
   
    
    pass_valido = check_password(password, user.password)

    if not pass_valido:
        return Response({'error': 'Password Incorrecto'}, status=status.HTTP_400_BAD_REQUEST)

    
    token, created = Token.objects.get_or_create(user=user) 
    return Response(token.key)  