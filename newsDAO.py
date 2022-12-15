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
       cursor = self.getcursor()
       sql="insert into newssource (name, url, keyword) values (%s,%s,%s)"
       cursor.execute(sql, values)
       self.connection.commit()
       newid = cursor.lastrowid
       self.closeAll()
       return newid

    def get_all_source(self):
        cursor = self.getcursor()
        sql="select * from newssource"
        cursor.execute(sql)
        results = cursor.fetchall()
        returnArray = []
        print(results)
        for result in results:
            print(result)
            returnArray.append(self.convertToDictionary(result))     
        self.closeAll()
        return returnArray

    def update_source(self, values):
        cursor = self.getcursor()
        sql="update newssource set name= %s, url=%s, keyword=%s  where id = %s"
        cursor.execute(sql, values)
        self.connection.commit()
        self.closeAll()

    def delete_source(self, id):
        cursor = self.getcursor()
        sql="delete from newssource where id = %s"
        values = (id,)
        cursor.execute(sql, values)
        self.db.commit()
        self.closeAll()
        print("Entry deleted")

    # Create a database that stores user input information such as the name of the source, url, and keyword
    def create_source_table(self):
        cursor = self.getcursor()
        sql = """
            CREATE TABLE newssource (
            id INT PRIMARY KEY AUTO_INCREMENT,
            name VARCHAR(255),
            url VARCHAR(255),
            keyword VARCHAR(255))
            """
        cursor.execute(sql)
        self.connection.commit()
        self.closeAll()
    
    # Database to store the results returned based on the information provided by the user in the source table
    def create_article_table(self):
        cursor = self.getcursor()
        sql = """
            CREATE TABLE newsarticles (
            id INT PRIMARY KEY AUTO_INCREMENT,
            newssource_id INT, FOREIGN KEY (newssource_id) REFERENCES newssource(id),
            title VARCHAR(255),
            url VARCHAR(255))
            """
        cursor.execute(sql)
        self.connection.commit()
        self.closeAll()

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
        self.closeAll()

newsDAO = NewsDAO()

if __name__ == "__main__":
    #newsDAO.create_database()
    #newsDAO.create_source_table()
    #newsDAO.create_article_table()

    print("testing")
