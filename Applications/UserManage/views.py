import json

from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.generics import (
    ListAPIView, CreateAPIView, DestroyAPIView, RetrieveAPIView
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

class UserAllView(ListAPIView):
    permission_classes = (permissions.IsAuthenticated, )
    authentication_classes = (JWTAuthentication, )
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        try:
            data = self.get_queryset()
            serializer = self.get_serializer(data, many=True)
            print(self.get_authenticate_header(request))
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error':str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UserDetailView(RetrieveAPIView):
    from django.forms import model_to_dict
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (JWTAuthentication, )
    lookup_url_kwarg = 'pk'
    lookup_field = 'pk'
    serializer_class = UserSerializer
    queryset = CustomUser.objects.get(pk=1)

    # def get_queryset(self):
    #     lookup_value = self.kwargs.get(self.lookup_url_kwarg)
    #     return CustomUser.objects.filter(pk=lookup_value)

    def get_object(self):
        try:
            serializer = self.get_serializer(data=self.get_queryset(), many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error':str(e)}, status=status.HTTP_404_NOT_FOUND)

class RegisterUserView(CreateAPIView):
    permission_classes = (permissions.AllowAny, )
    serializer_class = UserRegisterSerializer

    def get_authenticators(self):
        authenticators = super().get_authenticators()

    def post(self, request, *args, **kwargs):
        try:
            sended_data = request.data
            serializer = self.get_serializer(data=sended_data)
            if serializer.is_valid():
                serializer.check_data(sended_data)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error':str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get_serializer_class(self):
        ser_class = super().get_serializer_class()
        return ser_class

    # def get_queryset() - return queryset in our method
    # def get_object() - use field lookup_field to generate single instance
    # lookup_field - like pk to get single instance with our pk
    # lookup_url_kwarg - like pk to get single instance with our pk
    # pagination_class
    # get_serializer_class() - return serializer or we can custom this to add varius serializer
    # get_serializer(self, instance=None, data=None, many=False, partial=False) - zwraca instance serializer

    # def default_response_headers(self):
    #     context = super(RegisterUserView, self).default_response_headers()
    #     print("this is default response header")
    #     print(context)
