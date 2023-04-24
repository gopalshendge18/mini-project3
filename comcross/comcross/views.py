
from rest_framework import status, viewsets
import requests
from rest_framework.response import Response
from django.shortcuts import render,redirect

from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout  # add this
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm  # add this
from django.contrib.auth.forms import AuthenticationForm
import requests
import time
from bs4 import BeautifulSoup
import pandas as pd
from django.http import HttpResponse
from django.http import JsonResponse


def greeting(request):
    headers = {
'authority': 'www.amazon.com',
'pragma': 'no-cache',
'cache-control': 'no-cache',
'dnt': '1',
'upgrade-insecure-requests': '1',
'user-agent': 'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36',
'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
'sec-fetch-site': 'none',
'sec-fetch-mode': 'navigate',
'sec-fetch-dest': 'document',
'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
}    


    query = request.GET.get('q', '')
    category = request.GET.get('category', 'all')

    flipkart_url = 'https://www.flipkart.com/search?q={}'.format(query)
    amazon_url = 'https://www.amazon.in/s?k={}'.format(query)

    
    # base_url = 'https://www.flipkart.com/search?q={}'.format(query)


    pd_name_flipkart = []
    price_flipkart = []
    pd_name_amazon = []
    price_amazon = []
    img_flipkart =[]
    img_amazon = []
    url_flipkart = []
    url_amazon = []
        
#flipkart
    for i in range(1, 3):

        req = requests.get(flipkart_url+str(i))
        soup = BeautifulSoup(req.text, 'html')

        # product name
        pdt_name = soup.findAll('div', attrs={'class': '_4rR01T'})
        [pd_name_flipkart.append(i.text) for i in pdt_name]

        img_name = soup.findAll('img', attrs={'class':'_396cs4'})
        [img_flipkart.append(i.get('src')) for i in img_name]

        # img_name = soup.findAll('img', attrs={'class': '_396cs4'})
        # [img.append(i['src']) for i in img_name]

        # price
        p = soup.findAll('div', attrs={'class': '_30jeq3 _1_WHN1'})
        [price_flipkart .append(i.text) for i in p]
        
        #url link 
        url_link = soup.findAll('a', attrs={'class':'_1fQZEK'})
        [url_flipkart.append(i.get('href')) for i in url_link]
   

#amazon

    for i in range(1, 3):

        req = requests.get(amazon_url+str(i))
        soup = BeautifulSoup(req.text, 'html')

        # product name
        pdt_name = soup.findAll('span', attrs={'class': 'a-size-medium a-color-base a-text-normal'})
        [pd_name_amazon.append(i.text) for i in pdt_name]

        # price
        p = soup.findAll('span', attrs={'class': 'a-price-whole'})
        [price_amazon.append(i.text) for i in p]
        
        # img_name = soup.findAll('img', attrs={'class': '_396cs4'})
        # [img.append(i['src']) for i in img_name]

        # price
        
        img_name = soup.findAll('img', attrs={'class':'s-image'})
        [img_amazon.append(i.get('src')) for i in img_name]
        
        url_link = soup.findAll('a', attrs={'class':'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'})
        [url_amazon.append(i.get('href')) for i in url_link]
        

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
    if len(url_amazon) > len(price_amazon):
    # Add dummy values to price_amazon
         num_dummy_values = len(url_amazon) - len(price_amazon)
         dummy_values = [0] * num_dummy_values
         price_amazon.extend(dummy_values)
    elif len(price_amazon) > len(url_amazon):
    # Add dummy values to url_amazon
           num_dummy_values = len(price_amazon) - len(url_amazon)
           dummy_values = [''] * num_dummy_values
           url_amazon.extend(dummy_values)

    
    print("url of amazon",len(url_amazon))
    print(len(price_amazon)) 
    
    amazon_data = pd.DataFrame({'Product': pd_name_amazon,
                                'Price': price_amazon,
                                'url' : url_amazon
                            
                                })
    flipkart_data = pd.DataFrame({'Product': pd_name_flipkart,
                                  'Price': price_flipkart,
                                   'url' : url_flipkart
                                  })
    print(len(amazon_data))
    print(len(flipkart_data))
    # snapdeal_data = pd.DataFrame({'Product': snapdeal_pd_name,
    #                               'Price': snapdeal_price})
    amazon_data['Website'] = 'Amazon'
    print(type(amazon_data))
    flipkart_data['Website'] = 'Flipkart'
    # snapdeal_data['Website'] = 'Snapdeal'
    data = pd.concat([ amazon_data,flipkart_data])
    
    # data = pd.DataFrame({'Product': pd_name,
    #                      'Price': price
    #                     #  'Ratings': ratings,
    #                     #  'Warranty': warranty,
    #                     #  'No of Ratings': ratingsno,
    #                     #  'No of Reviews': reviewsno,
    #                     #  'Features': features 
    #                     })
    #json_data = data.to_json(orient='records')
    from tabulate import tabulate

    print(tabulate(data, headers='keys', tablefmt='psql'))


       


    return render(request,'index.html',{'data':data})


    

def home(request):

    return render(request,'home.html')
  



def amazon(request):

    headers = {
'authority': 'www.amazon.com',
'pragma': 'no-cache',
'cache-control': 'no-cache',
'dnt': '1',
'upgrade-insecure-requests': '1',
'user-agent': 'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36',
'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
'sec-fetch-site': 'none',
'sec-fetch-mode': 'navigate',
'sec-fetch-dest': 'document',
'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
}

    amazon_url = 'https://www.amazon.in/s?k=mobile'
    pdamz_name = []
    price = []
    
    
    
    req = requests.get(base_url,headers=headers)
    soup = BeautifulSoup(req.text, 'html')

        # product name
    pdt_name = soup.findAll('span', attrs={'class': 'a-size-medium a-color-base a-text-normal'})
    [pd_name.append(i.text) for i in pdt_name]

        # price
    p = soup.findAll('span', attrs={'class': 'a-price-whole'})
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
    

    

    return HttpResponse(json_data, content_type='application/json')

def home(request):

    return render(request,'home.html')

def redirect_to_flipkart(request, url):
    return redirect('https://www.flipkart.com' + url)


def redirect_to_amazon(request, url):
    return redirect('https://www.amazon.in' + url)