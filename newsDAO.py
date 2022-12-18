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

    def create_source(self, values):     
       cursor = self.get_cursor()
       sql="insert into newssource (source, keyword) values (%s,%s)"
       cursor.execute(sql, values)
       self.connection.commit()
       newid = cursor.lastrowid
       self.close_all()
       return newid

    def create_article(self, values):     
       cursor = self.get_cursor()
       sql="insert into newsarticles (title, author, description, date_published, url, source) values (%s,%s,%s,%s,%s,%s)"
       cursor.execute(sql, values)
       self.connection.commit()
       newid = cursor.lastrowid
       self.close_all()
       return newid

    def get_all_source(self):
        cursor = self.get_cursor()
        sql="select * from newssource"
        cursor.execute(sql)
        results = cursor.fetchall()
        return_array = []
        #print(results)
        for result in results:
            #print(result)
            return_array.append(self.convert_to_dictionary_source(result))     
        self.close_all()
        return return_array

    def get_all_articles(self):
        cursor = self.get_cursor()
        sql="select * from newsarticles"
        cursor.execute(sql)
        results = cursor.fetchall()
        return_array = []
        print(results)
        for result in results:
            #print(result)
            return_array.append(self.convert_to_dictionary_article(result))     
        self.close_all()
        return return_array

    def get_id_source(self, id):
        cursor = self.get_cursor()
        sql="select * from newssource where id = %s"
        values = (id,)
        cursor.execute(sql, values)
        result = cursor.fetchone()
        return_value = self.convert_to_dictionary_source(result)
        self.close_all()
        return return_value

    def convert_to_dictionary_source(self, result):
        colnames=['id','source', "keyword"]
        item = {}   
        if result:
            for i, col_name in enumerate(colnames):
                value = result[i]
                item[col_name] = value       
        return item

    def convert_to_dictionary_article(self, result):
        colnames=['id','title', "author", "description", "date_published", "url", "source"]
        item = {}   
        if result:
            for i, col_name in enumerate(colnames):
                value = result[i]
                item[col_name] = value       
        return item

    def update_source(self, values):
        cursor = self.get_cursor()
        sql="update newssource set source= %s, keyword=%s  where id = %s"
        cursor.execute(sql, values)
        self.connection.commit()
        self.close_all()

    def delete_source(self, id):
        cursor = self.get_cursor()
        sql="delete from newssource where id = %s"
        values = (id,)
        cursor.execute(sql, values)
        self.db.commit()
        self.close_all()
        print("Entry deleted")

    # Create a database that stores user input information such as the name of the source, url, and keyword
    def create_source_table(self):
        cursor = self.get_cursor()
        sql = """
            CREATE TABLE newssource (
            id INT PRIMARY KEY AUTO_INCREMENT,
            source VARCHAR(255),
            keyword VARCHAR(255))
            """
        cursor.execute(sql)
        self.connection.commit()
        self.close_all()
    
    # Database to store the results returned based on the information provided by the user in the source table
    def create_article_table(self):
        cursor = self.get_cursor()
        sql = """
            CREATE TABLE newsarticles (
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

    def create_database(self):
        self.connection = mysql.connector.connect(
            host=       self.host,
            user=       self.user,
            password=   self.password   
        )
        self.cursor = self.connection.cursor()
        sql = "create database " + self.database
        self.cursor.execute(sql)
        self.connection.commit()
        self.close_all()

newsDAO = NewsDAO()

if __name__ == "__main__":
    #newsDAO.create_database()
    # newsDAO.create_source_table()
    # newsDAO.create_article_table()

    print("testing")
