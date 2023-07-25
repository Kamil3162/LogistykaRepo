from Applications.TruckManage.models import Truck
from rest_framework import serializers
from django.db import IntegrityError

class TruckSerializer(serializers.ModelSerializer):
    class Meta:
        model = Truck
        fields = '__all__'

    def create(self, validated_data):
        try:
            truck = Truck.objects.create(
                **validated_data
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


