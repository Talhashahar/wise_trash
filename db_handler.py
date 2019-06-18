import datetime

from mysql import connector
import configuration
import logging

# Global Variables
SQLITE = 'sqlite'

# Table Names
USERS = 'users'
ADDRESSES = 'addresses'
cnx = None

# logging configuration
#logging.basicConfig(filename='example.log', level=logging.DEBUG)
logging.basicConfig(filename='db_handler.log', format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')



def connect_to_db():
    global cnx
    if cnx is None:
        cnx = connector.connect(user=configuration.db_user, password=configuration.db_password,
                                host=configuration.db_hostname,
                                database=configuration.db_schema_name)
        return cnx
    if cnx.is_connected():
        return cnx
    cnx = connector.connect(user=configuration.db_user, password=configuration.db_password,
                            host=configuration.db_hostname,
                            database=configuration.db_schema_name)
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


def create_trash_room_table():
    q = "CREATE TABLE IF NOT EXISTS trash_room (id char(9) PRIMARY KEY, full_address CHAR(45) , lat DOUBLE , " \
        "lng DOUBLE); "
    cursor = cnx.cursor()
    try:
        cursor.execute(q)
        cnx.commit()
        logging.info('trash_room table created')
    except Exception as e:
        logging.error('failed to create trash_room table %s', e)


def create_trash_room_to_sensors_table():
    q = "CREATE TABLE IF NOT EXISTS trash_room_to_sensors (trash_id char(9) , sensor_id char(9), PRIMARY KEY(" \
        "trash_id,sensor_id), FOREIGN KEY (trash_id) REFERENCES trash_room (id), FOREIGN KEY (sensor_id) REFERENCES " \
        "sensors (id) ON DELETE CASCADE ON UPDATE CASCADE); "
    cursor = cnx.cursor()
    try:
        cursor.execute(q)
        cnx.commit()
        logging.info('trash_room_to_sensors table created')
    except Exception as e:
        logging.error('failed to create trash_room_to_sensors table %s', e)


def create_statistics_table():
    q = "CREATE TABLE IF NOT EXISTS statistics (sensor_id char(9) , date DATE, capacity INT); "
    cursor = cnx.cursor()
    try:
        cursor.execute(q)
        cnx.commit()
        logging.info('statistics table created')
    except Exception as e:
        logging.error('failed to create statistics table %s', e)


def show_all_table():
    q = "SHOW TABLES"
    cursor = cnx.cursor()
    cursor.execute(q)
    result = cursor.fetchall()
    print(result)


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


def delete_all_tables():
    connect_to_db()
    try:
        cursor = cnx.cursor()
        # cursor.execute("drop table trash_room_to_sensors;")
        cursor.execute("drop table drivers;")
        cursor.execute("drop table trash_room;")
        cursor.execute("drop table sensors;")
        logging.info('all tables are deleted')
    except Exception as e:
        logging.error('one or more of tables are not deleted %s', e)


# Insert data to tables

def insert_driver(id, name, lat, lng, truck_size):
    db = connect_to_db()
    cursor = cnx.cursor()
    q = "insert into drivers (id, name, lat,lng, truck_size) VALUES (%s, %s, %s, %s, %s);"
    data = (id, name, float(lat), float(lng), truck_size)
    try:
        cursor.execute(q, data)
        db.commit()
        logging.info('successes insert driver to db')
    except Exception as e:
        logging.error('failed to insert driver to db', e)


def insert_sensor(id, address, capacity, lat, lng, status, update_date):
    db = connect_to_db()
    cursor = cnx.cursor()
    q = "insert into sensors(id, address, capacity, status, lat, lng, last_update_date) VALUES (%s, %s, %s, %s, %s, " \
        "%s, %s); "
    data = (id, address, capacity, status, float(lat), float(lng), update_date)
    try:
        cursor.execute(q, data)
        db.commit()
        logging.info('successes insert sensor to db')
    except Exception as e:
        logging.error('failed to insert sensor to db', e)


def insert_statistics(sensor_id, date, capacity):
    db = connect_to_db()
    cursor = cnx.cursor()
    q = "insert into statistics (sensor_id, date, capacity) VALUES (%s, %s, %s);"
    data = (sensor_id, date, capacity)
    try:
        res1 = cursor.execute(q, data)
        res = db.commit()
        logging.info('successes insert statistics to db')
    except Exception as e:
        logging.error('failed to insert statistics to db', e)


def insert_trash_room(id, full_address, lat, lng):
    db = connect_to_db()
    cursor = cnx.cursor()
    q = "insert into statistics (id, full_address, lat, lng) VALUES (%s, %s, %s, %s);"
    data = (id, full_address, lat, lng)
    try:
        cursor.execute(q, data)
        db.commit()
        logging.info('successes insert trash room to db')
    except Exception as e:
        logging.error('failed to insert trash room to db', e)


# Delete data from tables


def delete_trash_room(room_id):
    q = "delete from trash_room where id=%s;"
    connect_to_db()
    cursor = cnx.cursor()
    try:
        cursor.execute(q, (room_id,))
        cnx.commit()
        return "successes delete trash_room " + room_id
    except Exception as e:
        print("failed to delete trash_room " + e)
        cnx.rollback()
        return "failed to trash_room sensor " + room_id


def delete_sensor(sensor_id):
    q = "delete from sensors where id=%s;"
    connect_to_db()
    cursor = cnx.cursor()
    try:
        cursor.execute(q, (sensor_id,))
        cnx.commit()
        return "successes delete sensor " + sensor_id
    except Exception as e:
        print("failed to delete sensor " + e)
        cnx.rollback()
        return "failed to delete sensor " + sensor_id


def delete_driver(driver_id):
    q = "delete from drivers where id=%s;"
    connect_to_db()
    cursor = cnx.cursor()
    try:
        cursor.execute(q, (driver_id,))
        cnx.commit()
        return "successes delete driver " + driver_id
    except Exception as e:
        print("failed to delete driver " + e)
        cnx.rollback()
        return "failed to delete driver sensor " + driver_id


# Get data from tables
def get_driver_by_id(driver_id):
    q = "select * from drivers where id=%s;"
    connect_to_db()
    cursor = cnx.cursor()
    try:
        cursor.execute(q, (driver_id,))
        res = cursor.fetchall()
        return res
    except Exception as e:
        print("failed to get driver " + e)
        cnx.rollback()
        return None


def get_trash_room(room_id):
    q = "select * from trash_room where id=%s;"
    connect_to_db()
    cursor = cnx.cursor()
    try:
        cursor.execute(q, (room_id,))
        cnx.commit()
        return "successes get trash_room " + room_id
    except Exception as e:
        print("failed to get trash_room " + e)
        cnx.rollback()
        return "failed to get trash_room sensor " + room_id


def get_sensor_by_id(sensor_id):
    q = "select * from sensors where id=%s;"
    connect_to_db()
    cursor = cnx.cursor()
    try:
        cursor.execute(q, (sensor_id,))
        res = cursor.fetchall()
        if not res:
            return None
        return res[0]
    except Exception as e:
        print("failed to get sensor " + e)
        cnx.rollback()
        return None


# update elemnt in db
def update_driver_by_id(id, name, lat, lng, truck_size):
    db = connect_to_db()
    cursor = cnx.cursor()
    q = "UPDATE drivers SET name=%s, lat=%s, lng=%s, truck_size=%s  WHERE id = %s"
    data = (name, float(lat), float(lng), truck_size, id)
    try:
        cursor.execute(q, data)
        db.commit()
        logging.info('successes update driver to db')
    except Exception as e:
        logging.error('failed to update driver to db', e)


def update_treshold(new_threshold):
    current_treshold = get_threshold()
    db = connect_to_db()
    cursor = cnx.cursor()
    q = "UPDATE configuration SET threshold=%s where threshold=%s "
    data = (new_threshold, current_treshold)
    try:
        cursor.execute(q, data)
        db.commit()
        logging.info('successes update driver to db')
    except Exception as e:
        logging.error('failed to update driver to db', e)


def update_sensor_by_id(id, address, capacity, lat, lng, status, update_date):
    db = connect_to_db()
    cursor = cnx.cursor()
    q = "UPDATE sensors SET address=%s, capacity=%s, lat=%s, lng=%s, status=%s, last_update_date=%s WHERE id = %s"
    data = (str(address), int(capacity), float(lat), float(lng), status, update_date, id)
    try:
        cursor.execute(q, data)
        db.commit()
        logging.info('successes update driver to db')
    except Exception as e:
        logging.error('failed to update driver to db', e)


# getter data
def get_sensor_over_x_capacity(capacity):
    db = connect_to_db()
    cursor = cnx.cursor()
    q = "select * from sensors where capacity >=%s"
    try:
        cursor.execute(q, (capacity,))
        res = cursor.fetchall()
        return res
    except Exception as e:
        print("failed to get the trash-bins are full " + e)
        cnx.rollback()
        return None


def get_sensor_between_capacity(min, max):
    db = connect_to_db()
    cursor = cnx.cursor()
    data = (min, max)
    q = "select * from sensors where capacity >=%s AND capacity <=%s "
    try:
        cursor.execute(q, data)
        res = cursor.fetchall()
        return res
    except Exception as e:
        print("failed to get the trash-bins are full " + e)
        cnx.rollback()
        return None


def get_sensor_under_x_battery(battery):
    db = connect_to_db()
    cursor = cnx.cursor()
    q = "select * from sensors where battery <=%s"
    try:
        cursor.execute(q, (battery,))
        res = cursor.fetchall()
        return res
    except Exception as e:
        print("failed to get the trash-bins are full " + e)
        cnx.rollback()
        return None


def get_sensor_under_x_capacity(capacity):
    db = connect_to_db()
    cursor = cnx.cursor()
    q = "select * from sensors where capacity <=%s"
    try:
        cursor.execute(q, (capacity,))
        res = cursor.fetchall()
        return res
    except Exception as e:
        print("failed to get the trash-bins are full " + e)
        cnx.rollback()
        return None


def get_sensors_count_by_status(status):
    db = connect_to_db()
    cursor = cnx.cursor()
    q = "select count(*) from sensors where status =%s"
    try:
        cursor.execute(q, (status,))
        res = cursor.fetchall()
        return res[0][0]
    except Exception as e:
        print("failed to get the trash-bins are full " + e)
        cnx.rollback()
        return None


def get_sensors_by_status(status):
    db = connect_to_db()
    cursor = cnx.cursor()
    q = "select * from sensors where status =%s"
    try:
        cursor.execute(q, (status,))
        res = cursor.fetchall()
        return res
    except Exception as e:
        print("failed to get the trash-bins are full " + e)
        cnx.rollback()
        return None


def get_count_sensors():
    db = connect_to_db()
    cursor = cnx.cursor()
    q = "select count(*) from sensors"
    try:
        cursor.execute(q, )
        res = cursor.fetchall()
        return res[0][0]
    except Exception as e:
        print("failed to get the trash-bins are full " + e)
        cnx.rollback()
        return None


def get_sensors_pickup_today():
    db = connect_to_db()
    cursor = cnx.cursor()
    date = datetime.datetime.now()
    yesterday = date.today() - timedelta(1)
    q = "select count(*) from sensors where date = %s"
    try:
        cursor.execute(q, (date,))
        res = cursor.fetchall()
        return res
    except Exception as e:
        print("failed to get the trash-bins are full " + e)
        cnx.rollback()
        return None


def get_last_update_sensors(id):
    db = connect_to_db()
    cursor = cnx.cursor()
    q = "SELECT * FROM statistics where sensor_id = %s order by date desc limit 1;"
    try:
        cursor.execute(q, (id,))
        res = cursor.fetchall()
        return res
    except Exception as e:
        print("failed to get the trash-bins are full " + e)
        cnx.rollback()
        return None

def get_threshold():
    db = connect_to_db()
    cursor = cnx.cursor()
    q = "SELECT threshold FROM configuration;"
    try:
        cursor.execute(q)
        res = cursor.fetchall()
        return res[0][0]
    except Exception as e:
        print("failed to get the trash-bins are full " + e)
        cnx.rollback()
        return None

def get_sensor_stat_by_id(id):
    db = connect_to_db()
    cursor = cnx.cursor()
    q = "SELECT * FROM statistics where sensor_id = %s;"
    try:
        cursor.execute(q, (id,))
        res = cursor.fetchall()
        return res
    except Exception as e:
        print("failed to get the trash-bins are full " + e)
        cnx.rollback()
        return None


def get_sensors_ids():
    db = connect_to_db()
    cursor = cnx.cursor()
    q = "SELECT id FROM sensors;"
    try:
        cursor.execute(q,)
        res = cursor.fetchall()
        return res
    except Exception as e:
        print("failed to get the trash-bins are full " + e)
        cnx.rollback()
        return None


def get_sensors():
    db = connect_to_db()
    cursor = cnx.cursor()
    q = "SELECT * FROM sensors;"
    try:
        cursor.execute(q,)
        res = cursor.fetchall()
        return res
    except Exception as e:
        print("failed to get the trash-bins are full " + e)
        cnx.rollback()
        return None


def insert_battery_data(batt, id):
    db = connect_to_db()
    cursor = cnx.cursor()
    q = "UPDATE sensors SET battery=%s WHERE id = %s"
    data = (int(batt), id)
    try:
        cursor.execute(q, data)
        db.commit()
        logging.info('successes update driver to db')
    except Exception as e:
        logging.error('failed to update driver to db', e)

def get_last_two_days_statistics(id):
    db = connect_to_db()
    cursor = cnx.cursor()
    q = "select * from statistics WHERE sensor_id = %s order by date DESC limit 2"
    try:
        cursor.execute(q, (id,))
        result = cursor.fetchall()
        logging.info('successes update driver to db')
        return result
    except Exception as e:
        logging.error('failed to update driver to db', e)


def update_sensor_capacity_by_id(id, capacity):
    db = connect_to_db()
    cursor = cnx.cursor()
    q = "UPDATE sensors SET capacity=%s WHERE id = %s"
    data = (capacity, id)
    try:
        cursor.execute(q, data)
        db.commit()
        logging.info('successes update driver to db')
    except Exception as e:
        logging.error('failed to update driver to db', e)


def get_sensor_by_address(address):
    db = connect_to_db()
    cursor = cnx.cursor()
    q = """select * from sensors WHERE address like %s"""
    # data = (address, )
    cursor.execute(q, ('%' + str(address) + '%',))
    res = cursor.fetchall()
    if not res:
        return None
    return res


def get_statistcs_by_days(days):
    db = connect_to_db()
    cursor = cnx.cursor()
    q = "select DISTINCT date from statistics ORDER BY date desc limit %s;"
    data = (int(days), )
    cursor.execute(q, data)
    res = cursor.fetchall()
    if not res:
        return None
    return res


def get_avg_statatics_from_day(date):
    db = connect_to_db()
    cursor = cnx.cursor()
    q = "select avg(capacity) from statistics where date=%s;"
    data = (str(date), )
    cursor.execute(q, data)
    res = cursor.fetchall()
    if not res:
        return None
    return int(res[0][0])


def get_sum_volume_from_day(date):
    db = connect_to_db()
    cursor = cnx.cursor()
    q = "select sum(capacity) from statistics where date=%s;"
    data = (str(date), )
    cursor.execute(q, data)
    res = cursor.fetchall()
    if not res:
        return None
    return int(res[0][0])


def set_sensor_capacity_to_zero(trasbold):
    db = connect_to_db()
    cursor = cnx.cursor()
    q = "update sensors set capacity=0 where capacity > %s"
    data = (int(trasbold), )
    try:
        cursor.execute(q, data)
        db.commit()
        logging.info('cleanup task  - trashold capcity')
    except Exception as e:
        logging.error('fialed to cleanup task', e)


def set_sensor_capacity_to_zero_by_id(sensor_id):
    db = connect_to_db()
    cursor = cnx.cursor()
    q = "update sensors set capacity=0 where id = %s"
    data = (sensor_id, )
    try:
        cursor.execute(q, data)
        db.commit()
        logging.info('cleanup task  - trashold capcity')
    except Exception as e:
        logging.error('fialed to cleanup task', e)


def get_user_by_username(user):
    sql = "SELECT * FROM `users` WHERE `user`=%s"
    return None


def add_user(user, password):
    sql = f"INSERT INTO users (user, password) VALUES (%s, %s)"
    return None