from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from django.views.generic import TemplateView
from .serializers import CaseRecordSerializer, CreateCaseRecordSerializer, ViewCaseSerializer, VirusSerializer
from .models import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic


# Create your views here.


class CaseRecordAPI(APIView):
    def post(self, request, *args, **kwargs):
        print(request.data)
        serializer = CaseRecordSerializer(data=request.data)
        if serializer.is_valid():
            case = serializer.save()
            return Response(case.id, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreateCaseRecordView(LoginRequiredMixin, TemplateView):
    login_url = '/login/'
    template_name = "create_case_record.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['viruses'] = Virus.objects.all()
        return context


class CreateCaseRecordAPI(APIView):
    def post(self, request, *args, **kwargs):
        print(request.data)
        serializer = CreateCaseRecordSerializer(data=request.data)
        if serializer.is_valid():
            case = serializer.save()
            return Response(case.id, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AllCaseRecord(generic.ListView):
    template_name = "view_all_cases.html"
    context_object_name = 'case_records'

    def get_queryset(self):
        return CaseRecord.objects.all()

    # def post(self, request, *args, **kwargs):
    #     allCase = CaseRecord.objects.all()
    #     serializer = ViewCaseSerializer(allCase,many=True)
    #     # print(serializer.data)
    #     j = JSONRenderer().render(serializer.data)
    #     print(j)
    #     return Response(j, status=status.HTTP_200_OK)
    #     # return Response(serializer.errors,status.HTTP_403_FORBIDDEN)

class AllCaseRecordAPI(APIView):
    def get(self, request, *args, **kwargs):
        allCase = CaseRecord.objects.all()
        serializer = ViewCaseSerializer(allCase,many=True)
        # print(serializer.data)
        j = JSONRenderer().render(serializer.data)
        print(j)
        return Response(j, status=status.HTTP_200_OK)
        # return Response(serializer.errors,status.HTTP_403_FORBIDDEN)


class SearchCaseRecord(APIView):
    def post(self, request, *args, **kwargs):
        print(request.data)
        json = request.data
        filteredCase = None
        if 'caseID' in json:
            filteredCase = CaseRecord.objects.filter(id=json['caseID'])
        elif 'name' in json:
            filteredCase = CaseRecord.objects.filter(
                patient__name__icontains=json['name'])
        elif 'idNumber' in json:
            filteredCase = CaseRecord.objects.filter(
                patient__idNumber=json['idNumber'])
        else:
            return Response("Condition_Not_Exist", status=status.HTTP_400_BAD_REQUEST)
        serializer = ViewCaseSerializer(filteredCase, many=True)
        j = JSONRenderer().render(serializer.data)
        return Response(j, status=status.HTTP_200_OK)


class CreateVirusView(LoginRequiredMixin, TemplateView):
    template_name = "create_virus.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class CreateVirusAPI(APIView):
    def post(self, request, *args, **kwargs):
        print(request.data)
        serializer = VirusSerializer(data=request.data)
        if serializer.is_valid():
            virus = serializer.save()
            return Response(virus.name, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class IndexView(LoginRequiredMixin, TemplateView):
    login_url = '/login/'
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cases']= CaseRecord.objects.all()
        return context


class ViewLocationRecordsView(generic.DetailView):
    model = CaseRecord
    template_name = 'view_location_records_for_a_case.html'
