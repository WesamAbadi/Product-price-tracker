# import required files and modules

import requests
from bs4 import BeautifulSoup
import smtplib
import time

# set the headers and user string
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
}
response = requests.get(
    'http://127.0.0.1:5500/dist/index.html', headers=headers)

soup = BeautifulSoup(response.content, 'html.parser')
soup.encode('utf-8')
price = soup.find(class_="product-price").get_text().replace(',','').replace('$', '').replace(' ', '').strip()
converted_price = float(price[0:5])
oldprice = converted_price


# function that sends an email if the prices fell down
""" def send_mail():
  server = smtplib.SMTP('smtp.gmail.com', 587)
  server.ehlo()
  server.starttls()
  server.ehlo()

  server.login('email@gmail.com', 'password')

  subject = 'Price Fell Down'
  body = "Check the prouduct link: http://127.0.0.1:5500/dist"

  msg = f"Subject: {subject}\n\n{body}"
  
  server.sendmail(
    'sender@gmail.com',
    'receiver@gmail.com',
    msg
  )
  #print a message to check if the email has been sent
  print('Hey Email has been sent')
  # quit the server
  server.quit()
 """
# loop that allows the program to regularly check for prices
pricedroped = False
while (not pricedroped):

    response = requests.get(
        'http://127.0.0.1:5500/dist/index.html', headers=headers)

# create the soup object
    soup = BeautifulSoup(response.content, 'html.parser')

# change the encoding to utf-8
    soup.encode('utf-8')
    title = soup.find(class_="product-title").get_text()
    price = soup.find(class_="product-price").get_text().replace(',','').replace('$', '').replace(' ', '').strip()
    # print(price)

    # converting the string amount to float
    converted_price = float(price[0:5])
    # print(converted_price)
    if (converted_price < oldprice):

        print("Price Droped!", converted_price)
        oldprice = converted_price
    elif (converted_price > oldprice):
        oldprice = converted_price
        print("Price Increased!", converted_price)
    time.sleep(1)
