import pymysql
import logging
import conf


class LogDBHandler(logging.Handler):
    '''
    Customized logging handler that puts logs to the database.
    '''

    def __init__(self, connection, sql_cursor, db_tbl_log):
        logging.Handler.__init__(self)
        self.sql_cursor = sql_cursor
        self.connection = connection
        self.db_tbl_log = db_tbl_log

    def emit(self, record):
        self.log_msg = record.msg
        self.log_msg = self.log_msg.strip()
        self.log_msg = self.log_msg.replace('\'', '\'\'')
        sql = f'INSERT INTO {self.db_tbl_log} (level, log, module) VALUES (%s,%s,%s)'
        try:
            self.sql_cursor.execute(sql, (record.levelname, self.log_msg, record.name))
        # If error - print it out on screen. Since DB is not working - there's
        # no point making a log about it to the database :)
        except pymysql.Error as e:
            print(f'CRITICAL DB ERROR! Logging to database Failed {e.__str__()}')
            raise


class Logger:
    def __init__(self, name, tbl=conf.LOG_TABLE):
        connection = pymysql.connect(host=conf.db_hostname,
                                     user=conf.db_user,
                                     password=conf.db_password,
                                     db=conf.db_schema_name,
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor,
                                     autocommit=True,
                                     connect_timeout=31536000)
        log_cursor = connection.cursor()
        logdb = LogDBHandler(connection, log_cursor, tbl)
        self.log = logging.getLogger(name)
        self.log.addHandler(logdb)
        self.log.setLevel('DEBUG')

    def debug(self, message):
        self.log.debug(message)

    def info(self, message):
        self.log.info(message)

    def warning(self, message):
        self.log.warning(message)

    def error(self, message):
        self.log.error(message)

    def exception(self, message):
        self.log.exception(message)
