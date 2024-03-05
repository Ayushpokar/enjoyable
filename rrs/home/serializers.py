# create restframework serializers  
"""
This module contains the serializer classes for our REST API.  These are used to convert between Python objects and JSON format when we send data to
This is the Serializer for our User model.  It will be used to convert a User object into JSON and vice versa when we interact
Serializer for user model.
"""

'''
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *

class trainserializer(serializers.ModelSerializer):
    class Meta:
        model = train_master
        fields=('train_no','train_name', 'source_station', 'dest_station','depart_datetime','arrival_datetime','journey_duration',
                'available_seats','total_seats')
class bookingserializer(serializers.ModelSerializer):
            """Serializer for the Booking model."""
            
            class Meta:
                model = booking
                fields = ('id', 'user', 'train', 'journey_date', 
                          'booking_type', 'no_of_passengers', ) 
                
'''
        
'''
class UserSerializer(serializers.Model):
    """User Serializer."""
    
    class Meta:
        model = User
        fields = ('username', 'email')
        
# Create a new user and validate the data before saving to database
class UserCreateSerializer(serializers.ModelSerializer):
    """Handler for creating users in the system.""" 
    password2 = serializers.CharField(label='Password confirmation', write_only=True)
                              
    def validate_password(self, value):
        # Check if password matches confirmation
        data = self.get_initial()
        password = data.get('password')
        if not value or not password:
            raise serializers.ValidationError("Please ")
        if value != password:
            raise serializers.ValidationError("Passwords do not match")
        return value
            
    def create(self, validated_data):
        # Use the standard create function to handle creation of new users
        return User.objects.create_user(**validated_data)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def Passmassserializer(self, *args, **kwargs):
        """Override the original method to include password field"""
        kwargs['context'] = {'request': self.context['request']}
        return super(UserCreateSerializer, self).to_representation(*args, **kwargs) 
'''    