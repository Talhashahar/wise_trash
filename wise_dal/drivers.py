class Drivers:
    def __init__(self, connection):
        self.tbl = 'drivers'
        self.connection = connection

    def _select(self, VALUES, DATA=tuple(), KEYS='*', ALL=False, ROLLBACK_ON_FAIL=False):
        try:
            query = f'SELECT {KEYS} FROM {self.tbl} {VALUES}'
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
    def get_driver_by_id(self, driver_id):
        sql = f"`id=%s"
        data = (driver_id,)
        return self._select(sql, DATA=data, ALL=False)

    # SET
    def update_driver_by_id(self, id, name, lat, lng, truck_size):
        try:
            with self.connection.cursor() as cursor:
                sql = "UPDATE drivers SET name=%s, lat=%s, lng=%s, truck_size=%s  WHERE id = %s"
                data = (name, float(lat), float(lng), truck_size, id)
                cursor.execute(sql, data)
        except:
            self.connection.rollback()

    # DELETE
    def delete_driver(self, driver_id):
        try:
            with self.connection.cursor() as cursor:
                sql = "delete from drivers where id=%s"
                cursor.execute(sql, (driver_id,))
        except:
            self.connection.rollback()

    # CREATE
    def insert_driver(self, id, name, lat, lng, truck_size):
        try:
            with self.connection.cursor() as cursor:
                sql = "insert into drivers (id, name, lat,lng, truck_size) VALUES (%s, %s, %s, %s, %s)"
                data = (id, name, float(lat), float(lng), truck_size)
                cursor.execute(sql, data)
        except:
            self.connection.rollback()
