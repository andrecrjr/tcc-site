from django.shortcuts import render
from rest_framework import generics

from .models import *
from .serializers import *

class ProfileList(generics.ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class ProfileDetails(generics.RetrieveAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class ItemList(generics.ListAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

class ItemDetails(generics.RetrieveAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

