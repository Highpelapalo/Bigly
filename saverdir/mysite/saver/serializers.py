from .models import Client, Data
from rest_framework import serializers

class DataSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Data
        fields = ('url', 'client', 'command', 'data', 'created_time')

class ClientSerializer(serializers.HyperlinkedModelSerializer):
    #related_data = DataSerializer(source='data_set') #{data['command']: data['data'] for data in DataSerializer(Data.objects.all())}
    class Meta:
        model = Client
        fields = ('url', 'name', 'version', 'created_time', 'related_data')
