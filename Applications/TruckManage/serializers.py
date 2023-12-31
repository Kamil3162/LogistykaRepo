from Applications.TruckManage.models import Truck, TruckEquipment
from rest_framework import serializers
from django.db import IntegrityError

class TruckSerializer(serializers.ModelSerializer):
    class Meta:
        model = Truck
        fields = '__all__'

    def create(self, validated_data):
        try:
            truck = Truck.objects.create(
                brand=validated_data.get('brand'),
                model=validated_data.get('model'),
                power=validated_data.get('power'),
                registration_number=validated_data.get('registration_number'),
                driven_length=validated_data.get('driven_length'),
                production_date=validated_data.get('production_date'),
                available=validated_data.get('available'),
                photo=validated_data.get('photo'),
            )
            return truck
        except IntegrityError:
            raise IntegrityError("In db already exists similar truck")
        except Exception as e:
            raise Exception(str(e))

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()
        return instance

    def change_state(self, instance, state):
        try:
            valid_states = [option[0] for option in Truck.CHOICES]
            if state in valid_states:
                instance.avaiable = state
                instance.save()
                return instance
        except KeyError:
            raise KeyError("No valid kay in our options")


class TruckEquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TruckEquipment
        exclude = ('photo',)

    def create(self, validated_data):
        try:
            truck_equipment = TruckEquipment.objects.create(
                **validated_data
            )
            return truck_equipment
        except Exception as e:
            print(str(e))

    def update(self, instance, validated_data):
        try:
            for value, key in validated_data:
                instance.key = value
            instance.save()
            return instance
        except Exception as e:
            print(str(e))
