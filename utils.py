import csv
from datetime import datetime, timedelta
import jwt
import conf as conf
import base64
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto import Random
import re
from wise_dal.dal import DbClient

from exceptions import TokenNotExists


def convert_sensor_tuple_to_json(obj):
    mydict = {
        "id": obj[0],
        "address": obj[1],
        'capacity': obj[2],
        'status': obj[3],
        'lat': obj[4],
        'lng': obj[5]
    }
    return mydict


def get_sensors_by_main_filters(request):
    db = DbClient()
    checked_list = []
    sensors = []
    if request.form.get('empty_Bins'):
        sensors_low = db.sensors.get_sensor_between_capacity(0, 25)
        if sensors_low:
            sensors += sensors_low
        checked_list.append('checked')
    else:
        sensors_low = []
        checked_list.append('')
    if request.form.get('mid_Bins'):
        sensors_mid = db.sensors.get_sensor_between_capacity(26, 75)
        if sensors_mid:
            sensors += sensors_mid
        checked_list.append('checked')
    else:
        sensors_mid = []
        checked_list.append('')
    if request.form.get('full_Bins'):
        sensors_full = db.sensors.get_sensor_between_capacity(76, 100)
        if sensors_full:
            sensors += sensors_full
        checked_list.append('checked')
    else:
        sensors_full = []
        checked_list.append('')
    if request.form.get('over_trashold'):
        over_trashold = db.sensors.get_sensor_between_capacity(conf.trash_threshold, 100)
        if over_trashold:
            sensors += over_trashold
        checked_list.append('checked')
    else:
        over_trashold = []
        checked_list.append('')
    if request.form.get('below_trashold'):
        sensors_below = db.sensors.get_sensor_between_capacity(0, conf.trash_threshold)
        if sensors_below:
            sensors += sensors_below
        checked_list.append('checked')
    else:
        sensors_below = []
        checked_list.append('')
    if request.form.get('ConnectedBins'):
        ConnectedBins = db.sensors.get_sensors_by_status("online")
        if ConnectedBins:
            sensors += ConnectedBins
        checked_list.append('checked')
    else:
        ConnectedBins = []
        checked_list.append('')
    if request.form.get('FailedBins'):
        FailedBins = db.sensors.get_sensors_by_status("offline")
        if FailedBins:
            sensors += FailedBins
        checked_list.append('checked')
    else:
        FailedBins = []
        checked_list.append('')
    sensors = [tuple(sensor.values()) for sensor in sensors]
    sensors = list(dict.fromkeys(sensors))
    return sensors, checked_list


def get_avg_fill_per_sensor(sensor_stats):
    if len(sensor_stats) < 5:
        return 0
    sensor_stats = sensor_stats[::-1]
    days_to_calculate = 0
    total_trash = 0
    for index, sensor_stat in enumerate(sensor_stats):
        if sensor_stat['capacity'] > sensor_stats[index + 1]['capacity']:
            days_to_calculate = days_to_calculate + 1
            total_trash += sensor_stat['capacity'] - sensor_stats[index + 1]['capacity']
        else:
            if days_to_calculate == 0:
                return total_trash
            return total_trash // days_to_calculate
    if days_to_calculate == 0:
        return total_trash
    return total_trash // days_to_calculate


def write_sensors_to_csv(sensor_list):
    csvtitle = ("sensor_id", "address", "capacity", "status", "longitude", "latitude", "last_time_updated")
    sensor_list.insert(0, csvtitle)
    with open("export.csv", 'w') as myfile:
        wr = csv.writer(myfile)
        wr.writerows(sensor_list)
    sensor_list.pop(0)


def encrypt(key, source, encode=True):
    key = SHA256.new(key).digest()  # use SHA-256 over our key to get a proper-sized AES key
    IV = Random.new().read(AES.block_size)  # generate IV
    encryptor = AES.new(key, AES.MODE_CBC, IV)
    padding = AES.block_size - len(source) % AES.block_size  # calculate needed padding
    source += bytes([padding]) * padding  # Python 2.x: source += chr(padding) * padding
    data = IV + encryptor.encrypt(source)  # store the IV at the beginning and encrypt
    return base64.b64encode(data).decode("latin-1") if encode else data


def decrypt(key, source, decode=True):
    if decode:
        source = base64.b64decode(source.encode("latin-1"))
    key = SHA256.new(key).digest()  # use SHA-256 over our key to get a proper-sized AES key
    IV = source[:AES.block_size]  # extract the IV from the beginning
    decryptor = AES.new(key, AES.MODE_CBC, IV)
    data = decryptor.decrypt(source[AES.block_size:])  # decrypt
    padding = data[-1]  # pick the padding value from the end; Python 2.x: ord(data[-1])
    if data[-padding:] != bytes([padding]) * padding:  # Python 2.x: chr(padding) * padding
        raise ValueError("Invalid padding...")
    return data[:-padding]  # remove the padding


def generate_token(user_id):
    '''
    generate JWT token from id and phone number
    :param user_id: int
    :param phone: str
    :return: str
    '''
    return jwt.encode(
        {'user_id': user_id, 'exp': datetime.utcnow() + timedelta(days=1)},
        conf.API_TOKEN_KEY, algorithm=conf.ALGO).decode('utf-8')


def get_data_by_token(token):
    '''
    decode JWT token to dict
    :param token: str
    :return: dict
    '''
    return jwt.decode(token, conf.API_TOKEN_KEY, algorithm=conf.ALGO)


def is_password_valid(password):
    pattern = re.compile(conf.PASSWORD_PATTERN)
    return bool(re.search(pattern, password))


def validate_token(request):
    try:
        token = request.cookies.get('token', None)
        if not token:
            raise TokenNotExists()
        user = get_data_by_token(token)
        return True
    except (jwt.ExpiredSignatureError, TokenNotExists):
        return False
