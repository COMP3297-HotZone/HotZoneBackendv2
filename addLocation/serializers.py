from rest_framework import serializers
from .models import VisitedLocation
from .models import Location
from viewCases.models import CaseRecord
from viewCases.serializers import *

class LocationSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    address = serializers.CharField(max_length=500, allow_blank=True)
    xcoord = serializers.FloatField()
    ycoord = serializers.FloatField()
    
    # allow_blank
    
    def create(self, validated_data):
        name = validated_data["name"]
        address = validated_data["address"]
        xcoord = validated_data["xcoord"]
        ycoord = validated_data["ycoord"]

        return Location.objects.get_or_create(name=name,address=address,xcoord=xcoord,ycoord=ycoord)[0]
        
class VisitedLocationSerializer(serializers.Serializer):
    location = LocationSerializer()
    dateFrom = serializers.DateField()
    dateTo = serializers.DateField()
    category = serializers.CharField(max_length=20)
    caseID = serializers.IntegerField()

    def validate_caseID(self, value):
        return value

    def create(self, validated_data):
        dateFrom = validated_data['dateFrom']
        dateTo = validated_data['dateTo']
        category = validated_data['category']
        location_serializer = self.fields['location']
        location = location_serializer.create(validated_data['location'])
        caseID = validated_data['caseID']
        case_record = CaseRecord.objects.get(id=caseID)
        
        visited_location = VisitedLocation.objects.create(dateFrom=dateFrom,dateTo=dateTo,category=category,location=location,caseRecord=case_record)

        return visited_location

class LocationStandSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    address = serializers.CharField(max_length=500, allow_blank=True)
    xcoord = serializers.FloatField()
    ycoord = serializers.FloatField()

    def create(self, validated_data):
        return validated_data

class VisitedLocationStandardSerializer(serializers.Serializer):
    location = LocationStandSerializer()
    dateFrom = serializers.DateField()
    dateTo = serializers.DateField()
    category = serializers.CharField(max_length=20)
    caseRecord = ViewCaseSerializer()

    def create(self, validated_data):
        return validated_data