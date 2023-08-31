from rest_framework.generics import (
    CreateAPIView,
    RetrieveUpdateDestroyAPIView,
    ListAPIView
)
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializers import SemiTrailerSerializer, SemiTrailerEquipmentSerializer
from .models import SemiTrailer, SemiTrailerEquipment
from django.core.exceptions import ValidationError, ObjectDoesNotExist


class SemiTruckViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTAuthentication,)
    serializer_class = SemiTrailerSerializer
    lookup_url_kwarg = 'pk'
    queryset = SemiTrailer.objects.all()

    def list(self, request, *args, **kwargs):
        try:

            semi_trailers = self.get_queryset()
            serializer = self.get_serializer(instance=semi_trailers, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data={'error': str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get_object(self):
        try:
            pk = self.kwargs.get('pk')
            semi_trailer = SemiTrailer.objects.get(pk=pk)
            return semi_trailer
        except Exception as e:
            raise Exception(f'Error:{str(e)}')

    def create(self, request, *args, **kwargs):
        try:
            print(request.data)
            if request.data['semi_note'] == 'false':
                request.data['semi_note'] = False
            else:
                request.data['semi_note'] = True
            print(request.data['production_year'])
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.create(request.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(data={'error': str(e)},
                            status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        try:
            semi_trailer = self.get_object()
            serializer = SemiTrailerSerializer(instance=semi_trailer)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response(data={'error':str(e)},
                            status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(data={'error':str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, *args, **kwargs):
        try:
            data = request.data
            semi_trailer = self.get_object()
            serializer = SemiTrailerSerializer(
                data=data,
                instance=semi_trailer,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.update(semi_trailer, data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data={'error':str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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
            return Response(data={'error': str(e)},
                            status=status.HTTP_400_BAD_REQUEST)


class SemiTruckEquipmentDetail(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTAuthentication,)
    serializer_class = SemiTrailerEquipmentSerializer
    lookup_url_kwarg = 'pk'

    def get_object(self):
        semitailer_id = self.kwargs.get(self.lookup_url_kwarg)
        return SemiTrailerEquipment.objects.get(semi_trailer_id=semitailer_id)

    def retrieve(self, request, *args, **kwargs):
        try:
            semi_equipment = self.get_object()
            serializer = self.get_serializer(instace=semi_equipment)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data={'error': str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, *args, **kwargs):
        try:
            data = self.request
            semi_equipment = self.get_object()
            serializer = self.get_serializer(data=data,
                                             instance=semi_equipment,
                                             partial=True)
            serializer.is_valid(raise_exception=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data={'error': str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class SemiTrailerEquipmentList(ListAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTAuthentication,)
    serializer_class = SemiTrailerEquipmentSerializer

    def get_queryset(self):
        return SemiTrailerEquipment.objects.all()

    def list(self, request, *args, **kwargs):
        try:
            semi_equipments = self.get_queryset()
            serializer = self.get_serializer(semi_equipments, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data={'error': str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)