from rest_framework import status, viewsets
import requests
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework import serializers
from django.core.files.storage import FileSystemStorage
from django.core.files.base import ContentFile
from django.shortcuts import render, HttpResponse, redirect
import csv

from django.http import HttpResponse
from django.shortcuts import render

from django.shortcuts import render, redirect

from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
import requests
import time
from bs4 import BeautifulSoup
import pandas as pd

import requests
from bs4 import BeautifulSoup
import time
import pandas as pd
from django.http import HttpResponse
from django.http import JsonResponse


def greeting(request):
    
    query = request.GET.get('q', '')
    category = request.GET.get('category', 'all')
    base_url = 'https://www.flipkart.com/search?q={}'.format(query)
    print(base_url)
    print(category)
    print(query)

    pd_name = []
    price = []
    img   = []
    for i in range(1, 10):

        req = requests.get(base_url+str(i))
        soup = BeautifulSoup(req.text, 'html')

        pdt_name = soup.findAll('div', attrs={'class': '_4rR01T'})
        [pd_name.append(i.text) for i in pdt_name]
        
        img_name = soup.findAll('img', attrs={'class': '_396cs4'})
        [img.append(i['src']) for i in img_name]

        p = soup.findAll('div', attrs={'class': '_30jeq3 _1_WHN1'})
        [price.append(i.text) for i in p]
    
    print('pd_name = ', len(pd_name))
    print('price = ', len(price))

    if len(price)==0:
        for i in range(1, 3):
            req = requests.get(base_url+str(i))
            soup = BeautifulSoup(req.text, 'html')
            print(soup.prettify())
            pdt_name = soup.findAll('a', attrs={'class': 'IRpwTa'})
            [pd_name.append(i.text) for i in pdt_name]

            p = soup.findAll('div', attrs={'class': '_30jeq3'})
            [price.append(i.text) for i in p]
    print('pd_name = ', len(pd_name))
    print('price = ', len(price))
    print('price = ', len(img ))
    data = pd.DataFrame({'Product': pd_name,
                         'Price': price,'img_url': img})
    
    print(data)     

    return render(request,'index.html',{'data':data})
  


def home(request):
    
    return render(request,'home.html')
