# import MySQLdb

# class DataSaver:
#     def __init__(self):
#         self.host = 'localhost'
#         self.user = 'root'
#         self.password = 'zxh'
#         self.database = 'crawler'
#         self.db = None  # Initialize db to None
#         self.cursor = None  # Initialize cursor to None
#         try:
#             self.db = MySQLdb.connect(host=self.host,
#                                       user=self.user,
#                                       password=self.password,
#                                       database=self.database,
#                                       charset='utf8mb4')
#             self.cursor = self.db.cursor()
#             self.clear_table()  # Call clear_table during initialization
#         except MySQLdb.Error as e:
#             print(f"Error connecting to MySQL: {e}")

#     def clear_table(self):
#         try:
#             self.cursor.execute("DELETE FROM urldata")  # Replace your_table
#             self.cursor.execute("ALTER TABLE urldata AUTO_INCREMENT = 1")
#             self.db.commit()
#             print("Table urldata cleared")
#         except MySQLdb.Error as e:
#             print(f"Error clearing table: {e}")

#     def save(self, url, title):
#         try:
#             sql = "INSERT INTO urldata (url, title) VALUES (%s, %s)"  # Replace your_table
#             self.cursor.execute(sql, (url, title))
#             self.db.commit()
#             print(f"Saved {url} - {title} to database")
#         except MySQLdb.Error as e:
#             print(f"Error saving to MySQL: {e}")

#     def close(self):
#         if self.db:
#             self.db.close()