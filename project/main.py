#GUI Web Scraping Project

import tkinter as tk  # Importing the tkinter library for GUI
from tkinter import ttk, messagebox, filedialog, Menu  # Importing specific modules from tkinter
import webbrowser  # Importing the webbrowser module for opening web pages
import requests  # Importing the requests module for making HTTP requests
from bs4 import BeautifulSoup  # Importing BeautifulSoup for HTML parsing
import pandas as pd  # Importing pandas for data manipulation
import re  # Importing the re module for regular expressions
from urllib.parse import urljoin  # Importing urljoin for URL manipulation

# Function to get the exchange rate from GBP to USD
def get_exchange_rate():
    url = "https://www.x-rates.com/calculator/?from=GBP&to=USD&amount=1"  # URL for exchange rate
    response = requests.get(url)  # Sending GET request to the URL
    soup = BeautifulSoup(response.text, "html.parser")  # Parsing HTML content
    rate = soup.find("span", class_="ccOutputTrail").previous_sibling.strip()  # Extracting exchange rate
    return float(rate)  # Converting exchange rate to float and returning

# Function to fetch book categories from the website
def fetch_categories():
    base_url = "http://books.toscrape.com"  # Base URL of the website
    response = requests.get(base_url)  # Sending GET request to the base URL
    soup = BeautifulSoup(response.text, 'html.parser')  # Parsing HTML content
    categories = soup.find("ul", class_="nav-list").find("li").find("ul").find_all("li")  # Finding category elements
    # Dictionary to map categories to emojis
    category_emojis = {
        "Art": "🎨", "Architecture": "🏛️", "Autobiography": "📖", "Biography": "👤", "Business": "💼",
        "Children's": "👶", "Christian": "✝️", "Classics": "📚", "Comics": "🖼️", "Cookbooks": "🍳",
        "Crime": "🔪", "Fantasy": "🧙‍♂️", "Fiction": "📖", "History": "🏛️", "Horror": "👻",
        "Humor": "😂", "Music": "🎵", "Mystery": "🔍", "Philosophy": "🤔", "Poetry": "📜",
        "Politics": "🏛️", "Psychology": "🧠", "Religion": "🙏", "Romance": "💖", "Science": "🔬",
        "Science Fiction": "🚀", "Self-Help": "🆘", "Sports": "⚽", "Travel": "✈️", "Young Adult": "👦👧"
    }
    # Creating a dictionary of categories with their URLs and emojis
    return {cat.a.get_text().strip() + " " + category_emojis.get(cat.a.get_text().strip(), "📗"): urljoin(base_url, cat.a['href']) for cat in categories}

# Function to fetch books based on selected category URLs
def fetch_books(selected_category_urls):
    books = []  # List to store fetched books
    for category_url in selected_category_urls:  # Iterating through selected category URLs
        response = requests.get(category_url)  # Sending GET request to the category URL
        soup = BeautifulSoup(response.text, "html.parser")  # Parsing HTML content
        for book in soup.find_all("article", class_="product_pod"):  # Finding all book elements
            title = book.h3.a["title"]  # Extracting book title
            price_text = book.find("p", class_="price_color").text  # Extracting book price text
            price = float(re.sub(r'[^\d.]+', '', price_text))  # Extracting and converting book price to float
            rating_text = book.find("p", class_="star-rating")["class"][1]  # Extracting rating text
            rating = rating_text.replace("star-rating", "")  # Removing "star-rating" from rating text
            books.append({"Title": title, "Price ($)": "$" + str(round(price * exchange_rate, 2)), "Rating": rating})  # Adding book to list
    return books  # Returning the list of books

# Function to sort books by price (low to high)
def sort_books_by_price(books, ascending=True):
    return sorted(books, key=lambda x: float(re.sub(r'[^\d.]+', '', x["Price ($)"])), reverse=not ascending)

# Function to sort books by title (alphabetically)
def sort_books_by_title(books, ascending=True):
    return sorted(books, key=lambda x: x["Title"].lower(), reverse=not ascending)

