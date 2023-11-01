import json
from django.shortcuts import render
from rest_framework.views import APIView

from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    DestroyAPIView,
    RetrieveAPIView,
    RetrieveUpdateDestroyAPIView,
    RetrieveUpdateAPIView
)

from rest_framework import (
    permissions,
    status,
    authentication
)

from .serializers import (
    UserRegisterSerializer,
    UserLoginSerializer,
    UserSerializer,
    UserDetailSerializer,
    UserPermissionSerializer
)
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from django.contrib.auth import logout, authenticate, login
from .models import CustomUser
from django.http import JsonResponse
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.models import Group, Permission
from .auth.login_token_serializer import CustomTokenObtainSerializer
class LoginTokenView(TokenObtainPairView):
    permission_classes = (permissions.AllowAny, )
    serializer_class = CustomTokenObtainSerializer

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


class SingleUserDetail(RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticated, )
    authentication_classes = (JWTAuthentication,)
    serializer_class = UserDetailSerializer

    def retrieve(self, request, *args, **kwargs):
        try:
            user = self.request.user
            group_permission = user.groups.all()
            user_group = Group.objects.get(name='Driver')
            user_group_permission = CustomUser.objects.select_related(
            )
            all_assigned_groups = request.user.groups.all()
            all_permissions = all_assigned_groups[0].permissions.values_list('codename', flat=True)
            serializer = self.get_serializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data={'error': str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, *args, **kwargs):
        try:
            user = self.request.user
            data = self.request.data

            serializer = self.get_serializer(
                instance=user,
                data=data,
                partial=True
            )

            if serializer.is_valid():
                serializer.update(user, data)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_409_CONFLICT)
        except Exception as e:
            return Response(data={'error': str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UserAllView(ListAPIView):
    permission_classes = (permissions.IsAuthenticated, )
    authentication_classes = (JWTAuthentication, )
    serializer_class = UserSerializer

    def get_queryset(self):
        return CustomUser.objects.all()

    def list(self, request, *args, **kwargs):
        try:
            data = self.get_queryset()
            serializer = self.get_serializer(data, many=True)
            print(self.get_authenticate_header(request))
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PkUserDetailView(RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (JWTAuthentication, )
    lookup_url_kwarg = 'pk'
    lookup_field = 'pk'
    serializer_class = UserSerializer

    def get_queryset(self):
        user_pk = self.kwargs.get(self.lookup_url_kwarg)
        return CustomUser.objects.get(id=user_pk)

    def retrieve(self, request, *args, **kwargs):
        try:
            print('Esa testowanie wyswietlania')
            user_instance = request.user
            print(user_instance.show_permissions())
            print(user_instance.has_perm('is_active'))
            user = self.get_object()
            user_serializer = self.get_serializer(user)
            return Response(user_serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data={'error': str(e)},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, *args, **kwargs):
        try:
            data = request.data
            current_user = request.user
            modified_user = self.get_queryset()
            serializer = self.get_serializer(instance=modified_user,
                                             data=data,
                                             partial=True)
            if serializer.is_valid():
                mod_user = serializer.update(modified_user, data)
                mod_user.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_409_CONFLICT)
        except Exception as e:
            return Response(data={'error': str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UserPermissionView(APIView):
    permission_classes = (permissions.IsAuthenticated, )
    authentication_classes = (JWTAuthentication, )


    def get(self, request):
        try:
            print('esa')
            user = request.user
            serializer = UserPermissionSerializer(instance=user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data={'error': str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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
                user = serializer.check_data(sended_data)
                user_group = Group.objects.get(name='Driver')
                user.groups.add(user_group)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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

