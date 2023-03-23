import sqlite3
import requests
from bs4 import BeautifulSoup
import time
import tkinter as tk
import threading
import customtkinter
from email.message import EmailMessage
import ssl
import smtplib
import os
from dotenv import load_dotenv

load_dotenv()


stop_flag = False  # flag to signal the thread to stop
mycolor = "#242424"


def track_price():
    global selected_website, stop_flag
    website = selected_website.get()
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
    }

    with sqlite3.connect("trckerS.db") as con:
        cur = con.cursor()
        cur.execute(
            """CREATE TABLE IF NOT EXISTS trackers
                        (price real)"""
        )

        old_price = None

        # loop that allows the program to regularly check for prices
        while not stop_flag:
            try:
                response = requests.get(website, headers=headers)

                soup = BeautifulSoup(response.content, "html.parser")

                # Extract title and price based on the selected website
                if website == "http://127.0.0.1:5500/dist/index.html":
                    title = soup.find("h3", class_="product-title").get_text()
                    price = (
                        soup.find("h4", class_="product-price")
                        .get_text()
                        .replace(",", "")
                        .replace("$", "")
                        .strip()
                    )
                elif website == "https://www.trendshome.es":
                    title = soup.find("h1").get_text()
                    price = (
                        soup.find("span", class_="amount")
                        .get_text()
                        .replace(",", "")
                        .replace("€", "")
                        .strip()
                    )
                else:
                    # If the selected website is not recognized, raise an error
                    raise ValueError("Selected website not recognized")

                converted_price = float(price)

                if old_price is None:
                    old_price = converted_price

                if converted_price < old_price:
                    print("Price Dropped!", converted_price)
                    cur.execute("INSERT INTO trackers VALUES (?)", (converted_price,))
                    for row in cur.execute("""SELECT * FROM trackers"""):
                        print(row)
                        print(converted_price)
                    user_email_text = user_email.get()
                    if len(user_email_text.strip()) != 0:
                        send_email(old_price, converted_price, title, user_email_text)
                    old_price = converted_price


                elif converted_price > old_price:
                    cur.execute("INSERT INTO trackers VALUES (?)", (converted_price,))
                    old_price = converted_price
                    print("Price Increased!", converted_price)
                    for row in cur.execute("""SELECT * FROM trackers"""):
                        print(row)

                # update the text widget with the contents of the database

                textbox.delete("1.0", "end")
                for row in cur.execute("""SELECT * FROM trackers"""):
                    rowss = str(row).replace(",", "")
                    textbox.insert("end", str(rowss) + "$" + "\n")

            except Exception as e:
                print("An error occurred:", e)

            # wait for 1 second before checking again
            time.sleep(1)


def send_email(old_proce, price, product_name, email):
    email_sender = os.getenv("email_sender")

    email_password = os.getenv("email_password")

    email_receiver = email

    subject = "Price just droped!"
    body = (
        """The price of the product you're tracking just droped to """
        + str(price)
        + "$ \n -original price was: "+str(old_proce)+"$ \n -product name: "+product_name
        + "\n \n for more inforamtion, please visit our repo.: https://github.com/WesamAbadi/Product-price-tracker"
    )

    em = EmailMessage()
    em["From"] = email_sender
    em["To"] = email_receiver
    em["subject"] = subject
    em.set_content(body)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_receiver, em.as_string())


def start_tracking():
    global thread
    thread = threading.Thread(target=track_price)
    thread.start()
    track_button.configure(state=tk.DISABLED)
    user_email.configure(state=tk.DISABLED)
    combobox.configure(state=tk.DISABLED)


def stop_tracking():
    global thread, stop_flag
    stop_flag = True
    thread.join()
    track_button.configure(state=tk.NORMAL)
    combobox.configure(state=tk.NORMAL)


# create a tkinter window


window = customtkinter.CTk()
window.geometry("600x500")
window.title("Product Price tracker")

# create a list of websites to track
websites = ["http://127.0.0.1:5500/dist/index.html", "https://www.trendshome.es"]

# create a variable to hold the selected website
selected_website = tk.StringVar(window)
selected_website.set(websites[0])

# create the dropdown menu for website selection

website_label = tk.Label(
    window, text="Select a Website to track from:", background=mycolor, fg="white"
)
website_label.pack()

combobox = customtkinter.CTkOptionMenu(master=window, values=websites)
combobox.pack(padx=20, pady=10)
# create a button to start tracking the price
track_button = customtkinter.CTkButton(
    master=window, text="Start tracking", command=start_tracking
)
track_button.pack(padx=20, pady=10)


# create a button to stop tracking the price
stop_button = customtkinter.CTkButton(
    master=window, text="Stop tracking", command=stop_tracking
)
stop_button.pack(padx=20, pady=10)


user_email = customtkinter.CTkEntry(
    master=window, placeholder_text="Your email address", width=220
)
user_email.pack(padx=20, pady=10)

# create a text widget to display the contents of the database


textbox = customtkinter.CTkTextbox(window)
textbox.configure(width=500, height=300)

textbox.pack()


def on_closing():
    try:
        stop_tracking()
    except:
        print("the thread isn't on.")

    print("oye, why quitting?")
    window.destroy()


window.protocol("WM_DELETE_WINDOW", on_closing)

window.mainloop()