# Function to convert rating text to numeric value
def convert_rating_to_numeric(rating):
    if rating == "One":
        return 1
    elif rating == "Two":
        return 2
    elif rating == "Three":
        return 3
    elif rating == "Four":
        return 4
    elif rating == "Five":
        return 5
    else:
        return 0

# Function to sort books by rating (numeric)
def sort_books_by_rating(books, ascending=True):
    return sorted(books, key=lambda x: convert_rating_to_numeric(x["Rating"]), reverse=not ascending)

# Function to export data to Excel
def export_to_excel():
    filename = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel Files", "*.xlsx")])  # Asking user for filename and location
    if not filename:  # If filename not provided
        return  # Exit function
    data = [(book["Title"], book["Price ($)"], book["Rating"]) for book in books]  # Extracting data from books list
    df = pd.DataFrame(data, columns=["Title", "Price ($)", "Rating"])  # Creating DataFrame from data
    df.to_excel(filename, index=False)  # Exporting DataFrame to Excel file
    messagebox.showinfo("Success", "Data exported to Excel successfully!")  # Showing success message

# Function to show books based on selected categories and sorting option
def show_books():
    selected_indices = category_listbox.curselection()  # Getting selected category indices
    selected_category_names = [category_listbox.get(i) for i in selected_indices]  # Getting selected category names
    selected_category_urls = [categories[name] for name in selected_category_names]  # Getting selected category URLs
    if not selected_category_urls:  # If no categories selected
        messagebox.showinfo("Error", "Please select at least one category")  # Show error message
        return  # Exit function
    book_list.delete(*book_list.get_children())  # Clearing book list
    global books  # Using global variable for books
    books = fetch_books(selected_category_urls)  # Fetching books based on selected categories
    sort_option = sort_option_var.get()  # Getting selected sorting option
    if sort_option == "Price (Low to High)":  # If sorting by price low to high
        books = sort_books_by_price(books, ascending=True)  # Sort books by price low to high
    elif sort_option == "Price (High to Low)":  # If sorting by price high to low
        books = sort_books_by_price(books, ascending=False)  # Sort books by price high to low
    elif sort_option == "Alphabetically (A-Z)":  # If sorting alphabetically A-Z
        books = sort_books_by_title(books, ascending=True)  # Sort books alphabetically A-Z
    elif sort_option == "Alphabetically (Z-A)":  # If sorting alphabetically Z-A
        books = sort_books_by_title(books, ascending=False)  # Sort books alphabetically Z-A
    elif sort_option == "Rating (Low to High)":  # If sorting by rating low to high
        books = sort_books_by_rating(books, ascending=True)  # Sort books by rating low to high
    elif sort_option == "Rating (High to Low)":  # If sorting by rating high to low
        books = sort_books_by_rating(books, ascending=False)  # Sort books by rating high to low
    for book in books:  # Adding sorted books to book list
        book_list.insert("", "end", values=(book["Title"], book["Price ($)"], book["Rating"]))  # Inserting book into list

# Function to open the web page
def open_web_page():
    webbrowser.open_new("http://books.toscrape.com")  # Opening the web page in default web browser

# Function to clear category selection and book list
def clear_selection():
    category_listbox.selection_clear(0, tk.END)  # Clearing category selection
    book_list.delete(*book_list.get_children())  # Clearing book list

# Function to quit the application
def quit_app():
    root.destroy()  # Destroying the main window and quitting the application

# Function to show help information
def show_help():
    messagebox.showinfo("Help", """This is a Book Search Application. Follow these steps to make the most of the app:
	•	Select one or more categories: Choose book categories from the list on the left and click ‘Scrape Selected Categories’ to fetch books from those categories.
	•	Sorting options: You can sort the displayed books by price, title, or rating using the dropdown menu. The options include:
	•	Price: Low to High / High to Low
	•	Title: A-Z / Z-A
	•	Rating: Low to High / High to Low
	•	Selecting books: To select multiple books, hold down Ctrl (or Cmd on Mac) while clicking on the books. You can select as many books as you want this way. Clicking a book without holding Ctrl/Cmd will deselect the others.
	•	Adding books to favorites: Once you’ve selected your desired books, click ‘Add to Favorites’ to move them to your favorites list. You can select multiple books at once and add them all with a single click.
	•	Viewing favorites: Click ‘View Favorites’ to see the books you’ve added to your favorites list. You can also remove books from the list by selecting them and clicking the ‘Remove from Favorites’ button.
	•	Opening the Web Page: You can open the actual bookstore website where the books are being scraped from. To do this, click File and select ‘Open Web Page’.
	•	Clearing selections: To start scraping again or reset your current selections, click File and select ‘Clear Selection’. This will clear the selected categories and book list so you can start fresh.
	•	Exporting: You can export the list of books to an Excel file by selecting the ‘Export to Excel’ option from the File menu.
	•	Exiting the application: To exit the application, click File and select ‘Exit’.""")

