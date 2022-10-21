import json
from .models import bitcoin as bitmodel
from .serializers import *
from rest_framework import *
from rest_framework.response import Response
from django.http.response import JsonResponse
from rest_framework.views import APIView
import datetime
from bitcoin.pagination import APIPagination
import urllib.request
import json
import time
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.conf import settings
from datetime import datetime, timedelta
from rest_framework import generics
from django.core.mail import send_mail
from django.conf import settings
import schedule
#bit coin price get api and to send mail if it breaches the price given
def bitcoin_price_tracker():
    r = urllib.request.urlopen('https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd&include_24hr_change=true&include_last_updated_at=true&precision=0')
    price = r.read()
    decoded_price = json.loads(price)
    data = {
        'price':int(decoded_price["bitcoin"]["usd"]),
        'name':[key for key in decoded_price][0],
        'coin':"btc",
        'timestamp':datetime.now()
    }
    serializer = BitcoinSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
    minmaxval = minmax.objects.last()
    print(decoded_price["bitcoin"]["usd"])
    if decoded_price["bitcoin"]["usd"] < minmaxval.minimum :
        send_mail(
        'This Mail is about your Bitcoin tracker',
        'Bitcoin is breached the minimum value of '+ str(minmaxval.minimum),
        'chirag.m2santhe@gmail.com',
        ['chiragmurthy123@gmail.com'],
    fail_silently=False)
    if decoded_price["bitcoin"]["usd"] > minmaxval.maximum :
        send_mail(
        'This Mail is about your Bitcoin tracker',
        'Bitcoin is breached the maximum value of '+ str(minmaxval.maximum),
        'chirag.m2santhe@gmail.com',
        ['chiragmurthy123@gmail.com'],
    fail_silently=False)
    return JsonResponse({'msg':data})

#api for pagination and output
class BitcoinDetails(APIView,APIPagination):
    serializer_class = BitcoinSerializer
    def get(self, request):
        startdate = self.request.query_params.get('date', None)
        from_date = datetime.strptime(startdate, '%d-%m-%Y') +  timedelta(hours= 00, minutes = 00, seconds = 00, milliseconds= 000)
        to_date = datetime.strptime(startdate, '%d-%m-%Y').replace(hour=23, minute=59, second=59, microsecond=0)
        queryset = bitmodel.objects.all().filter(created_at__gte=from_date,created_at__lte=to_date).values()
        result = self.paginate_queryset(queryset, request,view=self)
        serializer = BitcoinSerializer1(result, many=True, context={'request':request})
        response = self.get_paginated_response(serializer.data)
        return response  

#api for adding minimum and maximum value
class MinMaxAdd(generics.GenericAPIView):
    serializer_class = MinMaxSerializer
    def post(self,request):
        serializer = MinMaxSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'Data Saved Succesfully'})
        return Response({"Failed to add the data"})

#api to get the latest price of bitcoin (for any extra purpose)
def min_max(request):
    if request.method == 'GET':
        bit_price = bitmodel.objects.last()
        print((bit_price.price,"bitcoinnn"))
        return JsonResponse({'user':bit_price.price})
    return Response({'status':"failed"})





schedule.every(5).seconds.do(bitcoin_price_tracker)
while True:
    schedule.run_pending()
    time.sleep(1)