from flask import Flask, request, render_template, jsonify, send_file, make_response
# import db_handler
import json
import jwt
import traceback
import utils
import conf
import datetime
from flask_cors import CORS
from utils import is_password_valid, encrypt, decrypt, generate_token, get_data_by_token, validate_token
from exceptions import *
from logger import Logger
from wise_dal.dal import DbClient

app = Flask(__name__)
CORS(app, supports_credentials=True, resources={r'/': {"origins": ''}})
logger = Logger(__name__)
db_handler = None


@app.route("/insert_driver/", methods=['GET', 'POST'])
def insert_driver():
    db = DbClient()
    content = request.json
    # if db.drivers.get_driver_by_id(content['id']):
    #     pass
    if db_handler.get_driver_by_id(content['id']):
        db_handler.update_driver_by_id(content['id'], content['name'], content['lat'], content['lng'],
                                       content['truck_size'])  # update
    else:
        db_handler.insert_driver(content['id'], content['name'], content['lat'], content['lng'],
                                 content['truck_size'])  # insert new
    return "success"


@app.route("/sensor_over_view")
def show_tables():
    db = DbClient()
    all = db_handler.get_sensor_over_x_capacity(0)
    over_80 = db_handler.get_sensor_over_x_capacity(80)
    return render_template('sensor_overview.html', all=all, over_80=over_80)


@app.route("/register", methods=['GET', 'POST'])
def register():
    db = DbClient()
    if request.method == 'POST':
        try:
            data = request.values
            user = data.get('username')
            password = data.get('password')
            if not is_password_valid(password):
                raise PasswordInvalid()
            else:
                password = str(encrypt(conf.PASSWORD_ENCRYPTION_KEY, str.encode(password)))
            if not (user and password):
                raise EmptyForm()
            user_data = db_handler.get_user_by_username(user)
            if user_data:
                raise UserAlreadyExists(user)
            else:
                db_handler.add_user(user, password)
                return 'ok', 200  # DO what you want is good

        except PasswordInvalid as e:
            logger.warning(e.__str__())
            return e.__str__(), 401
        except UserAlreadyExists as e:
            logger.warning(e.__str__())
            return e.__str__(), 401
        except (EmptyForm, ValueError) as e:
            logger.warning(e.__str__())
            return e.__str__(), 406
        except Exception as e:
            logger.exception(f'Failed register')
            return f'Failed register {e.__str__()}', 501
    else:
        return render_template('register.html')


@app.route("/", methods=['GET', 'POST'])
def login():
    '''
    POST login to system and generate JWT token
    :param request: flask request object
    '''
    db = DbClient()
    if request.method == 'POST':
        try:
            data = request.values
            user = data.get('username')
            password = data.get('password')
            if not (user and password):
                logger.info(f'Login failed on {request.remote_addr}, missing credentials')
                raise InvalidCredentials(user, password)

            user_data = db.users.get_user_by_username(user)
            if not user_data:
                raise UserNotExists(user)

            elif not (str.encode(password) == decrypt(conf.PASSWORD_ENCRYPTION_KEY, user_data['password'])):
                raise InvalidCredentials(user)
            else:
                token = generate_token(user_data['id'])
                logger.info(f'Token for user {user} created. token: {token}')
                sensors = []
                sensors_low = db.sensors.get_sensor_between_capacity(0, 25)
                if sensors_low:
                    sensors += sensors_low
                sensors_mid = db.sensors.get_sensor_between_capacity(26, 75)
                if sensors_mid:
                    sensors += sensors_mid
                sensors_full = db.sensors.get_sensor_between_capacity(76, 100)
                if sensors_full:
                    sensors += sensors_full
                sensors = [tuple(sensor.values()) for sensor in sensors]
                utils.write_sensors_to_csv(sensors)
                sensors = [[x[1], x[4], x[5], x[3], x[2], x[0]] for x in sensors]
                resp = make_response(render_template("index.html", sensors=sensors))
                resp.set_cookie('token', token)
                return resp

        except UserNotVerified as e:
            logger.warning(e.__str__())
            return e.__str__(), 401
        except UserNotExists as e:
            logger.warning(e.__str__())
            return e.__str__(), 404
        except InvalidCredentials as e:
            logger.warning(e.__str__())
            return e.__str__(), 401
        except Exception as e:
            logger.exception(f'Failed login from {request.remote_addr}')
            return f'Failed login {e.__str__()}', 501
    else:
        return render_template('login.html')


