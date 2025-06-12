import MySQLdb

class DataSaver:
    def __init__(self):
        self.host = 'localhost'
        self.user = 'root'
        self.password = 'zxh'
        self.database = 'crawler'

    def save(self, url, title):
        try:
            db = MySQLdb.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                charset='utf8mb4'
            )
            cursor = db.cursor()
            sql = "INSERT INTO urldata (url, title) VALUES (%s, %s)"
            cursor.execute(sql, (url, title))
            db.commit()
            cursor.close()
            db.close()
            print(f"Saved {url} - {title} to database")
        except MySQLdb.Error as e:
            print(f"Error saving to MySQL: {e}")

    def clear_table(self):
        try:
            db = MySQLdb.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                charset='utf8mb4'
            )
            cursor = db.cursor()
            cursor.execute("DELETE FROM urldata")
            cursor.execute("ALTER TABLE urldata AUTO_INCREMENT = 1")
            db.commit()
            cursor.close()
            db.close()
            print("Table urldata cleared")
        except MySQLdb.Error as e:
            print(f"Error clearing table: {e}")