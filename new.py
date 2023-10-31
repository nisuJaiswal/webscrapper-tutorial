import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL of the website to scrape
url = "https://www.footshop.eu/en/5-mens-shoes/page="

# Lists to store the scraped data
names = []
images = []
descriptions = []
prices = []

for page in range(1, 11):
    print(f"Collecting data fron Page {page}...")
    # Construct the URL for the current page
    page_url = f"https://www.bonjourretail.com/search?page={page}&q=Top&type=product"

    # Send a GET request to the URL
    response = requests.get(page_url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the page content with BeautifulSoup
        soup = BeautifulSoup(response.text, "html.parser")

        # Find product information on the page
        products = soup.find_all("div", attrs={"class": "tt-product"})
        # print(products)

        for product in products:
            # Extract the product name, image, and description
            name = product.find("h2", attrs={"class": "tt-title"}).text.strip()
            # print(name)

            image = product.find("img", attrs={"class": "lazyload"})
            image_url = image["data-mainimage"]
            # print(image_url["data-mainimage"])

            # Operating on URL of image
            position = image_url.find("_respimgsize")
            if position != -1:
                image = (
                    image_url[2:position] + image_url[position + len("_respimgsize") :]
                )

            # print("Modified String:", image)
            prc = product.find("span", attrs={"class": "new-price"}).text
            price = prc[2:]

            names.append(name)
            images.append(image)
            prices.append(price)
    else:
        print(f"Failed to retrieve data from page {page}")

# Create a DataFrame from the scraped data
data = pd.DataFrame({"Name": names, "Image": images, "Price": prices})
print(len(prices))
print(len(names))
print(len(images))
# Save the data to a CSV file
data.to_csv("Data.csv", index=False)

print(f"Scraped {len(names)} products and saved to 'footshop_products.csv'.")
