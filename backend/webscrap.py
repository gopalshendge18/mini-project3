# from bs4 import BeautifulSoup
# import requests

# url = "https://www.amazon.in/s?k=sandel&ref=nb_sb_noss_2"
# result = requests.get(url)
# print(result.text.encode("utf-8")) 
from bs4 import BeautifulSoup

import requests

url = "https://www.amazon.in/s?k=penut+butter"


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

response = requests.get(f"{url}", headers=headers)

with open("webpg.html","w", encoding="utf-8") as file: # saving html file to disk
    file.write(response.text)

bs = BeautifulSoup(response.text, "html.parser")
tags= bs.find_all(class_ ="s-card-container s-overflow-hidden aok-relative puis-expand-height puis-include-content-margin puis s-latency-cf-section s-card-border")
print("ASsa\n",type(tags))
print(tags[0][0].encode("utf-8")) # displaying html file use bs.prettify() for making the document more readable