# Creating the main window
root = tk.Tk()
root.title("Book Search")  # Setting window title
root.geometry("1000x600")  # Setting window size

canvas = tk.Canvas(root, bg="#e6f7ff")  # Creating canvas
canvas.place(relwidth=1, relheight=1)  # Placing canvas

menu_bar = Menu(root)  # Creating menu bar
root.config(menu=menu_bar)  # Configuring menu bar

file_menu = Menu(menu_bar, tearoff=0)  # Creating file menu
file_menu.add_command(label="Open Web Page", command=open_web_page)  # Adding command to open web page
file_menu.add_command(label="Clear Selection", command=clear_selection)  # Adding command to clear selection
file_menu.add_separator()  # Adding separator
file_menu.add_command(label="Export to Excel", command=export_to_excel)  # Adding command to export to Excel
file_menu.add_separator()  # Adding separator
file_menu.add_command(label="Exit", command=quit_app)  # Adding command to exit
menu_bar.add_cascade(label="File", menu=file_menu)  # Adding file menu to menu bar

help_menu = Menu(menu_bar, tearoff=0)  # Creating help menu
help_menu.add_command(label="Help", command=show_help)  # Adding command to show help
menu_bar.add_cascade(label="Help", menu=help_menu)  # Adding help menu to menu bar

style = ttk.Style(root)  # Creating style object
style.configure("TListbox", font=('Calibri', 11))  # Configuring listbox style
style.configure("Treeview", font=('Calibri', 11))  # Configuring treeview style
style.configure("Treeview.Heading", font=('Calibri', 13, 'bold'))  # Configuring treeview heading style

category_label = ttk.Label(root, text="Select Categories:", font=('Calibri', 13, 'bold'))  # Creating category label
category_label.grid(row=0, column=0, padx=10, pady=(10, 0), sticky='nw')  # Placing category label

category_listbox = tk.Listbox(root, selectmode='multiple', exportselection=False, width=40, height=10, font=('Calibri', 11))  # Creating category listbox
category_listbox.grid(row=1, column=0, padx=10, pady=(0, 10), sticky='nwes')  # Placing category listbox

scrollbar = ttk.Scrollbar(root, orient='vertical', command=category_listbox.yview)  # Creating scrollbar for listbox
scrollbar.grid(row=1, column=0, sticky='nes', pady=(0, 10), padx=(0, 10))  # Placing scrollbar
category_listbox['yscrollcommand'] = scrollbar.set  # Configuring listbox scrollbar

scrape_button = ttk.Button(root, text="Scrape Selected Categories", command=show_books)  # Creating scrape button
scrape_button.grid(row=2, column=0, padx=10, pady=10)  # Placing scrape button

book_label = ttk.Label(root, text="Book List:", font=('Calibri', 13, 'bold'))  # Creating book label
book_label.grid(row=0, column=1, padx=10, pady=(10, 0), sticky='nw')  # Placing book label

# Create the book list Treeview widget
book_list = ttk.Treeview(root, columns=("Title", "Price ($)", "Rating"), show="headings", height=1, selectmode="extended")  

# Configuring column headings
book_list.heading("Title", text="Title", anchor="w")  # Left align title
book_list.heading("Price ($)", text="Price ($)", anchor="center")  # Center align price
book_list.heading("Rating", text="Rating", anchor="center")  # Center align rating