@app.route('/get_all_sensors_by_json')
def get_all_sensors_by_json():
    db = DbClient()
    total_sensors = []
    sensors = db_handler.get_sensor_over_x_capacity(0)
    for sen in sensors:
        total_sensors.append(utils.convert_sensor_tuple_to_json(sen))
    return "ok"


@app.route('/get_sensor_by_id/<string:sensor_id>')
def get_sensor_by_id(sensor_id):
    db = DbClient()
    res = db_handler.get_sensor_by_id(sensor_id)
    res = utils.convert_sensor_tuple_to_json(res)
    return jsonify(res), 200


@app.route("/create_all_tables/")
def create_all_tables():
    db = DbClient()
    db_handler.create_all_tables()
    return "success"


@app.route("/insert_sensor/", methods=['GET', 'POST'])
def insert_sensor():
    db = DbClient()
    content = request.json
    fake_date = '2019-05-11'
    date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    # db_handler.insert_statistics(content['id'], fake_date, content['capacity'])
    db_handler.insert_statistics(content['id'], datetime.datetime.now().strftime("%Y-%m-%d %H:%M"), content['capacity'])
    if db_handler.get_sensor_by_id(content['id']):
        db_handler.update_sensor_by_id(content['id'], content['address'], content['capacity'], content['lat'],
                                       content['lng'], content['status'], date)
    else:
        db_handler.insert_sensor(content['id'], content['address'], content['capacity'], content['lat'], content['lng'],
                                 content['status'], date)
    return "ok"


@app.route("/insert_sensor_date/", methods=['GET', 'POST'])
def insert_sensor_date():
    db = DbClient()
    content = request.json
    # fake_date = '2019-05-11'
    # date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    # db_handler.insert_statistics(content['id'], fake_date, content['capacity'])
    date = content['date']
    db_handler.insert_statistics(content['id'], date, content['capacity'])
    if db_handler.get_sensor_by_id(content['id']):
        db_handler.update_sensor_by_id(content['id'], content['address'], content['capacity'], content['lat'],
                                       content['lng'], content['status'], date)
    else:
        db_handler.insert_sensor(content['id'], content['address'], content['capacity'], content['lat'], content['lng'],
                                 content['status'], date)
    return "ok"


@app.route('/get_trash_bins_to_pickup/')
def get_trash_bins_to_pickup():
    db = DbClient()
    res_json = {
        'arr': [
        ],
        'driver': {
            'lat': 32.23,
            'lng': 32.23
        },
        'capacity': 0
    }
    total_capacity = 0
    res = db.sensors.get_sensor_over_x_capacity(conf.trash_threshold)
    for x in res:
        res_json['arr'].append({'lat': x['lat'], 'lng': x['lng']})
        total_capacity += x['capacity']
    res_json['capacity'] = total_capacity
    return jsonify(res_json), 200


@app.route('/get_count_sensors/')
def get_count_sensors():
    db = DbClient()
    res = db.sensors.get_count_sensors()  # ['count(*)']
    return res


# @app.route('/get_count_sensors_changed/')
# def get_count_sensors_changed():  # need to get date from UI
#     db = DbClient()
#     res = db.sensors.get_count_sensors_changed()
#     return res


# @app.route('/get_last_update_sensors/')
# def get_count_last_update_sensors():  # need to get id from UI
#     db = DbClient()
#     res = db_handler.get_last_update_sensors()
#     return res


@app.route("/base")
def base():
    return render_template('base.html')


@app.route("/update_sensor_by_id/<string:data>")
def update_sensor_by_id(data):
    db = DbClient()
    sensor_id = data.split("_")[0]
    capacity = data.split("_")[1]
    db.sensors.update_sensor_capacity_by_id(sensor_id, capacity)
    db.statistics.insert_statistics(sensor_id, datetime.datetime.now().strftime("%Y-%m-%d %H:%M"), capacity)
    return jsonify({'status': 'ok'}), 200


