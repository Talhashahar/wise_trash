from flask import Flask, request, render_template, jsonify, send_file
import db_handler
import json
import utils
import configuration
import random
import datetime
from flask_cors import CORS

app = Flask(__name__)
CORS(app, supports_credentials=True, resources={r'/': {"origins": ''}})


@app.route("/")
def index():
    online = db_handler.get_sensors_count_by_status("online")
    offline = db_handler.get_sensors_count_by_status("offline")
    pickup_today = db_handler.get_sensor_over_x_capacity(int(configuration.trash_threshold))
    no_needed_pickup_today = db_handler.get_sensor_under_x_capacity(int(configuration.trash_threshold))
    low_battery_bins = db_handler.get_sensor_under_x_battery(configuration.battery_threshold)
    all_bins = db_handler.get_sensors()
    total_avg_fill = 0
    need_to_pickup_total = 0
    no_need_to_pickup_total = 0
    picked_up_bins = 0
    for bin in all_bins:
        total_avg_fill += utils.get_avg_fill_per_sensor(db_handler.get_sensor_stat_by_id(bin[0]))
        statistics_bin = db_handler.get_last_two_days_statistics(bin[0])
        if len(statistics_bin) == 2:
            if statistics_bin[1][2] > statistics_bin[0][2]:
                picked_up_bins = picked_up_bins + 1
    total_avg_fill = total_avg_fill / db_handler.get_count_sensors()
    for bin in pickup_today:
        need_to_pickup_total = need_to_pickup_total + bin[2]
    for bin in no_needed_pickup_today:
        no_need_to_pickup_total = no_need_to_pickup_total + bin[2]
    return render_template('index.html', online=int(online), offline=int(offline), total=online + offline,
                           need_pickup_count=len(pickup_today), need_to_pickup_total=need_to_pickup_total,
                           total_avg_fill=round(total_avg_fill, 3), no_need_to_pickup_total=no_need_to_pickup_total,
                           no_needed_pickup_today=len(no_needed_pickup_today), low_battery_bins=len(low_battery_bins),
                           picked_up_bins=picked_up_bins)


@app.route("/insert_driver/", methods=['GET', 'POST'])
def insert_driver():
    content = request.json
    if db_handler.get_driver_by_id(content['id']):
        db_handler.update_driver_by_id(content['id'], content['name'], content['lat'], content['lng'],
                                       content['truck_size'])  # update
    else:
        db_handler.insert_driver(content['id'], content['name'], content['lat'], content['lng'],
                                 content['truck_size'])  # insert new
    return "success"


@app.route("/sensor_over_view")
def show_tables():
    all = db_handler.get_sensor_over_x_capacity(0)
    over_80 = db_handler.get_sensor_over_x_capacity(80)
    return render_template('sensor_overview.html', all=all, over_80=over_80)


@app.route("/map")
def map_test():
    sensors = db_handler.get_sensor_over_x_capacity(0)
    capacity = request.args.get('capacity')
    if not capacity:
        sensors = [[x[1], x[4], x[5], x[3], x[2], x[0]] for x in sensors]
    else:
        capacity = int(capacity)
        sensors = [[x[1], x[4], x[5], x[3], x[2], x[0]] for x in sensors if int(x[2]) <= capacity]
    return render_template('map.html', sensors=json.dumps(sensors))


@app.route('/get_all_sensors_by_json')
def get_all_sensors_by_json():
    total_sensors = []
    sensors = db_handler.get_sensor_over_x_capacity(0)
    for sen in sensors:
        total_sensors.append(utils.convert_sensor_tuple_to_json(sen))
    return "ok"


@app.route('/get_sensor_by_id/<string:sensor_id>')
def get_sensor_by_id(sensor_id):
    res = db_handler.get_sensor_by_id(sensor_id)
    res = utils.convert_sensor_tuple_to_json(res)
    return jsonify(res), 200


@app.route("/create_all_tables/")
def create_all_tables():
    db_handler.create_all_tables()
    return "success"


@app.route("/insert_sensor/", methods=['GET', 'POST'])
def insert_sensor():
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
    content = request.json
    #fake_date = '2019-05-11'
    #date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
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
    res = db_handler.get_sensor_over_x_capacity(configuration.trash_threshold)
    return res


@app.route('/get_count_sensors/')
def get_count_sensors():
    res = db_handler.get_count_sensors()
    return res


