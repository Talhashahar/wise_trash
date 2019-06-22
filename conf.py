#System configuration
google_api_token = '&key=AIzaSyBLT0yiIBSyM_l0PvIp7cH1rbPnfPfcETM'
db_user = 'root'
db_password = 'Smirnoffice1!'
db_schema_name = 'wisetrash'
#db_hostname = '35.241.162.141'
db_hostname = 'wisetrash-db.cewsykbhugos.eu-west-1.rds.amazonaws.com'
db_port = 3306
PASSWORD_PATTERN = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$"
LOG_TABLE = 'logs'


#application configuration
trash_threshold = 60
battery_threshold = 30

ALGO = 'HS256'
API_TOKEN_KEY = 'ThisIsMyKey'
PASSWORD_ENCRYPTION_KEY = str.encode('thisIsPasswordEncryptionKey')