# Configure columns (set width and alignment)
book_list.column("Title", anchor="w", width="300")  # Left align title, set column width
book_list.column("Price ($)", anchor="center", width=100)  # Center align price, set column width
book_list.column("Rating", anchor="center", width=100)  # Center align rating, set column width

# Place the Treeview widget
book_list.grid(row=1, column=1, padx=10, pady=(0, 10), sticky='nwes')

book_list_scrollbar = ttk.Scrollbar(root, orient='vertical', command=book_list.yview)  # Creating scrollbar for book list
book_list_scrollbar.grid(row=1, column=2, sticky='ns', pady=(0, 10))  # Placing scrollbar
book_list['yscrollcommand'] = book_list_scrollbar.set  # Configuring book list scrollbar

# Adding sort option for "Price (Low to High)"
sort_options = ["Price (Low to High)", "Price (High to Low)", "Alphabetically (A-Z)", "Alphabetically (Z-A)", "Rating (Low to High)", "Rating (High to Low)"]
sort_option_var = tk.StringVar(root, sort_options[0])  # Creating variable for sorting option
sort_options.insert(0, "Price (Low to High)")  # Inserting "Price (Low to High)" at the beginning of the list
sort_label = ttk.Label(root, text="Sort By:", font=('Calibri', 13, 'bold'))  # Creating sort label
sort_label.grid(row=2, column=1, padx=10, pady=(10, 0), sticky='w')  # Placing sort label
sort_option_menu = ttk.OptionMenu(root, sort_option_var, *sort_options)  # Creating option menu for sorting options
sort_option_menu.grid(row=2, column=1, padx=(90, 10), pady=(10, 0), sticky='w')  # Placing option menu for sorting options
sort_button = ttk.Button(root, text="Apply Sorting", command=show_books)  # Creating sort button
sort_button.grid(row=2, column=1, padx=(230, 10), pady=(10, 0), sticky='w')  # Placing sort button

# List to store selected items manually
selected_books = set()  # Using a set to avoid duplicates

# Function to toggle selection of a book when clicked
def toggle_book_selection(event):
    item_id = book_list.identify_row(event.y)  # Get the clicked item (row)
    if item_id:  # If a row is clicked
        item_values = book_list.item(item_id, "values")  # Get values of the clicked item
        if item_values in selected_books:
            selected_books.remove(item_values)  # Unselect if already selected
            book_list.selection_remove(item_id)  # Remove selection visually
        else:
            selected_books.add(item_values)  # Select and add to the set
            book_list.selection_add(item_id)  # Visually select the item

# Bind left-click event to the toggle_book_selection function
book_list.bind("<Button-1>", toggle_book_selection)

# Adding Favorites Functionality
favorites = []  # List to store favorites

# Function to add selected books to favorites
def add_to_favorites():
    selected_items = book_list.selection()  # Getting selected items from book list

    if not selected_items: #Check if no book is selected
        messagebox.showinfo("Error", "No book selected.")
        return #Exit the function if no book is selected
    
    added_count = 0  # Counter for added favorites

    for item in selected_items:  # Loop through each selected item
        item_values = book_list.item(item, "values")  # Getting values of selected item

        if item_values not in favorites:  # If item not already in favorites
            favorites.append(item_values)  # Adding item to favorites list
            added_count += 1  # Increment the counter for added books
    
    if added_count > 0:  # If at least one book was added
        messagebox.showinfo("Favorites", f"{added_count} book(s) added to favorites")  # Show confirmation message
    else:  # If no books were added (they were already in favorites)
        messagebox.showinfo("Favorites", "All selected books are already in favorites")  # Inform the user

