class Configuration:
    def __init__(self, connection):
        self.tbl = 'configuration'
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
    def get_threshold(self):
        sql = f""
        return self._select(sql, KEYS='threshold', ALL=True)

    # SET
    def update_treshold(self, new_threshold):
        try:
            current_treshold = self.get_threshold()
            with self.connection.cursor() as cursor:
                sql = "UPDATE configuration SET threshold=%s where threshold=%s"
                cursor.execute(sql, (new_threshold, current_treshold))
        except:
            self.connection.rollback()

    # DELETE

    # CREATE
