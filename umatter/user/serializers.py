from .models import User

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id', 'username', 'email',
            'kakao_id', 'kakao_nickname',
            'profile_thumbnail',
            # 'verified_email', 'verified_phone_number'
            'is_staff', 'is_active',
            'created', 'modified'
        )
        read_only_fields = (
            'id', 'email',
            'kakao_id', 'kakao_nickname',
            'profile_thumbnail',
            'is_staff', 'created',
            'is_admin', 'is_superuser',
            # 'modified', 'is_active',
        )
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        # instance.email = validated_data.get('email', instance.email)
        instance.set_password(validated_data.get('password', instance.password))
        instance.save()
        return instance