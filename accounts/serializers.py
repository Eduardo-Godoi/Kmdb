from rest_framework import serializers

from accounts.models import User


class CriticSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id',  'first_name', 'last_name']


class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    is_staff = serializers.BooleanField()
    is_superuser = serializers.BooleanField()

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