@app.route("/main", methods=['GET', 'POST'])
def main():
    db = DbClient()
    try:
        if not validate_token(request):
            return render_template("error_page.html")
        user = get_data_by_token(request.cookies.get('token', None))
        if request.method == 'POST':
            sensors_low = []
            sensors_mid = []
            sensors_full = []
            sensors, checked_list = utils.get_sensors_by_main_filters(request)
            for sensor in sensors:
                sensor = [sensor, ]
                if int(sensor[0][2]) < 25:
                    sensors_low = sensors_low + sensor
                elif int(sensor[0][2]) < 75:
                    sensors_mid = sensors_mid + sensor
                else:
                    sensors_full = sensors_full + sensor
        else:
            sensors = []
            sensors_low = db.sensors.get_sensor_between_capacity(0, 25)
            if sensors_low:
                sensors += sensors_low
            sensors_mid = db.sensors.get_sensor_between_capacity(26, 75)
            if sensors_mid:
                sensors += sensors_mid
            sensors_full = db.sensors.get_sensor_between_capacity(76, 100)
            if sensors_full:
                sensors += sensors_full
            sensors = [tuple(sensor.values()) for sensor in sensors]
            utils.write_sensors_to_csv(sensors)
            sensors = [[x[1], x[4], x[5], x[3], x[2], x[0]] for x in sensors]
            return render_template("index.html", sensors=sensors, persent_count=len(sensors), total_count=len(sensors))
        utils.write_sensors_to_csv(sensors)
        sensor_count = db.sensors.get_count_sensors()['count(*)']
        sensors = [[x[1], x[4], x[5], x[3], x[2], x[0]] for x in sensors]
        return render_template("index.html", sensors=sensors, capacity_empty=checked_list[0],
                               capacity_mid=checked_list[1],
                               capacity_full=checked_list[2], over_trashold=checked_list[3],
                               below_trashold=checked_list[4],
                               ConnectedBins=checked_list[5], FailedBins=checked_list[6], persent_count=len(sensors),
                               total_count=sensor_count)

    except Exception as e:
        print(traceback.format_exc())
        print(e)


@app.route("/bindata", methods=['GET', 'POST'])
def new_databins():
    db = DbClient()
    if not validate_token(request):
        return render_template("error_page.html")
    user = get_data_by_token(request.cookies.get('token', None))
    if request.method == 'POST':
        result = request.form
        if result['radio-stacked'] == "capacity":
            sensors = db.sensors.get_sensor_between_capacity(result['capacity'], 100)
            if not sensors:
                return render_template("databins.html")
            #sensors = [[x[0], x[1], x[2], x[3], x[6]] for x in sensors]
        elif result['radio-stacked'] == 'id':
            sensors = db.sensors.get_sensor_by_id(result['Bin_ID'])
            if sensors is not None:
                #sensors = [[sensors[0], sensors[1], sensors[2], sensors[3], sensors[6]], ]
                pass
            else:
                return render_template("databins.html")
        else:
            sensors = db.sensors.get_sensor_by_address(result['address'])
            if not sensors:
                return render_template("databins.html")
            #sensors = [[x[0], x[1], x[2], x[3], x[6]] for x in sensors]
    else:
        sensors_low = db.sensors.get_sensor_between_capacity(0, 25)
        if not sensors_low:
            sensors_low = []
        sensors_mid = db.sensors.get_sensor_between_capacity(26, 75)
        if not sensors_mid:
            sensors_mid = []
        sensors_full = db.sensors.get_sensor_between_capacity(76, 100)
        if not sensors_full:
            sensors_full = []
        sensors = sensors_low + sensors_mid + sensors_full
    if type(sensors) is dict:
        tuple_sensors = [tuple(sensors.values()), ]
        sensors = [sensors, ]
    else:
        tuple_sensors = [tuple(sensor.values()) for sensor in sensors]
    utils.write_sensors_to_csv(tuple_sensors)
    return render_template("databins.html", sensors=sensors)