@app.route('/get_count_sensors_changed/')
def get_count_sensors_changed():  # need to get date from UI
    res = db_handler.get_count_sensors_changed()
    return res


@app.route('/get_last_update_sensors/')
def get_count_last_update_sensors():  # need to get id from UI
    res = db_handler.get_last_update_sensors()
    return res


@app.route('/calc', methods=['GET', 'POST'])
def calc():
    if request.method == 'POST':
        new_threshold = configuration.trash_threshold
        configuration.trash_threshold = new_threshold
        # db_handler.update_treshold(new_threshold)
    capacity = request.args.get('capacity') or 70
    pickup_sensors = db_handler.get_sensor_over_x_capacity(capacity)
    remain_sensors = db_handler.get_sensor_under_x_capacity(capacity)
    threshold = configuration.trash_threshold
    risk_sensors = []
    for sensor in remain_sensors:
        fill_avg = utils.get_avg_fill_per_sensor(db_handler.get_sensor_stat_by_id(sensor[0]))
        if int(sensor[2]) + fill_avg >= threshold:
            risk_sensors.append(sensor)
    return render_template("Calc.html", sensors=pickup_sensors, capacityint=capacity,
                           total_to_pickup=len(pickup_sensors), trash_treshold=threshold, risked=len(risk_sensors),
                           unrisked=len(pickup_sensors) + len(remain_sensors) - len(risk_sensors))


@app.route("/base")
def base():
    return render_template('base.html')


@app.route("/update_sensor_by_id/<string:data>")
def update_sensor_by_id(data):
    sensor_id = data.split("_")[0]
    capacity = data.split("_")[1]
    db_handler.update_sensor_capacity_by_id(sensor_id, capacity)
    db_handler.insert_statistics(sensor_id, datetime.datetime.now().strftime("%Y-%m-%d %H:%M"), capacity)
    return "seccues"


@app.route("/new_index", methods=['GET', 'POST'])
def new_index():
    if request.method == 'POST':
        checked_list = []
        result = request.form
        sensors = []
        if request.form.get('empty_Bins'):
            sensors_low = db_handler.get_sensor_between_capacity(0, 25)
            sensors = sensors + sensors_low
            checked_list.append('checked')
        else:
            sensors_low = []
            checked_list.append('')
        if request.form.get('mid_Bins'):
            sensors_mid = db_handler.get_sensor_between_capacity(26, 75)
            sensors = sensors + sensors_mid
            checked_list.append('checked')
        else:
            sensors_mid = []
            checked_list.append('')
        if request.form.get('full_Bins'):
            sensors_full = db_handler.get_sensor_between_capacity(76, 100)
            sensors = sensors + sensors_full
            checked_list.append('checked')
        else:
            sensors_full = []
            checked_list.append('')
        if request.form.get('over_trashold'):
            over_trashold = db_handler.get_sensor_between_capacity(configuration.trash_threshold, 100)
            sensors = sensors + over_trashold
            checked_list.append('checked')
        else:
            over_trashold = []
            checked_list.append('')
        if request.form.get('below_trashold'):
            sensors_below = db_handler.get_sensor_between_capacity(0, configuration.trash_threshold)
            sensors = sensors + sensors_below
            checked_list.append('checked')
        else:
            sensors_below = []
            checked_list.append('')
        if request.form.get('ConnectedBins'):
            ConnectedBins = db_handler.get_sensors_by_status("online")
            sensors = sensors + ConnectedBins
            checked_list.append('checked')
        else:
            ConnectedBins = []
            checked_list.append('')
        if request.form.get('FailedBins'):
            FailedBins = db_handler.get_sensors_by_status("offline")
            sensors = sensors + FailedBins
            checked_list.append('checked')
        else:
            FailedBins = []
            checked_list.append('')
        for sensor in sensors:
            sensor = [sensor, ]
            if int(sensor[0][2]) < 25:
                sensors_low = sensors_low + sensor
            elif int(sensor[0][2]) < 75:
                sensors_mid = sensors_mid + sensor
            else:
                sensors_full = sensors_full + sensor
    else:
        sensors_low = db_handler.get_sensor_between_capacity(0, 25)
        sensors_mid = db_handler.get_sensor_between_capacity(26, 75)
        sensors_full = db_handler.get_sensor_between_capacity(76, 100)
        sensors = sensors_low + sensors_mid + sensors_full
        sensors = [[x[1], x[4], x[5], x[3], x[2], x[0]] for x in sensors]
        utils.write_sensors_to_csv(sensors)
        return render_template("new/WISE2_main.html", sensors=sensors, sensors_low=sensors_low, sensors_mid=sensors_mid,
                               sensors_full=sensors_full)
    sensors = [[x[1], x[4], x[5], x[3], x[2], x[0]] for x in sensors]
    utils.write_sensors_to_csv(sensors)
    return render_template("new/WISE2_main.html", sensors=sensors, sensors_low=sensors_low, sensors_mid=sensors_mid,
                           sensors_full=sensors_full, capacity_empty=checked_list[0], capacity_mid=checked_list[1],
                           capacity_full=checked_list[2], over_trashold=checked_list[3], below_trashold=checked_list[4],
                           ConnectedBins=checked_list[5], FailedBins=checked_list[6])


