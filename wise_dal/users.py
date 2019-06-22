class Users:
    def __init__(self, connection):
        self.tbl = 'users'
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
    def get_user_by_username(self, user):
        sql = f"WHERE `user`=%s"
        data = (user,)
        return self._select(sql, DATA=data, ALL=False)

    def get_user_by_id(self, user_id):
        sql = f"WHERE `id`=%s"
        data = (user_id,)
        return self._select(sql, DATA=data, ALL=False)

    # SET

    # DELETE

    # CREATE

    def add_user(self, user, password):
        try:
            with self.connection.cursor() as cursor:
                sql = f"INSERT INTO {self.tbl} (user, password) VALUES (%s, %s)"
                cursor.execute(sql, (user, password))
            return cursor.lastrowid - 1
        except:
            self.connection.rollback()
