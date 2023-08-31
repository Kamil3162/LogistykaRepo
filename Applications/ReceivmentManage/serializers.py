import datetime
from django.utils import timezone
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import Receivment, SemiTrailerReportPhoto, TruckReportPhoto
from ..UserManage.models import CustomUser

class ReceivmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Receivment
        fields = '__all__'

    def create(self, validated_data):
        try:
            # destination user is a driver who took truck
            # source user is a manager those apply document
            receivment = Receivment.objects.create(
                destination_user=validated_data.get('destination_user'),
                source_user=validated_data.get('source_user'),
                truck=validated_data.get('truck'),
                semi_trailer=validated_data.get('semi_trailer'),
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

