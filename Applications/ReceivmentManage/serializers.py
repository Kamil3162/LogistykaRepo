import datetime
from django.utils import timezone
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import (
    Receivment,
    SemiTrailerReportPhoto,
    TruckReportPhoto,
    ReceivmentLocations,
    LocationHistory
)

from ..UserManage.models import CustomUser
from ..UserManage.serializers import UserSerializer
from ..TruckManage.serializers import TruckSerializer
from ..SemitruckManage.serializers import SemiTrailerSerializer
from django.db import IntegrityError

class ReceivmentsSerializer(serializers.ModelSerializer):
    source_user_name = serializers.CharField(source='source_user.first_name', read_only=True)
    source_user_surname = serializers.CharField(source='source_user.last_name', read_only=True)
    destination_user_name = serializers.CharField(source='destination_user.first_name', read_only=True)
    destination_user_surname = serializers.CharField(source='destination_user.last_name', read_only=True)
    truck_registration_number = serializers.CharField(source='truck.registration_number', read_only=True)
    semitrailer_registration_numer = serializers.CharField(source='semi_trailer.registration_number', read_only=True)

    class Meta:
        model = Receivment
        fields = [
            'id',
            'source_user_name',
            'source_user_surname',
            'destination_user_name',
            'destination_user_surname',
            'truck_registration_number',
            'semitrailer_registration_numer',
        ]

class ReceivmentsSerializerDetail(serializers.ModelSerializer):

    truck = TruckSerializer()
    semi_trailer = SemiTrailerSerializer()
    destination_user = UserSerializer()
    source_user = UserSerializer()

    class Meta:
        model = Receivment
        fields = '__all__'


class ReceivmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Receivment

    def create(self, validated_data):
        try:
            # destination user is a driver who took truck
            # source user is a manager those apply document
            receivment = Receivment.objects.create(
                destination_user=validated_data.get('destination_user'),
                source_user=validated_data.get('source_user'),
                truck=validated_data.get('truck'),
                semi_trailer=validated_data.get('semi_trailer'),
                destination=validated_data.get('destination')
            )
            return receivment
        except Exception as e:
            raise Exception(str(e))

    def finish_receivment(self, instance):
        try:
            instance.status = Receivment.StatusChoices.FINISHED
            instance.date_finished = timezone.now()
            instance.save()

            finish_receivment = Receivment.objects.create(
                source_user=instance.destination_user,
                destination_user=instance.source_user,
                semi_trailer=instance.semi_trailer,
                truck=instance.truck,
                status=Receivment.StatusChoices.FINISHED,
                receivment_type=Receivment.ReceivmentType.DRIVER
            )
            return finish_receivment

        except Exception:
            raise Exception("Something is bad")

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()

class TruckReportPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TruckReportPhoto
        fields = '__all__'

    def create(self, validated_data):
        try:
            truck_photo = TruckReportPhoto.objects.create(**validated_data)
        except Exception as e:
            raise Exception(str(e))

class SemiTrailerReportPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = SemiTrailerReportPhoto
        fields = '__all__'

    def create(self, validated_data):
        try:
            semitrailer = SemiTrailerReportPhoto.objects.create(**validated_data)
        except Exception as e:
            raise Exception(str(e))


class FinalLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReceivmentLocations
        fields = '__all__'

    def create(self, validated_data):
        try:
            final_location = ReceivmentLocations.objects.create(
                **validated_data
            )
        except IntegrityError as e:
            raise IntegrityError("Record exists in db")
        except ValidationError as e:
            raise ValidationError(
                "Serializer raise following errors:{}".format(str(e))
            )
        except Exception as e:
            raise e

    def update(self, instance, validated_data):
        for key, value in validated_data.keys():
            setattr(instance, key, value)
        instance.save()

class LocationHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = LocationHistory
        fields = ('__all__',)

    def create(self, validated_data):
        try:
            location_history = LocationHistory.objects.create(**validated_data)
        except Exception as e:
            raise Exception(str(e))

    def update(self, instance, validated_data):
        for key, value in validated_data.keys():
            setattr(instance, key, value)
        instance.save()

    def __delete__(self, instance):
        pass
