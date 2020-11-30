from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from django.views.generic import TemplateView
from rest_framework.response import Response
from .clustering import *
from django.contrib.auth.mixins import LoginRequiredMixin
import json

# Create your views here.
class ClusterAPIView(APIView):
    def get(self, request, *args, **kwargs):
        print(request.query_params)
        param = request.query_params
        D = int(param['d'] or 200)
        T = int(param['t'] or 3)
        C = int(param['c'] or 2)
        clusteringResult = performCluster(D, T, C)
        return Response(json.dumps(clusteringResult), status=status.HTTP_200_OK)

class ClusterView(LoginRequiredMixin, TemplateView, APIView):
    login_url = 'login'
    template_name = "view_cluster.html"

    