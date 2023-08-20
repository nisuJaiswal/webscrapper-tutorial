import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options

options = Options()
options.page_load_strategy = 'normal'
driver = webdriver.Chrome(options=options)

models = []
prices = []
driver.get('https://www.footshop.eu/en/5-mens-shoes')

content = driver.page_source
soup = BeautifulSoup(content, features='html.parser')

for element in soup.findAll('div', attrs={'class': 'Products_product_1JtLQ'}):
    model = element.find('h4', attrs={'class': 'Product_name_1Go7D'})
    price = element.find(
        'div', attrs={'class': 'ProductPrice_price_J4pAM'})
    models.append(model.text)
    if price:
        prices.append(price.strong.text)


print("No Error")

# print("Models:", models)
# print(type(models))
df = pd.DataFrame({"Product Name": models, "Price": prices})
df.to_csv('shoes.csv', index=False, encoding='utf-8')
