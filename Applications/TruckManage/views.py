from rest_framework.generics import (
    CreateAPIView,
    RetrieveUpdateDestroyAPIView
)
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializers import (
    TruckSerializer,
    TruckEquipmentSerializer
)
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.parsers import MultiPartParser
from rest_framework.decorators import action
from .models import Truck, TruckEquipment
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework.pagination import PageNumberPagination

# find . -path "*/__pycache__" -type d -exec rm -r {} ';'

class PaginationClass(PageNumberPagination):
    page_size = 4

class TruckViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated, )
    authentication_classes = (JWTAuthentication, )
    parser_classes = (MultiPartParser, )
    serializer_class = TruckSerializer
    queryset = Truck.objects.all()
    pagination_class = PaginationClass
    lookup_url_kwarg = 'pk'

    def get_object(self):
        try:
            pk = self.kwargs.get(self.lookup_url_kwarg)
            truck = Truck.objects.get(pk=pk)
            return truck
        except Truck.DoesNotExist:
            raise Http404("Object not found")

    def list(self, request, *args, **kwargs):
        try:
            trucks = self.filter_queryset(self.get_queryset())
            page = self.paginate_queryset(trucks)
            if page is not None:
                trucks_serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(trucks_serializer.data)
            serializer = self.get_serializer(instance=trucks, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data={'error': str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data={'error': str(e)},
                            status=status.HTTP_404_NOT_FOUND)

    def update(self, request, *args, **kwargs):
        try:
            data = request.data
            truck = self.get_object()
            serializer = TruckSerializer(
                data=data,
                instance=truck,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.update(truck, data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data={'error': str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def create(self, request, *args, **kwargs):
        try:
            # parse and change format of our data
            data = request.data
            data['power'] = int(data.get('power'))
            data['driven_length'] = int(data.get('driven_length'))
            serializer = TruckSerializer(data=data)

            # part of validation and create truck
            serializer.is_valid(raise_exception=True)
            truck = serializer.create(data)
            truck.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)},
                            status=status.HTTP_400_BAD_REQUEST)

class TruckEquipmentCreateView(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTAuthentication,)
    serializer_class = TruckEquipmentSerializer

    def create(self, request, *args, **kwargs):
        try:
            print(request.data)
            truck = get_object_or_404(Truck, pk=request.data['truck'])
            request.data['truck'] = truck.pk
            print(request.data)
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            request.data['truck'] = truck
            serializer.create(request.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)},
                            status=status.HTTP_400_BAD_REQUEST)

class TruckEquipmentDetailView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTAuthentication,)
    serializer_class = TruckEquipmentSerializer
    lookup_url_kwarg = 'pk'

    def get_object(self):
        truck_id = self.kwargs.get(self.lookup_url_kwarg)
        print(truck_id)
        return TruckEquipment.objects.get(truck_id=truck_id)

    def retrieve(self, request, *args, **kwargs):
        try:
            truck_equipment = self.get_object()
            serializer = self.get_serializer(truck_equipment)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data={'error': str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, *args, **kwargs):
        try:
            data = self.request.data
            print(data)
            semi_equipment = self.get_object()
            serializer = self.get_serializer(data=data,
                                             instance=semi_equipment,
                                             partial=True)
            serializer.is_valid(raise_exception=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data={'error': str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)