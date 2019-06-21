import datetime

from mysql import connector
import conf
from logger import Logger

# Global Variables
SQLITE = 'sqlite'

# Table Names
USERS = 'users'
ADDRESSES = 'addresses'
cnx = None
logging = Logger(__name__)

'''


OLD VERSION , DO NOT USE


'''

def connect_to_db():
    global cnx
    if cnx is None:
        cnx = connector.connect(user=conf.db_user, password=conf.db_password,
                                host=conf.db_hostname,
                                database=conf.db_schema_name)
        return cnx
    if cnx.is_connected():
        return cnx
    cnx = connector.connect(user=conf.db_user, password=conf.db_password,
                            host=conf.db_hostname,
                            database=conf.db_schema_name)
    return cnx


# Create tables
def create_drivers_table():
    q = "CREATE TABLE IF NOT EXISTS drivers (id char(9) PRIMARY KEY, name CHAR(30) , lat float , lng float , " \
        "truck_size INT ); "
    cursor = cnx.cursor()
    try:
        cursor.execute(q)
        cnx.commit()
        logging.info('drivers table created')
    except Exception as e:
        logging.error('failed to create drivers table %s', e)


def create_sensors_table():
    q = "CREATE TABLE IF NOT EXISTS sensors (id char(9) PRIMARY KEY, address char(60), capacity INT(3) , status CHAR " \
        "(45),  lat double , lng double, last_update_date date); "
    cursor = cnx.cursor()
    try:
        cursor.execute(q)
        cnx.commit()
        logging.info('sensors table created')
    except Exception as e:
        logging.error('failed to create sensors table %s', e)


def create_statistics_table():
    q = "CREATE TABLE IF NOT EXISTS statistics (sensor_id char(9) , date DATE, capacity INT); "
    cursor = cnx.cursor()
    try:
        cursor.execute(q)
        cnx.commit()
        logging.info('statistics table created')
    except Exception as e:
        logging.error('failed to create statistics table %s', e)


def create_all_tables():
    connect_to_db()
    try:
        create_statistics_table()
        create_drivers_table()
        create_sensors_table()
        # create_trash_room_table()
        # create_trash_room_to_sensors_table()
        logging.info('all tables are created.')
    except Exception as e:
        logging.critical('one or more of tables are not created, cant start to probram %s', e)


# Insert data to tables


# Delete data from tables

