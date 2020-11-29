from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .clustering import *
import json

# Create your views here.
class ClusterAPIView(APIView):
    def get(self, request, *args, **kwargs):
        print(request.query_params)
        param = request.query_params
        if not 'd' in param or not 't' in param or not 'c' in param:
            return Response("missing parameter", status=status.HTTP_400_BAD_REQUEST)
        D = int(param['d'])
        T = int(param['t'])
        C = int(param['c'])
        clusteringResult = performCluster(D, T, C)
        return Response(json.dumps(clusteringResult), status=status.HTTP_200_OK)