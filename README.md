Amazon Web Scraping with Selenium and Django
This Python script allows you to scrape product information from Amazon product pages using Selenium. The scraped data is then saved to Django’s basic SQLite database.
Prerequisites
Before running the script, make sure you have the following installed:
•	Python (version 3.x)
•	Chrome WebDriver (ensure it matches your Chrome browser version)
You'll also need to install the required Python packages listed in the requirements.txt file.
Installation
1.	Clone this repository to your local machine:
git clone https://github.com/ParanoyaFobios/test_task
Install the required Python packages:
pip install -r requirements.txt
First start
1.	Make sure you are in the directory with the manage.py file.
2.	Prepare the database and superuser with the following commands:
	- python manage.py makemigrations
	- python manage.py migrate
	- python manage.py createsuperuser
3.	Finally start the server with the command
  -	python manage.py runserver
The application will be available at http://127.0.0.1:8000/ in your browser.
Caution: HTML selectors could be change, be ready to change it in core\management\commands\scrape_amazon.py file
