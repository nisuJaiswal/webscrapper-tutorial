import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import time


# Base URL
baseUrl = 'https://www.flipkart.com'
titles = []  # done
description = []
images = []  # done
product_urls = []  # done
productSizes = []  # done
productColors = []  # done

# For Looping and Temporary Purpose
singleProductImg = []
singleProductColor = []
colors = []
sizes = []
singleProductDescription = {}
loopProductUrl = []

# Loop for pages, e.g. range(1,10) means from 1 to 9 pages, data will be scraped

for i in range(1,25):

    url = 'https://www.flipkart.com/search?q=tops+for+women+wear&sid=clo%2Cash%2Cohw%2C36j&as=on&as-show=on&otracker=AS_QueryStore_OrganicAutoSuggest_1_10_na_na_na&otracker1=AS_QueryStore_OrganicAutoSuggest_1_10_na_na_na&as-pos=1&as-type=RECENT&suggestionId=tops+for+women+wear%7CWomen%27s+Tops&requestId=a64fd899-7a7a-4b48-8345-ca590a611d6e&as-searchtext=Women+Wear&page=' + \
        str(i)

    res = requests.get(url)
    # Getting Content of url
    content = res.content
    # print(content)

    # Parsing content into HTMl
    soup = BeautifulSoup(content, features='html.parser')

    # Looping through all the products and colleting title along with the product URL
    for product in soup.findAll('div', attrs={"class": "_1xHGtK"}):
        title = product.find('a', attrs={"class": "IRpwTa"}).text
        tempUrl = product.a['href']
        productUrl = baseUrl + tempUrl
        loopProductUrl.append(productUrl)
        product_urls.append(productUrl)
        titles.append(title)
    time.sleep(1)

    # Looping through the link of all the product URL and collecting Images, Sizes and other stuff
    for link in loopProductUrl:
        # print(link)
        # link = product_urls[0]
        res = requests.get(link)
        cont = res.content

        anotherSoup = BeautifulSoup(cont, features='html.parser')
        ul = anotherSoup.find('ul', attrs={"class": "_3GnUWp"})
        # print(ul)
        if ul:
            for li in ul.findAll('li', attrs={"class": "_20Gt85"}):
                imgSrc = li.find('img')['src']
                imgSrc = imgSrc.replace('/128/128/','/832/832/') # converting the size of the image
                singleProductImg.append(imgSrc)
        # print(singleProductImg)
        else:
            singleProductImg.append([])

        images.append(singleProductImg)
        # print(images)

        colorUl = anotherSoup.findAll('ul', attrs={"class": "_1q8vHb"})
        # print(colorUl[0],colorUl[1])
        # print(len(colorUl))
        # print(type(colorUl))

        # Checking for length because sizes and colors have the same className
        if len(colorUl) == 2:
            # print("inside")
            for li in colorUl[0].findAll('li', attrs={"class": "_3V2wfe"}):
                color = li.find('div', attrs={"class": "_3Oikkn"}).text
                colors.append(color)
            for li in colorUl[1].findAll('li', attrs={"class": "_3V2wfe"}):
                tempSize = li.a.text
                sizes.append(tempSize)
            # productSizes.append(', '.join(sizes))
            # productColors.append(', '.join(colors))

        elif len(colorUl) == 1:
            for li in colorUl[0].findAll('li', attrs={"class": "_3V2wfe"}):
                size = li.a.text
                sizes.append(size)
                # colors.append([])
            productSizes.append(sizes)
            productColors.append([])
        else:
            colors.append('')
            sizes.append('')
            # productSizes.append(sizes)
            # productColors.append(colors)

        # Getting the description
        descriptionDivs = anotherSoup.find_all('div', attrs={"class":"X3BRps"})
        if(descriptionDivs):
            descriptionDivs = descriptionDivs[0].find_all('div', attrs={"class":"row"})  #array of divs with class row
            # print(descriptionDivs)

            if descriptionDivs:
                print(len(descriptionDivs))
                for feature in descriptionDivs:
                    featureTitle = feature.find('div', attrs = {"class":"_2H87wv"}).text
                    featureText = feature.find('div', attrs = {"class":"_2vZqPX"}).text
                    singleProductDescription[featureTitle]=featureText
                    # print([featureTitle,featureText])
                if colors:
                    print(colors)
                    singleProductDescription["Colours"] = ','.join(colors)
                if sizes:
                    singleProductDescription["Sizes"] = ','.join(sizes)
            else:
                singleProductDescription = {}
        else:
            singleProductDescription = {}


        # print(singleProductDescription)
        description.append(singleProductDescription)


        # Clearing all the temporary purpose Lists, got my 2 hours to solve this :(
        singleProductImg = []
        singleProductColor = []
        colors = []
        sizes = []
        singleProductDescription = {}

    loopProductUrl = []
    print("Page no.", i, "Scrapped")


# Printing Lengths
# print(len(titles), len(product_urls))
# print(len(productColors))
# print(len(productSizes))
# print(len(images))


# Making DataFrame and Inserting it into the .csv

# df = pd.DataFrame({"Name": titles, "Product_URL": product_urls,
#                   "Colors": productColors, "Size": productSizes, "Image Url": images})

# df.to_csv('Flipkart_2.csv', index=False, encoding='utf-8')

# Getting JSON Data
data_json = []

for i in range(len(titles)):
    data_json.append({
        "title" : titles[i],
        "description":description[i],
        "productUrl" : product_urls[i],
        "images":images[i]
    })

print(len(data_json))

with open("Flipkart_Data_3.json", "w") as outfile:
    json.dump({"Data":data_json}, outfile)
