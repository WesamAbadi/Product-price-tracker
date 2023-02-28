import sqlite3
import requests
from bs4 import BeautifulSoup
import time
import tkinter as tk


def track_price():
    global website
    website = website_entry.get()
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
    }

    with sqlite3.connect('trckerS.db') as con:
        cur = con.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS trackers
                        (price real)''')

        old_price = None

        # loop that allows the program to regularly check for prices
        pricedropped = False
        while not pricedropped:
            try:
                response = requests.get(
                    website, headers=headers)
                soup = BeautifulSoup(response.content, 'html.parser')
                title = soup.find(class_="product-title").get_text()
                price = soup.find(class_="product-price").get_text().replace(',',
                                                                             '').replace('$', '').replace(' ', '').strip()
                converted_price = float(price[0:5])

                if old_price is None:
                    old_price = converted_price

                if converted_price < old_price:
                    print("Price Dropped!", converted_price)
                    cur.execute("INSERT INTO trackers VALUES (?)",
                                (converted_price,))
                    for row in cur.execute('''SELECT * FROM trackers'''):
                        print(row)
                    old_price = converted_price
                elif converted_price > old_price:
                    cur.execute("INSERT INTO trackers VALUES (?)",
                                (converted_price,))
                    old_price = converted_price
                    print("Price Increased!", converted_price)
                    for row in cur.execute('''SELECT * FROM trackers'''):
                        print(row)

                # update the text widget with the contents of the database
                price_list.delete("1.0", tk.END)
                for row in cur.execute('''SELECT * FROM trackers'''):
                    price_list.insert(tk.END, str(row) + "\n")

                time.sleep(1)
            except Exception as e:
                print("An error occurred:", e)


# create a tkinter window
window = tk.Tk()
window.title("Price Tracker")

# create a label and an entry field for the website URL
website_label = tk.Label(window, text="Website URL:")
website_label.pack()
website_entry = tk.Entry(window, width=50)
website_entry.pack()

# create a button to start tracking the price
track_button = tk.Button(window, text="Track Price", command=track_price)
track_button.pack()

# create a text widget to display the contents of the database
price_list = tk.Text(window)
price_list.pack()

window.mainloop()
