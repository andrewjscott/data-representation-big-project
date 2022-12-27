# Data Representation Project - NewsAPI

This is an application written in using Python 3.8.8, MySQL, and HTML. The application uses Flask to make calls to NewsAPI in order to retrieve news articles based on the input provided by users. Users input a news source and keyword, and they can then view a summary of the articles returned from [NewsAPI](https://newsapi.org/). 

There are two user accounts for logging in - Admin and Restricted. The Admin account can create, update, delete sources, and view returned articles. The Restricted account can only create sources and view returned articles. 

This repository contains the following folders and files:   
1. static - this folder contains the following files:   
(a) articles.css (Contains CSS code for styling articles.html)   
(b) favicon.ico (Loads a favicon in the tab when a webpage is opened)   
(c) sources.css (Contains CSS for styling all other HTML files)    
2. templates - this folder contains the following files:   
(a) all_articles.html (Webpage to display the data contained in the MySQL table that stores details about the articles returned by NewsAPI)    
(b) articles.html (Webpage to display summaries of the articles returned by NewsAPI based on the source and keyword provided by the user)    
(c) login.html (Webpage that allows the user to login to use the application)    
(d) sources.html (Webpage that shows the MySQL table containing the sources and keyword provided by users and allows them to perform CRUD operations)    
3.  .gitignore - Contains information for which files should not be uploaded when the repository is pushed to github.
4. README.md - Contains and overview about this repository, its files, and how to use it.   
5. application.py - Contains the python code to make Flask calls to NewsAPI based on the values contained in the MySQL tables and the options selected by the user on the interface provided by the HTML webpages.
6. dbconfig_template.py - A template for the user to provide details to connect to MySQL and NewsAPI.    
7. newsDAO.py - Contains the python code to interact with MySQL.   
8. requirements.txt - Contains the python modules used by the application.     

There are two ways to use this application.

## PythonAnywhere
The application is hosted on PythonAnywhere, which is the simpliest way to use it. Visit the website http://andrewjscott.pythonanywhere.com/ and follow the on screen instructions to log in. 

## Clone Repository and run on Local Machine
This repository can also be cloned and run locally. Ensure that Python and MySQL are already installed on your machine. Note that these instructions are for Windows. Some adaptations might be needed for users on Mac or Linux.  

1. Clone this repository by running the following code on your command line: ```git clone https://github.com/andrewjscott/data-representation-big-project.git```   
2. Navigate to the cloned folder and launch a virtual environment by first running the following: ```python -m venv venv``` and press return, and then run: ```.\venv\Scripts\activate.bat```  
3. Rename the file dbconfig_template.py to dbconfig.py and edit the file so that the host is "localhost", user, and password are set to the details of your MySQL, and database is set as project. Enter your NewsAPI key to this file also. If you do not have one, you can get one free from [the NewsAPI website](https://newsapi.org/). Enter any random string for the secret_key variable.
4. Install the required modules by running the following code: ```pip install -r requirements.txt```    
5. Run the application with the following code: ```python application.py```    
6. The command line should tell you what url the server is now running on (e.g Running on http://127.0.0.1:5000/). Open this address using your web browser and follow the onscreen instructions to use the application.