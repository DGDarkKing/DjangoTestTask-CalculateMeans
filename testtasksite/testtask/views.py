from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views.decorators.http import require_POST
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from .BusnesLayer.Facade import Facade
from .BusnesLayer.MyMean import MyMean
from .BusnesLayer.NumpyMean import NumpyMean
from .BusnesLayer.TimeSpanPrices import TimeSpanPrices


class TestTaskViewSet(ViewSet):

    @action(methods=['post'], detail=False, url_path='numpy')
    def numpy_resolve(self, request):
        timespan_prices = TimeSpanPrices(request.data)
        facade = Facade(timespan_prices, NumpyMean())
        response = facade.calculate_means()
        return Response(response)

    @action(methods=['post'], detail=False, url_path='my')
    def my_resolve(self, request):
        timespan_prices = TimeSpanPrices(request.data)
        facade = Facade(timespan_prices, MyMean())
        response = facade.calculate_means()
        return Response(response)
