from rest_framework import serializers
from addLocation.serializers import *
from viewCases.serializers import *
from addLocation.models import *
from viewCases.models import *


class LocationClusteringSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        exclude = ('address',)

class CaseRecordClusteringSerializer(serializers.ModelSerializer):
    class Meta:
        model = CaseRecord
        exclude = ('localOrImported','patient',)

class ClusteringDataSerializer(serializers.Serializer):
    location = LocationClusteringSerializer()
    dateFrom = serializers.DateField()
    dateTo = serializers.DateField()
    category = serializers.CharField(max_length=20)
    caseRecord = CaseRecordClusteringSerializer()

    def create(self, validated_data):
        return validated_data