# Function to view favorites
def view_favorites():
    def remove_from_favorites():
        selected_items = fav_list.selection()  # Getting selected items from favorites list
        removed_count = 0

        for item in selected_items:  # Iterating through selected items
            item_values = fav_list.item(item, "values")  # Getting values of selected item
            if item_values in favorites:
                favorites.remove(item_values)  # Removing item from favorites list
                fav_list.delete(item)  # Deleting item from favorites list
                removed_count += 1  # Increment removed counter

        # Show a single message with the number of removed books
        if removed_count > 0:
            messagebox.showinfo("Favorites", f"{removed_count} book(s) removed from favorites")  # Showing info message
    
    # Function to toggle selection of a book in favorites
    def toggle_favorite_selection(event):
        item_id = fav_list.identify_row(event.y)  # Get the clicked item (row)
        if item_id:  # If a row is clicked
            item_values = fav_list.item(item_id, "values")  # Get values of the clicked item
            if item_values in selected_favorites:
                selected_favorites.remove(item_values)  # Unselect if already selected
                fav_list.selection_remove(item_id)  # Remove selection visually
            else:
                selected_favorites.add(item_values)  # Select and add to the set
                fav_list.selection_add(item_id)  # Visually select the item


    # Creating favorites window
    favorites_window = tk.Toplevel(root)
    favorites_window.title("Favorites")  # Setting window title
    favorites_window.geometry("600x400")  # Setting window size

    # Creating favorites list
    fav_list = ttk.Treeview(favorites_window, columns=("Title", "Price ($)", "Rating"), show="headings") 

    # Configuring column headings and alignment
    fav_list.heading("Title", text="Title", anchor="w")  # Setting column heading for title
    fav_list.heading("Price ($)", text="Price ($)", anchor="center")  # Setting column heading for price
    fav_list.heading("Rating", text="Rating", anchor="center")  # Setting column heading for rating

    # Configuring column width and alignment for the content
    fav_list.column("Title", anchor="w", width=300)
    fav_list.column("Price ($)", anchor="center", width=100)
    fav_list.column("Rating", anchor="center", width=100)

    fav_list.pack(fill='both', expand=True)  # Packing favorites list

    # Add the favorite books to the Treeview
    for fav in favorites:
        fav_list.insert("", "end", values=(fav[0], fav[1], fav[2]))  # Inserting favorite into list

    # Bind left-click event to the toggle_favorite_selection function
    fav_list.bind("<Button-1>", toggle_favorite_selection)

    # Button to remove selected items from favorites
    remove_button = ttk.Button(favorites_window, text="Remove from Favorites", command=remove_from_favorites)  
    remove_button.pack(pady=10)  # Packing remove button

# List to store selected favorites manually
selected_favorites = set()  # Using a set to avoid duplicates

add_favorites_button = ttk.Button(root, text="Add to Favorites", command=add_to_favorites)  # Creating add favorites button
add_favorites_button.grid(row=3, column=0, padx=10, pady=10)  # Placing add favorites button

view_favorites_button = ttk.Button(root, text="View Favorites", command=view_favorites)  # Creating view favorites button
view_favorites_button.grid(row=4, column=0, padx=10, pady=10)  # Placing view favorites button

root.grid_columnconfigure(1, weight=1)  # Configuring column weight
root.grid_rowconfigure(1, weight=1)  # Configuring row weight

exchange_rate = get_exchange_rate()  # Getting exchange rate
categories = fetch_categories()  # Fetching categories
for category in categories.keys():  # Adding categories to category listbox
    category_listbox.insert(tk.END, category)  # Inserting category into listbox

root.mainloop()  # Running the main event loop


'''
In your script, provide the terms of use  at x-rates.com and the information in robots.txt to verify you understand if scraping is allowed on this site.

The terms of use from the website state that we can use anything from this site as long as we don't distribute it 
or transfer copies to others in exchange for money. We are also not allowed to use special software to parse content 
from the site. The robots.txt from the site also allows us to see what we are able to access. The only thing we aren't allowed 
to access was to get authorization of the site, but other than that it gave us the sitemaps that we are able to scrape.


robots.txt (below)
User-agent: *
Disallow: /auth/

# sitemap xml
Sitemap: https://www.x-rates.com/sitemap-table-1.xml
Sitemap: https://www.x-rates.com/sitemap-graph-1.xml
Sitemap: https://www.x-rates.com/sitemap-calculator-1.xml
Sitemap: https://www.x-rates.com/sitemap-monthly-average-1.xml
Sitemap: https://www.x-rates.com/sitemap-historical-1.xml
Sitemap: https://www.x-rates.com/sitemap-general.xml
'''