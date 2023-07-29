from django.shortcuts import render
from rest_framework.generics import (
    CreateAPIView,
    RetrieveUpdateDestroyAPIView
)
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializers import SemiTrailerSerializer, SemiTrailerEquipmentSerializer

class SemiTruckCreate(CreateAPIView):
    permission_classes = (IsAuthenticated, )
    authentication_classes = (JWTAuthentication, )
    serializer_class = SemiTrailerSerializer

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.create(request.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(data={'error':str(e)},
                            status=status.HTTP_400_BAD_REQUEST)

class SemiTruckDetail(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTAuthentication,)
    serializer_class = SemiTrailerSerializer
    lookup_url_kwarg = 'pk'

    def get_queryset(self):
        pass

    def get_object(self):
        pass

    def retrieve(self, request, *args, **kwargs):
        pass

    def update(self, request, *args, **kwargs):
        pass

    def delete(self, request, *args, **kwargs):
        pass


class SemiTruckEquipmentCreate(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTAuthentication,)
    serializer_class = SemiTrailerEquipmentSerializer

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.create(request.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(data={'error':str(e)},
                            status=status.HTTP_400_BAD_REQUEST)

class SemiTruckEquipmentDetail(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTAuthentication,)
    serializer_class = SemiTrailerEquipmentSerializer

    def retrieve(self, request, *args, **kwargs):
        pass

    def update(self, request, *args, **kwargs):
        pass

    def delete(self, request, *args, **kwargs):
        pass

