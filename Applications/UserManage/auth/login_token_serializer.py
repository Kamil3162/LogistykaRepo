from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.core import serializers
class CustomTokenObtainSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        # data - return dict (access, refresh_token)
        # after invoke validate we have access to user instance
        data = super(CustomTokenObtainSerializer, self).validate(attrs)

        permission_groups = self.user.groups.all()
        permission_names = permission_groups[0].permissions.values_list('codename', flat=True)

        data['permissions'] = {
            str(x): x for x in permission_names
        }
        data['permission_group'] = serializers.serialize('json', permission_groups)

        return data