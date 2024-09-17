# web scraping python
GUI Web Scraping Project in Python

Overview

This is a Graphical User Interface (GUI) project developed in Python using the Tkinter library. The purpose of this project is to perform web scraping on the website [Books to Scrape](http://books.toscrape.com), extracting data such as book titles, prices, and ratings, and presenting the scraped data in a user-friendly interface.

The project was developed during my time in college in the US, combining skills in Python, web scraping, and GUI development.

Features

	•	GUI Interface: Easy-to-use interface built with Tkinter, allowing users to interact with the scraping results visually.
	•	Web Scraping: Automatically scrapes book data (title, price, and rating) from the website Books to Scrape.
	•	Category Selection: Users can select one or more book categories to scrape.
	•	Sorting Options: Sort the scraped books by price (ascending or descending), title (A-Z or Z-A), and rating (low to high or high to low).
	•	Favorites: Allows users to select books and add them to a favorites list, with the ability to view and remove favorites.
	•	Export to Excel: The scraped data can be exported to an Excel file.
	•	Error Handling: Includes error messages for cases such as no categories selected or no books selected when adding to favorites.

How It Works

	1.	Category Selection: The GUI allows you to select one or more categories from the list (e.g., “Science Fiction”, “Romance”). Once selected, click the Scrape Selected Categories button to fetch book data from the chosen categories.
	2.	Sorting: After scraping, you can sort the book list using different criteria (price, title, or rating) using the dropdown menu.
	3.	Favorites: You can select books from the list and add them to your favorites. Favorites can be viewed, removed, or exported to Excel.
	4.	Export: The scraped data, including book title, price, and rating, can be exported to an Excel file for further use.

Obs: After running the code, you can press the button 'help' and see the instructions clearly and how it works.

Technologies Used

	•	Python: The core programming language used for the project.
	•	Tkinter: For building the GUI interface.
	•	Requests: To handle HTTP requests and fetch webpage data.
	•	BeautifulSoup: For parsing and scraping HTML content.
	•	Pandas: To handle data manipulation and export the data to an Excel file.

Contact

For any questions or feedback, feel free to contact me at [davilna889@gmail.com](mailto:davilna889@gmail.com).