@app.route("/calc", methods=['GET', 'POST'])
def new_calc():
    db = DbClient()
    if not validate_token(request):
        return render_template("error_page.html")
    user = get_data_by_token(request.cookies.get('token', None))
    username = db.users.get_user_by_id(user['user_id'])['user']
    config_trashold = conf.trash_threshold
    present_treshold = conf.trash_threshold
    if request.method == 'POST':
        if request.form.get('range'):
            present_percent = request.form.get('range')
            capacity = int(present_percent)
            present_treshold = capacity
        if request.form.get('trashold'):
            result = request.form.get('trashold')
            if '%' in result:
                threshold = int(result[:-1])
            else:
                threshold = int(result)
            conf.trash_threshold = int(threshold)
            capacity = int(conf.trash_threshold)
            config_trashold = capacity
            present_treshold = capacity
    else:
        capacity = 70
    pickup_sensors = db.sensors.get_sensor_over_x_capacity(capacity)
    if not pickup_sensors:
        pickup_sensors = []
    remain_sensors = db.sensors.get_sensor_under_x_capacity(capacity)
    if not remain_sensors:
        remain_sensors = []
    threshold = conf.trash_threshold
    risk_sensors = []
    # for sensor in remain_sensors:
    #     fill_avg = utils.get_avg_fill_per_sensor(db_handler.get_sensor_stat_by_id(sensor[0]))
    #     if int(sensor[2]) + fill_avg >= threshold:
    #         risk_sensors.append(sensor)

    # return render_template("new/calc.html")
    return render_template("calc.html", sensors=pickup_sensors, capacityint=capacity,
                           total_to_pickup=len(pickup_sensors), config_trashold=config_trashold,
                           present_treshold=present_treshold, risked=len(risk_sensors),
                           unrisked=len(pickup_sensors) + len(remain_sensors) - len(risk_sensors), username=username)


@app.route("/stats", methods=['GET', 'POST'])
def new_stats():
    db = DbClient()
    if not validate_token(request):
        return render_template("error_page.html")
    user = get_data_by_token(request.cookies.get('token', None))
    return render_template("analytics.html")


@app.route("/about")
def new_about():
    if not validate_token(request):
        return render_template("error_page.html")
    user = get_data_by_token(request.cookies.get('token', None))
    return render_template("about.html")


@app.route("/error")
def error():
    return render_template("error_page.html")


@app.route("/download/<string:data>")
def download(data):
    db = DbClient()
    if not validate_token(request):
        return render_template("error_page.html")
    user = get_data_by_token(request.cookies.get('token', None))
    if data == 'full':
        sensors = db.sensors.get_sensors()
        sensors = [tuple(sensor.values()) for sensor in sensors]
        utils.write_sensors_to_csv(sensors)
    return send_file('export.csv', attachment_filename='export.csv')


@app.route("/get_avg_capacity_and_days")
def get_avg_capacity_and_days():
    db = DbClient()
    res = []
    sensors = db.sensors.get_sensors()
    days = db.statistics.get_statistcs_by_days(7)
    avg_days = []
    sum_days = []
    for day in days:
        temp_dict_avg = {'day': day['date'].strftime("%Y-%m-%d"),
                         'avg': int(db.statistics.get_avg_statatics_from_day(day['date'].strftime("%Y-%m-%d"))[
                                        'avg(capacity)'])}
        temp_dict_sum = {'day': day['date'].strftime("%Y-%m-%d"),
                         'sum': int(db.statistics.get_sum_volume_from_day(day['date'].strftime("%Y-%m-%d"))['sum(capacity)'])}
        avg_days += [temp_dict_avg, ]
        sum_days += [temp_dict_sum, ]
    online = len(db.sensors.get_sensors_by_status("online"))
    offline = len(db.sensors.get_sensors_by_status("offline"))
    response = {
        'avg_array': avg_days,
        'sum_array': sum_days,
        'online': online,
        'offline': offline
    }
    # response['sum_array'][2]['sum'] = 100
    return jsonify(response), 200


@app.route("/get_volume_capacity_and_days")
def get_volume_capacity_and_days():
    db = DbClient()
    res = []
    sensors = db_handler.get_sensors()
    days = db_handler.get_five_days_from_statistcs()
    avg_days = []
    for day in days:
        temp_dict = {'day': day[0].strftime("%Y-%m-%d"),
                     'avg': db_handler.get_sum_volume_from_day(day[0].strftime("%Y-%m-%d"))}
        avg_days += [temp_dict, ]
    return jsonify(avg_days), 200


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
