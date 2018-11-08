from mysql import connector
import configuration
import flask

# Global Variables
SQLITE = 'sqlite'

# Table Names
USERS = 'users'
ADDRESSES = 'addresses'
cnx = None

def connect_to_db():
    global cnx
    cnx = connector.connect(user=configuration.db_user, password=configuration.db_password,
                        host=configuration.db_hostname,
                        database=configuration.db_schema_name, port=3306)


def create_drivers_table():
    q = "CREATE TABLE drivers_a (id INT PRIMARY KEY, name CHAR(30) , lat DOUBLE , lng DOUBLE , trcuk_size INT )"
    cursor = cnx.cursor()
    cursor.execute(q)


def create_sensors_table():
    q = "CREATE TABLE sensors_a (id INT PRIMARY KEY, capacity(int), status(CHAR 10)"
    cursor = cnx.cursor()
    cursor.execute(q)

def create_trash_room_table():


def show_all_table():
    q = "SHOW TABLES"
    cursor = cnx.cursor()
    cursor.execute(q)
    #cnx.commit()
    result = cursor.fetchall()
    print (result)

def init_all_tables():
    create_drivers_table()
    create_sensors_table()


#q = 'SELECT * FROM `docs`'
#cursor = cnx.cursor()
#cursor.execute(q)
#result = cursor.fetchall()  # return list of tuples, each node is row.
#emp_no = cursor.lastrowid
#cnx.commit()
#cursor.close()

connect_to_db()
show_all_table()
init_all_tables()

pass
