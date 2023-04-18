
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
from django.contrib.auth import login, authenticate, logout  # add this
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm  # add this
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
    base_url = 'https://www.flipkart.com/search?q=smartphones'
    base_url = ''
    pd_name = []
    price = []
    
    
    for i in range(1, 3):
        time.sleep(3)
        req = requests.get(base_url+str(i))
        soup = BeautifulSoup(req.text, 'html')

        # product name
        pdt_name = soup.findAll('div', attrs={'class': '_4rR01T'})
        [pd_name.append(i.text) for i in pdt_name]

        # price
        p = soup.findAll('div', attrs={'class': '_30jeq3 _1_WHN1'})
        [price.append(i.text) for i in p]

        # ratings
        # r = soup.findAll('div', attrs={'class': 'gUuXy-'})
        # [ratings.append(i.span.div.text) for i in r]

        # # warranty
        # wl = soup.findAll('ul', attrs={'class': '_1xgFaf'})
        # w = [i.findAll('li')[-1] for i in wl]
        # [warranty.append(i.text) for i in w]

        # # number of ratings and reviews
        # a = soup.findAll('span', attrs={'class': '_2_R_DZ'})
        # for i in a:
        #     a = i.text.split('&')
        #     ratingsno.append(a[0].split(" ")[0])
        #     reviewsno.append(a[1].split(" ")[0])

        # # features
        # prop = soup.findAll('ul', attrs={'class': '_1xgFaf'})
        # for i in prop:
        #     a = i.findAll('li')[0:-2]
        #     b = [i.text for i in a]
        #     features.append(','.join(b))

    print('pd_name = ', len(pd_name))
    print('price = ', len(price))
    # print('ratings = ', len(ratings))
    # print('warranty = ', len(warranty))
    # print('ratingsno =', len(ratingsno))
    # print('reviewsno = ', len(reviewsno))
    # print('features = ', len(features))
    
    data = pd.DataFrame({'Product': pd_name,
                         'Price': price
                        #  'Ratings': ratings,
                        #  'Warranty': warranty,
                        #  'No of Ratings': ratingsno,
                        #  'No of Reviews': reviewsno,
                        #  'Features': features 
                        })
    json_data = data.to_json(orient='records')
    na = data.iloc[0]

    print(na['Product'])

    return HttpResponse(json_data, content_type='application/json')

