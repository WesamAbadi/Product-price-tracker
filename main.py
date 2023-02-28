import sqlite3
import sys
import requests
from bs4 import BeautifulSoup
import time
import tkinter as tk
import threading


stop_flag = False  # flag to signal the thread to stop


def track_price():
    global selected_website, stop_flag
    website = selected_website.get()
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
    }

    with sqlite3.connect('trckerS.db') as con:
        cur = con.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS trackers
                        (price real)''')

        old_price = None

        # loop that allows the program to regularly check for prices
        while not stop_flag:
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

            except Exception as e:
                print("An error occurred:", e)

            # wait for 1 second before checking again
            time.sleep(1)


def start_tracking():
    global thread
    thread = threading.Thread(target=track_price)
    thread.start()
    track_button.config(state=tk.DISABLED)
    website_menu.config(state=tk.DISABLED)


def stop_tracking():
    global thread, stop_flag
    stop_flag = True
    thread.join()
    track_button.config(state=tk.NORMAL)
    website_menu.config(state=tk.NORMAL)

# create a tkinter window
window = tk.Tk()
window.title("Price Tracker")

# create a list of websites to track
websites = ["http://127.0.0.1:5500/dist/index.html", "https://www.trendshome.es"]

# create a variable to hold the selected website
selected_website = tk.StringVar(window)
selected_website.set(websites[0])

# create the dropdown menu for website selection
website_label = tk.Label(window, text="Select a Website:")
website_label.pack()
website_menu = tk.OptionMenu(window, selected_website, *websites)
website_menu.pack()

# create a button to start tracking the price
track_button = tk.Button(window, text="Start Tracking", command=start_tracking)
track_button.pack()

# create a button to stop tracking the price
stop_button = tk.Button(window, text="Stop Tracking", command=stop_tracking)
stop_button.pack()

# create a text widget to display the contents of the database
price_list = tk.Text(window)
price_list.pack()

window.mainloop()
