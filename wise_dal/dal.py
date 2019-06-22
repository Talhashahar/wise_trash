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
