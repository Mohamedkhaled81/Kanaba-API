"""
custom validation for register
"""
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

from rest_framework import serializers



def validate_name(value):
        reg = RegexValidator(r'^[A-Za-z]+$', 'Name can only contain English letters')
        try:
            reg(value)
        except ValidationError as e:
            raise serializers.ValidationError(str(e))

def validate_passwords(password, password1):
    if password != password1:
        raise serializers.ValidationError('Passwords must match.')
    
    reg = RegexValidator(r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[.!@#$%^&*-]).{8,}$',
                         'Password must be at least 8 characters and contain at least one digit,one lowercase letter, one uppercase letter, and one special character.')
    try:
        reg(password)
    except ValidationError as e:
        raise serializers.ValidationError(str(e))
