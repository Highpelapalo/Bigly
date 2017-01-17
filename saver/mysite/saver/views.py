from django.shortcuts import render
from rest_framework import generics, viewsets
from .serializers import ClientSerializer, DataSerializer
from .models import Client, Data

class ClientViewSet(viewsets.ModelViewSet):
    queryset =  Client.objects.all()
    serializer_class = ClientSerializer

    #def perform_create(self,serializer):
    #    serializer.save(owner=self.request.user)

class DataViewSet(viewsets.ModelViewSet):
    queryset =  Data.objects.all()
    serializer_class = DataSerializer

class ClientViewName(generics.ListAPIView):
    serializer_class = ClientSerializer

    def get_queryset(self):
        clientname = self.kwargs['name']
        return Client.objects.filter(name=clientname)

    #def perform_create(self, serializer):
    #    serializer.save(owner=self.request.user)

# Create your views here.
