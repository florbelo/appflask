import pymysql

# Database connection settings

host="localhost"
user="root"
password = ""
db= "contact_us"
cursor=pymysql.cursors.DictCursor
    
# Create a database connection
def get_db_connection():
    connection = pymysql.connect(host=host,user=user,password=password,database=db, cursorclass=cursor)
    return connection