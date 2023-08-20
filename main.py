import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup

options = webdriver.ChromeOptions()
options.page_load_strategy = 'normal'
options.add_argument('--start-maximized')
driver = webdriver.Chrome(options=options)

models = []
prices = []
images = []

driver.get("https://www.footshop.eu/en/5-mens-shoes/page={6}")


def getData():

    total_height = driver.execute_script("return document.body.scrollHeight")

    # Scroll smoothly using JavaScript
    for y in range(0, total_height, 40):  # Adjust the step size as needed
        driver.execute_script(f"window.scrollTo(0, {y});")

    # Scroll to the bottom of the page
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    content = driver.page_source
    soup = BeautifulSoup(content, features='html.parser')

    for element in soup.findAll('div', attrs={'class': 'Products_product_1JtLQ'}):
        model = element.find('h4', attrs={'class': 'Product_name_1Go7D'})
        price = element.find(
            'div', attrs={'class': 'ProductPrice_price_J4pAM'})
        image = element.find('img', attrs={'class': 'LazyImage_image_3wH1D'})

        models.append(model.text)
        if price:
            prices.append(price.strong.text)
        if image:
            img_src = image['src']
            images.append(img_src)

    df = pd.DataFrame(
        {"Product Name": models, "Price": prices, "Image": images})

    df.to_csv('shoes.csv', index=False, encoding='utf-8',
              mode='a', header=False)


getData()

# Create a dataframe and save to CSV
# df = pd.DataFrame({"Product Name": models, "Price": prices, "Image": images})
