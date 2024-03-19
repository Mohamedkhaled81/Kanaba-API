"""
User Serilaizers
"""
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .validators import validate_name, validate_passwords
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate



class CustomerSerilaizer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        style={'input_type': 'password'}
    )
    password1 = serializers.CharField(
        style={'input_type': 'password'},
        write_only=True
    )
    email = serializers.EmailField(validators=[UniqueValidator(
        queryset=get_user_model().objects.filter(role="Customer"))])
    first_name = serializers.CharField(validators=[validate_name])
    last_name = serializers.CharField(validators=[validate_name])

    class Meta:
        model = get_user_model()
        fields = [
            'first_name', 'last_name', 'email',
            'password','password1'
        ]

    def validate(self, attrs):
        password = attrs.get('password')
        password1 = attrs.get('password1')
        validate_passwords(password, password1)
        del attrs['password1']
        return attrs

    def create(self, validated_data):
        user = get_user_model().objects.create_user(
            **validated_data, role='Customer',
        )
        return user

class CustomerLoginSerializer(serializers.Serializer):

    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        write_only=True,
    )
    
    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        user = authenticate(username=email,password=password)
        if not user:
            if get_user_model().objects.filter(email=email).exists():
                raise serializers.ValidationError(
                    'Invalid password')
            raise serializers.ValidationError(
                'Email not found')
        attrs['user'] = user
        return attrs

