from django.shortcuts import render
from rest_framework import generics
from .models import User
from .serializers import UserSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication

# Create your views here.


class UserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
