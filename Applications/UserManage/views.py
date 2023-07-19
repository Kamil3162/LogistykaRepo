import json

from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.generics import (
    ListAPIView, CreateAPIView, DestroyAPIView
)
from rest_framework import permissions, status, authentication
from .serializers import (
    UserRegisterSerializer, UserLoginSerializer, UserSerializer)
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from django.contrib.auth import logout, authenticate, login
from .models import CustomUser
from django.http import JsonResponse
from rest_framework_simplejwt.authentication import JWTAuthentication
class Login(APIView):
    permission_classes = [permissions.AllowAny, ]
    authentication_classes = (authentication.SessionAuthentication, )

    def post(self, request):
        clean_data = request.data
        serializer = UserLoginSerializer(data=clean_data)
        if serializer.is_valid():
            user = serializer.check_user(clean_data)
            login(request, user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_404_NOT_FOUND)

class Register(APIView):
    permission_classes = [permissions.AllowAny, ]

    def post(self, request):
        print(request.data)
        clean_data = request.data
        serializer = UserRegisterSerializer(data=clean_data)
        if serializer.is_valid():
            try:
                user = serializer.check_data(clean_data)
                return Response(data=serializer.data, status=status.HTTP_201_CREATED)
            except ValidationError as e:
                return Response(data={'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(data={'error':str(serializer.errors)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class AllUsers(ListAPIView):
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny, )

    def get_queryset(self):
        return CustomUser.objects.all()

    def get_serializer_context(self):
        context = super(AllUsers, self).get_serializer_context()

class UserDetail(APIView):
    permission_classes = (permissions.IsAuthenticated, )
    authentication_classes = (authentication.SessionAuthentication, )

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

class Logout(APIView):
    def post(self, request):
        logout(request)
        return Response(status=status.HTTP_200_OK)

'''
    Part responsible for handle view using jwt token 
'''

from rest_framework_simplejwt.tokens import RefreshToken

class LoginTokenView(APIView):
    permission_classes = (permissions.AllowAny, )

    def post(self, request):
        data = request.data
        serializer = UserLoginSerializer(data=data)
        if serializer.is_valid():

            user = serializer.check_user(data)
            refresh = RefreshToken.for_user(user)

            return Response(data={
                'refresh': str(refresh),
                'access': str(refresh.access_token)
            })

class HomeTokenView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        return JsonResponse(data={
            'information': "properly log in"
        })

class LogoutTokenView(APIView):
    permission_classes = (permissions.IsAuthenticated, )
    authentication_classes = (JWTAuthentication, )

    def post(self, request):
        try:
            print(request)
            refresh_token = request.data['refresh_token']
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(data={'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ValidateToken(APIView):
    permission_classes = (permissions.IsAuthenticated, )
    authentication_classes = (JWTAuthentication,)

    def get(self, request):
        return Response(data={'valid': True}, status=status.HTTP_200_OK)

class UserDetailToken(APIView):
    permission_classes = (permissions.IsAuthenticated, )
    authentication_classes = (JWTAuthentication,)

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
