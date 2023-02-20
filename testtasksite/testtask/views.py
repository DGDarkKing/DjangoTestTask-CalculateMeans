from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views.decorators.http import require_POST
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from .Mean.Facade import Facade
from .Mean.MyMean import MyMean
from .Mean.NumpyMean import NumpyMean


class TestTaskViewSet(ViewSet):

    @action(methods=['post'], detail=False, url_path='numpy')
    def numpy_resolve(self, request):
        facade = Facade(request.data, NumpyMean())
        response = facade.run()
        return Response(response)

    @action(methods=['post'], detail=False, url_path='my')
    def my_resolve(self, request):
        facade = Facade(request.data, MyMean())
        response = facade.run()
        return Response(response)
