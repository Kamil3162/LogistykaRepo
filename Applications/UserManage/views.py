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
from django.contrib.auth import logout, authenticate
from .models import CustomUser

class Login(APIView):
    permission_classes = [permissions.AllowAny, ]
    authentication_classes = (authentication.SessionAuthentication, )

    def post(self, request):
        clean_data = request.data
        serializer = UserLoginSerializer(data=clean_data)
        if serializer.is_valid():
            user = serializer.check_user(clean_data)
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