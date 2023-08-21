from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import CreateAPIView, DestroyAPIView
from rest_framework_simplejwt import authentication
from rest_framework import permissions
from .serializers import ReceivmentSerializer
from .models import Receivment
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from ..UserManage.models import CustomUser
from ..TruckManage.models import Truck
from ..SemitruckManage.models import SemiTrailer
from .utils.select_manager import ManagerSelect
from rest_framework.exceptions import ValidationError
class ReceivmentViewSet(ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (authentication.JWTAuthentication, )
    serializer_class = ReceivmentSerializer
    queryset = Receivment.objects.all()

    def create(self, request, *args, **kwargs):
        try:
            print("esa")
            state_busy = 'Zajety'
            manager_chose = ManagerSelect()
            data = request.data

            sender = get_object_or_404(CustomUser, pk=data.get('sender'))
            transferring_user = manager_chose.chose_random_manager()
            data['transferring_user'] = transferring_user.pk

            truck = get_object_or_404(Truck, pk=data.get('truck'))
            semi_trailer = get_object_or_404(SemiTrailer,
                                             pk=data.get('semi_trailer'))

            information_response = dict()
            status_code = None

            '''
               This method is invoke when I call is_valid function
           '''
            print("naura")
            print(data)
            active_receivments = Receivment.objects.filter(
                status__exact=False, transferring_user=data['transferring_user']
            )

            print(active_receivments)
            print("naura")
            if len(active_receivments) > 0:
                return Response(data={"error": "You have active receivment, "
                                      "you cant have more than one"},
                                status=status.HTTP_400_BAD_REQUEST)

            if sender.is_active and truck.is_available\
                    and semi_trailer.is_available:
                serializer_receivment = self.get_serializer(data=data)
                serializer_receivment.is_valid(raise_exception=True)

                data['sender'] = sender
                data['transferring_user'] = transferring_user
                data['truck'] = truck
                data['semi_trailer'] = semi_trailer

                serializer_receivment.create(data)

                truck.update_state(state_busy)
                semi_trailer.update_state(state_busy)

                status_code = status.HTTP_201_CREATED
                information_response['success'] = serializer_receivment.data
            else:
                status_code = status.HTTP_409_CONFLICT
                information_response['error'] = 'Check user status,\
                 truck, semitrailer'

            return Response(data=information_response, status=status_code)
        except Exception as e:
            return Response(data={'error': str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, *args, **kwargs):
        try:
            data = request.data
            transferring_user = self.request

            receivment_instance = Receivment.objects.get(
                transferring_user=transferring_user,
                status__exact=False
            )

            serializer = self.get_serializer(
                data,
                instance=receivment_instance,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.update(receivment_instance, data)
            return Response(serializer.data, status.HTTP_200_OK)
        except Receivment.DoesNotExist as e:
            return Response(data={'error': str(e)},
                            status=status.HTTP_404_NOT_FOUND)
        except Receivment.MultipleObjectsReturned as e:
            return Response(data={'error': str(e)},
                            status=status.HTTP_409_CONFLICT)






