class Statistics:
    def __init__(self, connection):
        self.tbl = 'statistics'
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
    def get_sensor_stat_by_id(self, sensor_id):
        sql = f"`sensor_id` = %s"
        data = (sensor_id,)
        return self._select(sql, DATA=data, ALL=True)

    def get_sum_volume_from_day(self, date):
        sql = f"`date`=%s"
        data = (str(date),)
        return self._select(sql, DATA=data, ALL=False, KEYS='sum(capacity)')

    def get_avg_statatics_from_day(self, date):
        sql = f"date`=%s"
        data = (str(date),)
        return self._select(sql, DATA=data, ALL=False, KEYS='avg(capacity)')

    def get_last_update_sensors(self, sensor_id):
        sql = f"sensor_id = %s order by date desc limit 1"
        data = (sensor_id,)
        return self._select(sql, DATA=data, ALL=False)

    def get_statistcs_by_days(self, days):
        try:
            with self.connection.cursor() as cursor:
                sql = "select DISTINCT date from statistics ORDER BY date desc limit %s"
                cursor.execute(sql, (int(days),))
                result = cursor.fetchall()
                return result if result else None
        except:
            self.connection.rollback()

    # SET

    # DELETE

    # CREATE

    def insert_statistics(self, sensor_id, date, capacity):
        try:
            with self.connection.cursor() as cursor:
                sql = "insert into statistics (sensor_id, date, capacity) VALUES (%s, %s, %s)"
                cursor.execute(sql, (sensor_id, date, capacity))
        except:
            self.connection.rollback()
