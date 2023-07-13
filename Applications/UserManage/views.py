from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.generics import (
    ListAPIView, CreateAPIView, DestroyAPIView
)
from rest_framework.permissions import AllowAny, IsAuthenticated


class Login(APIView):
    permission_classes = [AllowAny, ]

    def get(self, request):
        pass

    def post(self, request):
        pass

class Register(APIView):
    pass


class UserDetail(APIView):
    permission_classes = [AllowAny, ]


class Logout(APIView):
    permission_classes = [IsAuthenticated, ]