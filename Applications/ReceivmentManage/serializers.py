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
            receivment = Receivment.objects.create(
                sender=validated_data.get('sender'),
                transferring_user=validated_data.get('transferring_user'),
                truck=validated_data.get('truck'),
                semi_trailer=validated_data.get('semi_trailer')
            )
            return receivment
        except Exception as e:
            raise Exception(str(e))

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

