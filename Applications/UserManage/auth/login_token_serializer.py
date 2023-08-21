from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.core import serializers
from Applications.UserManage.serializers import UserDetailSerializer
class CustomTokenObtainSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        # data - return dict (access, refresh_token)
        # after invoke validate we have access to user instance
        data = super(CustomTokenObtainSerializer, self).validate(attrs)
        user = self.user

        permission_groups = user.groups.all()
        permission_names = user.get_all_permissions()
        user_serialized = UserDetailSerializer(instance=user)

        data['permissions'] = {
          str(x): x for x in permission_names
        }
        data['user'] = user_serialized.data
        data['permission_group'] = serializers.serialize('json', permission_groups)

        print(data)
        return data