from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework_simplejwt import authentication
from rest_framework import permissions
from .serializers import ReceivmentSerializer, \
    ReceivmentsSerializer, \
    ReceivmentsSerializerDetail, \
    LocationHistorySerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.exceptions import ValidationError
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from django.shortcuts import get_object_or_404
from ..UserManage.models import CustomUser
from ..TruckManage.serializers import TruckSerializer
from ..SemitruckManage.serializers import SemiTrailerSerializer
from ..TruckManage.models import Truck
from ..SemitruckManage.models import SemiTrailer
from .utils.select_manager import ManagerSelect
from .models import Receivment, ReceivmentLocations, LocationHistory


class CustomPagination(PageNumberPagination):
    page_size = 5

class ReceivmentModelViewSet(ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (authentication.JWTAuthentication,)
    serializer_class = ReceivmentsSerializerDetail
    pagination_class = CustomPagination
    queryset = Receivment.objects.select_related(
        'destination_user',
        'source_user',
        'semi_trailer',
        'truck'
    )

    @action(detail=True, methods=['POST'], name='Finish active receivment')
    def finish_receivment(self, request, pk):
        try:
            '''
                We wannna get vehicle and receivment instace details to
                perform finish action on our receivment and change state 
                in ours vehicles. Change State is crucial because we wanna
                use these vehicles in next future receivments
            '''
            status_choices = SemiTrailer.CHOICES
            data = {
                'available': status_choices[1][0]
            }

            receivment_instance = Receivment.objects.get(pk=pk)
            semi_trailer = receivment_instance.semi_trailer
            truck = receivment_instance.truck

            serializer = self.get_serializer(instance=receivment_instance)
            serializer.finish_receivment(receivment_instance)
            truck_serializer = TruckSerializer.update(instance=truck,
                                                      validated_data=data)
            semitrailer_serializer = SemiTrailerSerializer.update(
                instance=semi_trailer, validated_data=data
            )
            return Response(data={'success': 'success'},
                            status=status.HTTP_200_OK)
        except Exception:
            return Response(data={'success': 'success'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # def list(self, request, *args, **kwargs):
    #     return super().list(request, *args, **kwargs)


class ReceivmentCreateView(CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (authentication.JWTAuthentication, )
    serializer_class = ReceivmentSerializer
    queryset = Receivment.objects.all()

    def create(self, request, *args, **kwargs):
        try:
            '''
                Sender is a driver those wanna create new receivment
                Transferring user is a manager which rent a car
            '''
            state_busy = SemiTrailer.get_choices()[1][1]
            manager_chose = ManagerSelect()
            data = request.data
            transferring_user = manager_chose.chose_random_manager()
            sender = get_object_or_404(CustomUser, pk=data.get('destination_user'))

            truck = get_object_or_404(Truck, pk=data.get('truck'))

            semi_trailer = get_object_or_404(SemiTrailer,
                                             pk=data.get('semi_trailer'))

            information_response = dict()
            status_code = None

            # we return instance of receivment with all data
            driver_location = Receivment.driver_manager.get_latest_driver_location(
                driver=sender
            ).destination

            literal_driver_location = driver_location.concatination_address()

            # receivment location to drive
            target_location = Receivment.driver_manager.pick_receivment(
                literal_driver_location
            )

            data['source_user'] = transferring_user.pk
            data['destination_user'] = sender.pk
            data['truck'] = truck.pk
            data['semi_trailer'] = semi_trailer.pk
            data['destination'] = target_location.pk

            # If active receivment is not None we cant create new receivment
            active_receivments = Receivment.objects.filter(
                status__exact=False, destination_user=data['destination_user']
            )

            if len(active_receivments) > 0:
                return Response(data={"error": "You have active receivment, "
                                      "you cant have more than one"},
                                status=status.HTTP_400_BAD_REQUEST)

            if truck.is_available and semi_trailer.is_available:
                serializer_receivment = self.get_serializer(data=data)
                serializer_receivment.is_valid(raise_exception=True)

                data_location = {
                    'city': target_location.city,
                    'street': target_location.street,
                    'apartment_number': target_location.apartment_number
                }

                data['source_user'] = sender
                data['destination_user'] = transferring_user
                data['truck'] = truck
                data['semi_trailer'] = semi_trailer
                data['destination'] = target_location

                receivment = serializer_receivment.create(data)

                location_history_data = {
                    'receivment': receivment.pk,
                    'location': f'{data_location.get("city")} \
                    {data_location.get("street")} \
                    {data_location.get("apartment_number")}'
                }

                location_history_serializer = LocationHistorySerializer(
                    data=location_history_data)
                location_history_serializer.is_valid(raise_exception=True)
                location_history_data['receivment'] = receivment
                location_history_serializer.create(location_history_data)

                # code responsible for update state of machines to busy
                truck.update_state(state_busy)
                semi_trailer.update_state(state_busy)

                status_code = status.HTTP_201_CREATED
                information_response['success'] = serializer_receivment.data
            else:
                status_code = status.HTTP_409_CONFLICT
                information_response['error'] = 'Check user status,\
                 truck, semitrailer and format location'

            return Response(data=information_response, status=status_code)
        except Exception as e:
            return Response(data={'error': str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except KeyError as e:
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

class ActiveUserReceivment(RetrieveUpdateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (authentication.JWTAuthentication,)
    serializer_class = ReceivmentSerializer
    queryset = Receivment.objects.all()

    def get_object(self):
        try:
            user = self.request.user    # this instace to make an filter
            receivment_statuses = Receivment.get_statuses()
            receivment = self.get_queryset().get(
                destination_user=user,
                status=receivment_statuses.IN_PROGESS
            )
            return receivment
        except Receivment.DoesNotExist:
            print("Using following data i cant find similar or exact object")
        except Receivment.MultipleObjectsReturned:
            print("Query return more than two objects")
        except Exception as e:
            print(str(e))

    def retrieve(self, request, *args, **kwargs):
        try:
            receivment_object = self.get_object()
            serializer = self.get_serializer(instance=receivment_object)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {'error':str(e)},
                status=status.HTTP_400_BAD_REQUEST
             )

class CreateLocationApiView(CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (authentication.JWTAuthentication,)
    serializer_class = ReceivmentSerializer


class UpdateLocationApiView(RetrieveUpdateDestroyAPIView):
    pass


