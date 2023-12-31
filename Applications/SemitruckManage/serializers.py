from rest_framework import serializers
from .models import SemiTrailer, SemiTrailerEquipment
from django.db import IntegrityError
class SemiTrailerSerializer(serializers.ModelSerializer):
    class Meta:
        model = SemiTrailer
        fields = '__all__'

    def create(self, validated_data):
        try:
            semi_trailer = SemiTrailer.objects.create(
                brand=validated_data.get('brand'),
                model=validated_data.get('model'),
                registration_number=validated_data.get('registration_number'),
                production_year=validated_data.get('production_year'),
                semi_note=validated_data.get('semi_note'),
                photo=validated_data.get('photo'),
                available=validated_data.get('available')
            )
        except IntegrityError:
            raise IntegrityError("Following data exists in db change registration number")
        except Exception as e:
            raise Exception(str(e))

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()
        return instance


class SemiTrailerEquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = SemiTrailerEquipment
        fields = '__all__'

    def create(self, validated_data):
        try:
            semitrailer_equip = SemiTrailerEquipment.objects.create(
                semi_trailer=validated_data.get('semi_trailer'),
                belts=validated_data.get('belts'),
                corners=validated_data.get('corners'),
                aluminium_stick=validated_data.get('aluminium_stick'),
                wide_stick=validated_data.get('wide_stick'),
                ladder=validated_data.get('ladder'),
                roof_stick=validated_data.get('roof_stick'),
                dimenstion_board=validated_data.get('dimenstion_board')
            )
            return semitrailer_equip
        # except IntegrityError:
        #     raise IntegrityError(f"Semi Trailer:{self.validated_data.get('semi_trailer').id}"
        #                          f" Already have equipment ")
        except Exception as e:
            raise Exception(str(e))

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()
        return instance
