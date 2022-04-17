import sqlite3

conn = sqlite3.connect("F_images.sqlite")

cursor = conn.cursor()
sql_query = """ CREATE TABLE image (
    id integer PRIMARY KEY,
    fileName varchar(255) NOT NULL,
    prediction text NOT NULL
)
"""

select_query = """ Select * from image"""
#cursor.execute(sql_query)
print(cursor.execute(select_query).fetchone())
