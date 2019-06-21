class Sensors:
    def __init__(self, connection):
        self.tbl = 'sensors'
        self.connection = connection

    def _select(self, VALUES, DATA=(), KEYS='*', ALL=False, ROLLBACK_ON_FAIL=False):
        try:
            query = f'SELECT {KEYS} FROM {self.tbl} WHERE {VALUES}'
            with self.connection.cursor() as cursor:
                cursor.execute(query, DATA)
                if ALL:
                    result = cursor.fetchall()
                else:
                    result = cursor.fetchone()
                return result if result else None
        except Exception as e:
            if ROLLBACK_ON_FAIL:
                self.connection.rollback()
            print(e.__str__())

    # GET
    def get_sensor_by_address(self, address):
        sql = f"`address like %s"
        data = (address,)
        return self._select(sql, DATA=data, ALL=True)

    def get_sensors(self):
        sql = f""
        return self._select(sql, ALL=True)

    def get_sensors_ids(self):
        sql = f"`address like %s"
        return self._select(sql, KEYS='id', ALL=True)

    def get_count_sensors(self):
        sql = f""
        return self._select(sql, KEYS='count(*)', ALL=False)
        # maybe len(self.get_sensors()) ?

    def get_sensors_by_status(self, status):
        sql = f"`status` =%s"
        data = (status,)
        return self._select(sql, DATA=data, ALL=True)

    def get_sensors_count_by_status(self, status):
        sql = f"`status` =%s"
        data = (status,)
        return self._select(sql, KEYS='count(*)', DATA=data, ALL=True)

    def get_sensor_under_x_capacity(self, capacity):
        sql = f"`capacity` <=%s"
        data = (capacity,)
        return self._select(sql, DATA=data, ALL=True)

    def get_sensor_over_x_capacity(self, capacity):
        sql = f"`capacity` >=%s"
        data = (capacity,)
        return self._select(sql, DATA=data, ALL=True)

    def get_sensor_under_x_battery(self, battery):
        sql = f"`battery` <=%s"
        data = (battery,)
        return self._select(sql, DATA=data, ALL=True)

    def get_sensor_between_capacity(self, min, max):
        sql = f"`capacity` >=%s AND `capacity` <=%s "
        data = (min, max)
        return self._select(sql, DATA=data, ALL=True)

    def get_sensor_by_id(self, sensor_id):
        sql = f"id=%s"
        data = (sensor_id,)
        return self._select(sql, DATA=data, ALL=False)

    # SET
    def set_sensor_capacity_to_zero_by_id(self, sensor_id):
        try:
            with self.connection.cursor() as cursor:
                sql = f"UPDATE sensors set capacity=0 where id = %s"
                cursor.execute(sql, (sensor_id,))
            return cursor.lastrowid - 1
        except Exception as e:
            self.connection.rollback()

    def set_sensor_capacity_to_zero(self, trasbold):
        try:
            with self.connection.cursor() as cursor:
                sql = f"UPDATE sensors set capacity=0 where capacity > %s"
                cursor.execute(sql, (trasbold,))
            return cursor.lastrowid - 1
        except Exception as e:
            self.connection.rollback()

    def update_sensor_capacity_by_id(self, id, capacity):
        try:
            with self.connection.cursor() as cursor:
                sql = "UPDATE sensors SET capacity=%s WHERE id = %s"
                cursor.execute(sql, (capacity, id))
            return cursor.lastrowid - 1
        except Exception as e:
            self.connection.rollback()

    def update_sensor_by_id(self, id, address, capacity, lat, lng, status, update_date):
        try:
            with self.connection.cursor() as cursor:
                sql = "UPDATE sensors SET address=%s, capacity=%s, lat=%s, lng=%s, status=%s, last_update_date=%s WHERE id = %s"
                data = (str(address), int(capacity), float(lat), float(lng), status, update_date, id)
                cursor.execute(sql, data)
        except:
            self.connection.rollback()

    def insert_battery_data(self, batt, id):
        try:
            with self.connection.cursor() as cursor:
                sql = "UPDATE sensors SET battery=%s WHERE id = %s"
                data = (int(batt), id)
                cursor.execute(sql, data)
        except:
            self.connection.rollback()

    # DELETE

    def delete_sensor(self, sensor_id):
        try:
            with self.connection.cursor() as cursor:
                sql = "delete from sensors where id=%s"
                cursor.execute(sql, (sensor_id,))
        except:
            self.connection.rollback()

    # CREATE
    def insert_sensor(self, id, address, capacity, lat, lng, status, update_date):
        try:
            with self.connection.cursor() as cursor:
                sql = "insert into sensors(id, address, capacity, status, lat, lng, last_update_date) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                data = (id, address, capacity, status, float(lat), float(lng), update_date)
                cursor.execute(sql, data)
        except:
            self.connection.rollback()

# WTF
# def get_sensors_pickup_today():
#     db = connect_to_db()
#     cursor = cnx.cursor()
#     date = datetime.datetime.now()
#     yesterday = date.today() - timedelta(1)
#     q = "select count(*) from sensors where date = %s"
#     try:
#         cursor.execute(q, (date,))
#         res = cursor.fetchall()
#         return res
#     except Exception as e:
#         print("failed to get the trash-bins are full " + e)
#         return None
