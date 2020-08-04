from rest_framework import serializers
from django.contrib.auth.models import User
from django.core import validators
from django.db.models.fields import CharField

from usermanagement.models import (InterviewerProfile, CandidateProfile, 
                                    InterviewSlot)
from usermanagement.CustomMessages import CustomMessages


msg_ob = CustomMessages()
phone_number_validator = validators.RegexValidator(r"^[ .0-9+]+$", 'Please enter a valid phone number.')

class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True, 'min_length': 8},
                        'email': {'required': True, 'allow_null': False}}

    def validate_email(self, email):
        if not email:
            raise serializers.ValidationError(msg_ob.email_empty) 
        elif User.objects.filter(email=email).exists():
            raise serializers.ValidationError(msg_ob.email_exists)
        else:    
            return email

    def validate(self, data):
        phone_number = self.initial_data.get('phone_number')
        phone_number_validator(phone_number)
        if not phone_number:
            raise serializers.ValidationError(msg_ob.phone_number_empty)
        elif User.objects.filter(username=phone_number).exists():
            raise serializers.ValidationError(msg_ob.phone_number_exists)
        else:
            return data

    def validate_first_name(self, first_name):
        if not first_name:
            raise serializers.ValidationError(msg_ob.first_name_empty)
        else:
            return first_name

    def create(self, validated_data):
        validated_data['username'] = self.initial_data['phone_number']
        return User.objects.create_user(**validated_data)

    def __init__(self, *args, **kwargs):
        super(UserProfileSerializer, self).__init__(*args, **kwargs)


class InterviewSlotSerializer(serializers.ModelSerializer):

    class Meta:
        model = InterviewSlot
        fields = ('interviewer', 'candidate', 'slot')

    def validate_slot(self, value):
        return value

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)
        super(InterviewSlotSerializer, self).__init__(*args, **kwargs)
        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)


class InterviewerSerializer(serializers.ModelSerializer):
    email = serializers.SerializerMethodField()
    first_name = serializers.SerializerMethodField()

    class Meta:
        model = InterviewerProfile
        fields = ('id', 'first_name', 'phone_number', 'email')

    def get_email(self, obj):
        return obj.user.email

    def get_first_name(self, obj):
        return obj.user.first_name

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)
        super(InterviewerSerializer, self).__init__(*args, **kwargs)
        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)


class CandidateSerializer(serializers.ModelSerializer):
    email = serializers.SerializerMethodField()
    first_name = serializers.SerializerMethodField()

    class Meta:
        model = CandidateProfile
        fields = ('id', 'first_name', 'phone_number', 'email')

    def get_email(self, obj):
        return obj.user.email

    def get_first_name(self, obj):
        return obj.user.first_name

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)
        super(CandidateSerializer, self).__init__(*args, **kwargs)
        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)