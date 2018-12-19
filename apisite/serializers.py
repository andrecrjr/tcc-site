from rest_framework import serializers
from .models import *
from rest_framework.authtoken.models import Token

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username', 'first_name', 'last_name', 'email')

class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=True)
    class Meta:
        model = Profile
        fields = ('user',)
    
    def create(self, validated_data):
        """
        Overriding the default create method of the Model serializer.
        :param validated_data: data containing all the details of profile
        :return: returns a successfully created profile record
        """
        user_data = validated_data.pop('user')
        user = UserSerializer.create(UserSerializer(), validated_data=user_data)
        profile = Profile.objects.update_or_create(user=user)
        return profile

class InventarioSerializer(serializers.ModelSerializer):
    usuario = ProfileSerializer(required=True)
    class Meta:
        model = Inventario
        fields = ('usuario',)

    def create(self, validated_data):
        user_data = validated_data.pop('usuario')
        user = ProfileSerializer.create(ProfileSerializer(), validated_data=user_data)
        inventario = Invetario.objects.update_or_create(usario=user)
        return inventario

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'

class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = ('key', 'user')