import pymysql.cursors
from wise_dal.users import Users
from wise_dal.configuration import Configuration
from wise_dal.drivers import Drivers
from wise_dal.sensors import Sensors
from wise_dal.statistics import Statistics

import conf


class DbClient(object):
    def __init__(self):
        self.connection = None
        self.connection = pymysql.connect(host=conf.db_hostname,
                                          user=conf.db_user,
                                          password=conf.db_password,
                                          db=conf.db_schema_name,
                                          charset='utf8mb4',
                                          cursorclass=pymysql.cursors.DictCursor,
                                          autocommit=True,
                                          connect_timeout=31536000)

    def __del__(self):
        if self.connection:
            self.connection.close()

    def _select(self, VALUES, DATA=(), KEYS='*', ALL=False, ROLLBACK_ON_FAIL=False):
        try:
            self.tbl = 'users'
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

    @property
    def users(self):
        return Users(self.connection)

    @property
    def configuration(self):
        return Configuration(self.connection)

    @property
    def drivers(self):
        return Drivers(self.connection)

    @property
    def sensors(self):
        return Sensors(self.connection)

    @property
    def statistics(self):
        return Statistics(self.connection)


if __name__ == '__main__':
    db = DbClient()
    sql = f"`user`=%s"
    data = ('test',)
    db._select(sql, DATA=data, ALL=True)
