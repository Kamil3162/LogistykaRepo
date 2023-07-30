from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import Receivment
class ReceivmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Receivment
        fields = '__all__'

    def create(self, validated_data):
        try:
            state = 'Wolny'

            transfer_user = validated_data.get('transferring_user')

            active_receivments = Receivment.objects.filter(
                status__exact=False, transferring_user=transfer_user
            ).first()

            truck = validated_data.get('truck')

            semi_trailer = validated_data.get('semi_trailer')

            if active_receivments is not None:
                raise ValidationError("You have active receivment, "
                                      "you cant have more than one")
            elif truck.avaiable is not state and \
                semi_trailer.statys is not state :
                raise ValidationError("You cant assign busy truck or semitrailer")

            receivment = Receivment.objects.create(
                truck=validated_data.get('truck'),
                semi_trailer=validated_data.get('semi_trailer'),
                transferring_user=validated_data.get('transferring_user'),
                sender=validated_data.get('sender')
            )
        except Exception as e:
            raise Exception(str(e))

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()



