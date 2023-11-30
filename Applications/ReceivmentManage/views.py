from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from rest_framework_simplejwt import authentication
from rest_framework import permissions
from .serializers import ReceivmentSerializer, \
    ReceivmentsSerializer, \
    ReceivmentsSerializerDetail, \
    LocationHistorySerializer, FinalLocationSerializer
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
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.forms.models import model_to_dict
from django.utils import timezone

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

            receivment_instance = Receivment.objects.get(pk=pk)

            semi_trailer = receivment_instance.semi_trailer
            truck = receivment_instance.truck

            status_choices = SemiTrailer.CHOICES
            data = {
                'available': status_choices[0][0]
            }

            serializer = self.get_serializer(instance=receivment_instance)
            serializer.finish_receivment(receivment_instance)

            truck_serializer = TruckSerializer(
                instance=truck,
                data=data,
                partial=True
            )

            semitrailer_serializer = SemiTrailerSerializer(
                instance=semi_trailer,
                data=data,
                partial=True
            )

            if truck_serializer.is_valid():
                truck_serializer.save()
            else:
                raise ValueError("Invalid data for truck update")


            if semitrailer_serializer.is_valid():
                semitrailer_serializer.save()
            else:
                raise ValueError("Invalid data for truck update")


            return Response(data={'success': 'success'},
                            status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data={'error': str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ReceivmentCreateView(CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (authentication.JWTAuthentication, )
    serializer_class = ReceivmentSerializer
    queryset = Receivment.objects.all()

    def create(self, request, *args, **kwargs):
        try:
            """
            Create a new receivment based on the provided data.
        
            Args:
                request: The HTTP request object.
                data: The data containing information for creating the receivment.
        
            Returns:
                dict: A dictionary containing information about the created receivment.
            """
            data = request.data

            driver_location = None
            information_response = dict()
            status_code = None

            state_busy = SemiTrailer.get_choices()[1][1]
            manager_chose = ManagerSelect()
            transferring_user = manager_chose.chose_random_manager()


            sender = get_object_or_404(CustomUser, pk=data.get('destination_user'))
            truck = get_object_or_404(Truck, pk=data.get('truck'))
            semi_trailer = get_object_or_404(SemiTrailer,
                                             pk=data.get('semi_trailer'))

            # we return instance of receivment with all data
            driver_location = Receivment.driver_manager.get_latest_driver_location(
                driver=sender
            )

            if driver_location is False:
                driver_location = ReceivmentLocations.location_manager.get_base_location()

            literal_driver_location = driver_location.concatination_address()

            # this function calculate the closest place to delivery
            # return instance those we need to create new instance in our db
            target_location = Receivment.driver_manager.pick_receivment(
                literal_driver_location
            )

            print(target_location)

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

                data['source_user'] = transferring_user
                data['destination_user'] = sender
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
    serializer_class = ReceivmentsSerializerDetail
    queryset = Receivment.objects.all()

    # also i should return location and data aobut vehickles
    def get_object(self):
        try:
            user = self.request.user    # this instace to make an filter
            receivment = Receivment.driver_manager.get_active_receivement(user)
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
    serializer_class = FinalLocationSerializer

    def create(self, request, *args, **kwargs):
        try:
            data = request.data
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.create(data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as e:  # Catch validation errors specifically
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'detail': str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class HandeLocationHistoryApiView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (authentication.JWTAuthentication,)

    def get_queryset(self):
        """
            This function should return two instance from LocationHistory
            So we havbe two option - we have two instance one or 0
        """
        user = self.request.user
        active_user_receivment = Receivment.driver_manager.get_active_receivement(user)
        queryset = LocationHistory.objects.filter(
            receivment=active_user_receivment
        ).order_by('updated_at')
        return active_user_receivment, queryset

    def put(self, request, *args, **kwargs):
        try:
            user = request.user
            data = request.data
            active_receivment, last_locations = self.get_queryset()

            if last_locations.count() < 2:
                return Response({'error': 'we have to create new instance using post method'},
                                status=status.HTTP_404_NOT_FOUND)
            else:
                data['receivment'] = active_receivment.pk
                data['updated_at'] = timezone.now()

                # Get the last location if it exists
                last_location = last_locations.first()

                # {"error": "we have to create new instance using post method"}

                if last_location is not None:
                    # Prepare the serializer with the instance and data
                    serializer = LocationHistorySerializer(
                        instance=last_location,
                        data=data,
                        partial=True
                    )
                    # Validate the data
                    serializer.is_valid(raise_exception=True)
                    # Save the instance (update)
                    serializer.save()
                    return Response(serializer.data,
                                    status=status.HTTP_202_ACCEPTED)
                # Handle the case where there is no last location
                return Response(
                    {'error': 'No existing location found to update.'},
                    status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, *args, **kwargs):
        try:
            print("sukces")
            user = self.request.user
            receivment = Receivment.driver_manager.get_active_receivement(user)
            data = request.data
            data['receivment'] = receivment.pk
            if receivment is not None:
                serializer = LocationHistorySerializer(data=data)
                serializer.is_valid(raise_exception=True)
                data['receivment'] = receivment
                serializer.create(data)
                print("sukces")
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response({'error': 'lack of active receivments'},
                            status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request, *args, **kwargs):
        try:
            receivment, locations_history = self.get_queryset()
            serializer = LocationHistorySerializer(locations_history, many=True)
            print(serializer.data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)},
                            status.HTTP_500_INTERNAL_SERVER_ERROR)
