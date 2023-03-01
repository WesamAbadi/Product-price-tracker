import customtkinter


app = customtkinter.CTk()
app.geometry("600x500")
app.title("CTk example")


# create a list of websites to track
websites = ["http://127.0.0.1:5500/dist/index.html",
            "https://www.trendshome.es"]

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

button = customtkinter.CTkButton(
    master=app, text="CTkButton", command=start_tracking)
button.pack(padx=20, pady=10)
button = customtkinter.CTkButton(
    master=app, text="CTkButton", command=stop_tracking)
button.pack(padx=20, pady=10)

# create a button to stop tracking the price
stop_button = tk.Button(window, text="Stop Tracking", command=stop_tracking)
stop_button.pack()

# create a text widget to display the contents of the database
price_list = tk.Text(window)
price_list.pack()


app.mainloop()
