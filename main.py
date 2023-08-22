import requests
from bs4 import BeautifulSoup
import pandas as pd

baseUrl = 'https://www.flipkart.com'
titles = []  # done
descs = []
images = []  # done
product_urls = []  # done
productSizes = []  # done
productColors = []  # done


singleProductImg = []
singleProductColor = []
colors = []
sizes = []
# for i in range(1, 3):
url = 'https://www.flipkart.com/search?q=tops+for+women+wear&sid=clo%2Cash%2Cohw%2C36j&as=on&as-show=on&otracker=AS_QueryStore_OrganicAutoSuggest_1_10_na_na_na&otracker1=AS_QueryStore_OrganicAutoSuggest_1_10_na_na_na&as-pos=1&as-type=RECENT&suggestionId=tops+for+women+wear%7CWomen%27s+Tops&requestId=a64fd899-7a7a-4b48-8345-ca590a611d6e&as-searchtext=Women+Wear&page=' + \
    str(1)

res = requests.get(url)
content = res.content
# print(content)

soup = BeautifulSoup(content, features='html.parser')

for product in soup.findAll('div', attrs={"class": "_1xHGtK"}):
    title = product.find('a', attrs={"class": "IRpwTa"}).text
    tempUrl = product.a['href']
    productUrl = baseUrl + tempUrl
    product_urls.append(productUrl)
    titles.append(title)

for link in product_urls:
    # print(link)
    res = requests.get(link)
    cont = res.content

    anotherSoup = BeautifulSoup(cont, features='html.parser')
    ul = anotherSoup.find('ul', attrs={"class": "_3GnUWp"})
    # print(ul)
    for li in ul.findAll('li', attrs={"class": "_20Gt85"}):
        imgSrc = li.find('img')['src']
        singleProductImg.append(imgSrc)
        # print(singleProductImg)

    images.append(singleProductImg)
    # print(images)

    colorUl = anotherSoup.findAll('ul', attrs={"class": "_1q8vHb"})
    # print(colorUl[0],colorUl[1])
    # print(len(colorUl))
    # print(type(colorUl))
    if len(colorUl) == 2:
        # print("inside")
        for li in colorUl[0].findAll('li', attrs={"class": "_3V2wfe"}):
            color = li.find('div', attrs={"class": "_3Oikkn"}).text
            colors.append(color)
        for li in colorUl[1].findAll('li', attrs={"class": "_3V2wfe"}):
            tempSize = li.a.text
            sizes.append(tempSize)
        productSizes.append(sizes)
        productColors.append(colors)

    elif len(colorUl) == 1:
        for li in colorUl[0].findAll('li', attrs={"class": "_3V2wfe"}):
            size = li.a.text
            sizes.append(size)
            colors.append([])
        productSizes.append(sizes)
        productColors.append(colors)
    else:
        colors.append([])
        sizes.append([])
        productSizes.append(sizes)
        productColors.append(colors)

print(len(titles), len(product_urls))
print(len(productColors))
print(len(productSizes))
print(len(images))


df = pd.DataFrame({"Name": titles, "Product_URL": product_urls,
                  "Colors": productColors, "Size": productSizes, "Image Url": images})
df.to_csv('Flipkart.csv', index=False, encoding='utf-8')
