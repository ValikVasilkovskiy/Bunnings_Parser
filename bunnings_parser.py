from time import sleep
import os

from selenium import webdriver
from bs4 import BeautifulSoup
from openpyxl import Workbook


dir = os.path.abspath(os.path.dirname(__file__))
url = "https://www.bunnings.com.au/our-range/storage-cleaning/cleaning/bins"
out_file_name = 'bins.xlsx'
out_file_dir = os.path.join(dir, 'data', out_file_name)
wait_time = 5
id_match = []
driver = webdriver.Chrome()
print("Start get bins...")



driver.get(url)
driver.minimize_window()
# sleep for load page source
sleep(wait_time)

# click view all products
link = driver.find_element_by_id("MoreProductsButton")
link.click()
sleep(wait_time)

# click view next
r = 0
while True:
    try:
        print("Click next products... {}".format(r))
        link = driver.find_element_by_class_name("view-more-icon")
        link.click()
        r += 1
        sleep(10)
    except:
        break
sleep(wait_time)

data = driver.page_source
bsObj = BeautifulSoup(data, "html.parser")

# create out file sheet and headers
wb = Workbook()
ws = wb.create_sheet("bins")
ws.append([
    "Product detail",
    "Price",
])

all_cards = bsObj.find_all("article", class_="product-list__item hproduct special-order-product")
n = 0
for card in all_cards:
    print("Iteration --> {}".format(n))
    n += 1

    # get product detail
    product_details = card.find("div", class_="product-list__prodname product-list__title fn").text

    # get product price (with out $)
    price = card.find("div", class_="price-value").text[1:]

    # create line
    data_line = [product_details, price]
    ws.append(data_line)
    wb.save(out_file_dir)

driver.close()
print("Close WebDriver...")
print('Save Data in file {}'.format(out_file_dir))