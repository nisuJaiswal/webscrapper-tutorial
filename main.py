import requests
from bs4 import BeautifulSoup
import pandas as pd

url = 'https://www.flipkart.com/search?q=tops+for+women+wear&sid=clo%2Cash%2Cohw%2C36j&as=on&as-show=on&otracker=AS_QueryStore_OrganicAutoSuggest_1_10_na_na_na&otracker1=AS_QueryStore_OrganicAutoSuggest_1_10_na_na_na&as-pos=1&as-type=RECENT&suggestionId=tops+for+women+wear%7CWomen%27s+Tops&requestId=a64fd899-7a7a-4b48-8345-ca590a611d6e&as-searchtext=Women+Wear&page=' + \
    str(1)
baseUrl = 'https://www.flipkart.com/'

res = requests.get(url)
content = res.content
# print(content)

titles = []
descs = []
images = []
product_urls = []


soup = BeautifulSoup(content, features='html.parser')
for product in soup.findAll('div', attrs={"class": "_1xHGtK"}):
    title = product.find('a', attrs={"class": "IRpwTa"}).text
    tempUrl = product.a['href']
    productUrl = baseUrl + tempUrl
    product_urls.append(productUrl)
    titles.append(title)

print(len(titles), len(product_urls))
