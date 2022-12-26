"""
An object that interacts with mysql to create and interact with mysql tables for the purpose of 
sending requests to NewsAPI and storing/viewing the returned articles.

Author: Andrew Scott
"""

import mysql.connector
import dbconfig as cfg
class NewsDAO:
    connection = ""
    cursor =     ''
    host =       ''
    user =       ''
    password =   ''
    database =   ''
    
    def __init__(self):
        self.host=       cfg.mysql['host']
        self.user=       cfg.mysql['user']
        self.password=   cfg.mysql['password']
        self.database=   cfg.mysql['database']

    def get_cursor(self): 
        self.connection = mysql.connector.connect(
            host=       self.host,
            user=       self.user,
            password=   self.password,
            database=   self.database,
        )
        self.cursor = self.connection.cursor()
        return self.cursor

    def close_all(self):
        self.connection.close()
        self.cursor.close()

    # Adds a new row of source information to the sources table
    def create_source(self, values):     
        cursor = self.get_cursor()
        sql="insert into newssource (source, keyword) values (%s,%s)"
        cursor.execute(sql, values)
        self.connection.commit()
        newid = cursor.lastrowid
        self.close_all()
        return newid
    
    # Code to add a row with a source and keyword to the table by default whenever the table is created for the first time
    def first_source(self):
        cursor = self.get_cursor()
        values = ("bbc-news", "stretch")
        sql = "SELECT * FROM newssource"
        cursor.execute(sql)
        rows = cursor.fetchall()
        if len(rows) == 0:
            sql="INSERT IGNORE INTO newssource (source, keyword) VALUES (%s, %s)"
            cursor.execute(sql, values)
            self.connection.commit()
            newid = cursor.lastrowid
            self.close_all()
            return newid
        else:
            pass

    # Adds a row that contains article information returned from NewsAPI
    def create_article(self, values):     
        cursor = self.get_cursor()
        sql="insert into newsarticles (title, author, description, date_published, url, source) values (%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql, values)
        self.connection.commit()
        newid = cursor.lastrowid
        self.close_all()
        return newid

    # Return everything from the sources table
    def get_all_source(self):
        cursor = self.get_cursor()
        sql="select * from newssource"
        cursor.execute(sql)
        results = cursor.fetchall()
        return_array = []
        for result in results:
            return_array.append(self.convert_to_dictionary_source(result))     
        self.close_all()
        return return_array

    # Return everything from the article table
    def get_all_articles(self):
        cursor = self.get_cursor()
        sql="select * from newsarticles"
        cursor.execute(sql)
        results = cursor.fetchall()
        return_array = []
        for result in results:
            return_array.append(self.convert_to_dictionary_article(result))     
        self.close_all()
        return return_array

    # Return a row from the source table based on the provided id
    def get_id_source(self, id):
        cursor = self.get_cursor()
        sql="select * from newssource where id = %s"
        values = (id,)
        cursor.execute(sql, values)
        result = cursor.fetchone()
        return_value = self.convert_to_dictionary_source(result)
        self.close_all()
        return return_value

    # Adds each row from the source table to a dictionary
    def convert_to_dictionary_source(self, result):
        colnames=['id','source', "keyword"]
        item = {}   
        if result:
            for i, col_name in enumerate(colnames):
                value = result[i]
                item[col_name] = value       
        return item

    # Adds each row from the article table to a dictionary
    def convert_to_dictionary_article(self, result):
        colnames=['id','title', "author", "description", "date_published", "url", "source"]
        item = {}   
        if result:
            for i, col_name in enumerate(colnames):
                value = result[i]
                item[col_name] = value       
        return item

    # Allows the user to change values in the source table
    def update_source(self, values):
        cursor = self.get_cursor()
        sql="update newssource set source= %s, keyword=%s  where id = %s"
        cursor.execute(sql, values)
        self.connection.commit()
        self.close_all()

    # Allows the user to delete a row from the source table
    def delete_source(self, id):
        cursor = self.get_cursor()
        sql="delete from newssource where id = %s"
        values = (id,)
        cursor.execute(sql, values)
        self.connection.commit()
        self.close_all()
        print("Entry deleted")

    # When a user tries to logs in, check if the entered credentials match the table credentials
    def check_users(self, account_type, password):
        cursor = self.get_cursor()
        sql = 'SELECT * FROM users WHERE account_type = %s AND password = %s'
        values = (account_type, password)
        cursor.execute(sql, values)
        result = cursor.fetchone()
        return result

    # Create a database table that stores user input information such as the name of the source, url, and keyword
    def create_source_table(self):
        cursor = self.get_cursor()
        sql = """
            CREATE TABLE IF NOT EXISTS newssource (
            id INT PRIMARY KEY AUTO_INCREMENT,
            source VARCHAR(255),
            keyword VARCHAR(255))
            """
        cursor.execute(sql)
        self.connection.commit()
        self.close_all()
    
    # Database table to store the results returned based on the information provided by the user in the source table
    def create_article_table(self):
        cursor = self.get_cursor()
        sql = """
            CREATE TABLE IF NOT EXISTS newsarticles (
            id INT PRIMARY KEY AUTO_INCREMENT,
            title VARCHAR(255),
            author VARCHAR(255),
            description VARCHAR(255),
            date_published DATETIME,
            url VARCHAR(255),
            source VARCHAR(255))
            """
        cursor.execute(sql)
        self.connection.commit()
        self.close_all()

    # Database table to store two user accounts, admin and restricted
    def create_users_table(self):
        cursor = self.get_cursor()
        sql = """
            CREATE TABLE IF NOT EXISTS users (
            id INT PRIMARY KEY AUTO_INCREMENT,
            account_type VARCHAR(255),
            password VARCHAR(255))
            """
        cursor.execute(sql)
        self.connection.commit()
        self.close_all()
    
    # Add two users to the users table
    def add_users(self):
        cursor = self.get_cursor()
        values1 = ("admin", "abc")
        values2 = ("restricted", "xyz")
        sql = "SELECT * FROM users"
        cursor.execute(sql)
        rows = cursor.fetchall()
        if len(rows) == 0:
            sql="INSERT IGNORE INTO users (account_type, password) VALUES (%s, %s)"
            cursor.execute(sql, values1)
            self.connection.commit()
            newid = cursor.lastrowid
            cursor.execute(sql, values2)
            self.connection.commit()
            newid2 = cursor.lastrowid
            self.close_all()
            return newid, newid2
        else:
            pass

    # If the database for this project does not exist, this will create it
    def create_database(self):
        self.connection = mysql.connector.connect(
            host=       self.host,
            user=       self.user,
            password=   self.password   
        )
        self.cursor = self.connection.cursor()
        sql = "CREATE database IF NOT EXISTS " + self.database
        self.cursor.execute(sql)
        self.connection.commit()
        self.close_all()

newsDAO = NewsDAO()
