from rest_framework import serializers
from registration.models.User.model import User as CustomUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            'id', 'username', 'password', 'first_name', 'last_name',
            'birth_date', 'phone', 'email', 'role', 'city', 'parent_name',
            'parent_phone', 'rank', 'rank_date'
        ]
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            phone=validated_data.get('phone', ''),
            birth_date=validated_data.get('birth_date', None),
            email=validated_data.get('email', ''),
            role=validated_data.get('role', 'guest'),
            city=validated_data.get('city', ''),
            parent_name=validated_data.get('parent_name', ''),
            parent_phone=validated_data.get('parent_phone', ''),
            rank=validated_data.get('rank', ''),
            rank_date=validated_data.get('rank_date', None),
        )
        return user