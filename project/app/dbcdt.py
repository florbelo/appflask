import pymysql

# Database connection settings

host="localhost"
user="root"
password = ""
db= "club_del_trueque"
cursor=pymysql.cursors.DictCursor
    
# Create a database connection
def get_cdt_connection():
    connection = pymysql.connect(host=host,user=user,password=password,database=db, cursorclass=cursor)
    return connection