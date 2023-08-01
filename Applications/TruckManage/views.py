from rest_framework.generics import (
    CreateAPIView,
    RetrieveUpdateDestroyAPIView
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializers import (
    TruckSerializer
)
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Truck
from django.http import Http404

# find . -path "*/__pycache__" -type d -exec rm -r {} ';'

class TruckCreate(CreateAPIView):
    permission_classes = (IsAuthenticated, )
    authentication_classes = (JWTAuthentication, )
    serializer_class = TruckSerializer

    def create(self, request, *args, **kwargs):
        try:
            # parse and change format of our data
            data = request.data
            serializer = TruckSerializer(data=data)

            # part of validation and create truck
            serializer.is_valid(raise_exception=True)
            truck = serializer.create(data)
            truck.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)},
                            status=status.HTTP_400_BAD_REQUEST)

class TruckDetailView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated, )
    authentication_classes = (JWTAuthentication, )
    serializer_class = TruckSerializer
    lookup_url_kwarg = 'pk'

    def get_object(self):
        try:
            pk = self.kwargs.get(self.lookup_url_kwarg)
            truck = Truck.objects.get(pk=pk)
            return truck
        except Truck.DoesNotExist:
            raise Http404("Object not found")

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

class TruckViewAdmin:
    pass