@app.route("/new_bindata", methods=['GET', 'POST'])
def new_databins():
    if request.method == 'POST':
        result = request.form
        if result['radio-stacked'] == "capacity":
            zzz = result['radio-stacked']
            sensors = db_handler.get_sensor_between_capacity(result['capacity'], 100)
            sensors = [[x[0], x[1], x[2], x[3], x[6]] for x in sensors]
        elif result['radio-stacked'] == 'id':
            sensors = db_handler.get_sensor_by_id(result['Bin_ID'])
            sensors = [[sensors[0], sensors[1], sensors[2], sensors[3], sensors[6]], ]
            pass
        else:
            sensors = db_handler.get_sensor_by_address(result['address'])
            sensors = [[x[0], x[1], x[2], x[3], x[6]] for x in sensors]
            pass
    else:
        sensors_low = db_handler.get_sensor_between_capacity(0, 25)
        sensors_mid = db_handler.get_sensor_between_capacity(26, 75)
        sensors_full = db_handler.get_sensor_between_capacity(76, 100)
        sensors = sensors_low + sensors_mid + sensors_full
    utils.write_sensors_to_csv(sensors)
    return render_template("new/WISE2_DataBins.html", sensors=sensors)


@app.route("/new_calc")
def new_calc():
    if request.method == 'POST':
        new_threshold = configuration.trash_threshold
        configuration.trash_threshold = new_threshold
        # db_handler.update_treshold(new_threshold)
    capacity = request.args.get('capacity') or 70
    pickup_sensors = db_handler.get_sensor_over_x_capacity(capacity)
    remain_sensors = db_handler.get_sensor_under_x_capacity(capacity)
    threshold = configuration.trash_threshold
    risk_sensors = []
    # for sensor in remain_sensors:
    #     fill_avg = utils.get_avg_fill_per_sensor(db_handler.get_sensor_stat_by_id(sensor[0]))
    #     if int(sensor[2]) + fill_avg >= threshold:
    #         risk_sensors.append(sensor)

    # return render_template("new/Calc.html")
    return render_template("new/Calc.html", sensors=pickup_sensors, capacityint=capacity,
                           total_to_pickup=len(pickup_sensors), trash_treshold=threshold, risked=len(risk_sensors),
                           unrisked=len(pickup_sensors) + len(remain_sensors) - len(risk_sensors))


@app.route("/new_stats")
def new_stats():
    return render_template("new/WISE2_stats.html")


@app.route("/new_about")
def new_about():
    return render_template("new/WISE2_about.html")


@app.route("/download/<string:data>")
def download(data):
    if data == 'full':
        utils.write_sensors_to_csv(db_handler.get_sensors())
    return send_file('export.csv', attachment_filename='export.csv')


@app.route("/get_avg_capacity_and_days")
def get_avg_capacity_and_days():
    res = []
    sensors = db_handler.get_sensors()
    days = db_handler.get_five_days_from_statistcs()
    avg_days = []
    sum_days = []
    for day in days:
        temp_dict_avg = {'day': day[0].strftime("%Y-%m-%d"),
                         'avg': db_handler.get_avg_statatics_from_day(day[0].strftime("%Y-%m-%d"))}
        temp_dict_sum = {'day': day[0].strftime("%Y-%m-%d"),
                         'sum': db_handler.get_sum_volume_from_day(day[0].strftime("%Y-%m-%d"))}
        avg_days += [temp_dict_avg, ]
        sum_days += [temp_dict_sum, ]
    online = len(db_handler.get_sensors_by_status("online")) - 20
    offline = len(db_handler.get_sensors_by_status("offline")) + 20
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
