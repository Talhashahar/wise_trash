from flask import Flask, request, render_template, jsonify
import db_handler
import json
import utils
import configuration
import random
import datetime


app = Flask(__name__)


@app.route("/")
def index():
    online = db_handler.get_sensors_by_status("online")
    offline = db_handler.get_sensors_by_status("offline")
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
            if statistics_bin[1] > statistics_bin[0]:
                picked_up_bins = picked_up_bins + 1
    total_avg_fill = total_avg_fill / db_handler.get_count_sensors()
    for bin in pickup_today:
        need_to_pickup_total = need_to_pickup_total + bin[2]
    for bin in no_needed_pickup_today:
        no_need_to_pickup_total = no_need_to_pickup_total + bin[2]
    return render_template('index.html', online=int(online), offline=int(offline), total=online+offline, need_pickup_count=len(pickup_today), need_to_pickup_total=need_to_pickup_total, total_avg_fill=round(total_avg_fill, 3), no_need_to_pickup_total=no_need_to_pickup_total, no_needed_pickup_today=len(no_needed_pickup_today), low_battery_bins=len(low_battery_bins), picked_up_bins=picked_up_bins)


@app.route("/insert_driver/", methods=['GET', 'POST'])
def insert_driver():
    content = request.json
    if db_handler.get_driver_by_id(content['id']):
        db_handler.update_driver_by_id(content['id'], content['name'], content['lat'], content['lng'], content['truck_size']) #update
    else:
        db_handler.insert_driver(content['id'], content['name'], content['lat'], content['lng'], content['truck_size'])        #insert new
    return "success"

@app.route("/sensor_over_view")
def show_tables():
    all = db_handler.get_all_sensor_over_x_capacity(0)
    over_80 = db_handler.get_all_sensor_over_x_capacity(80)
    return render_template('sensor_overview.html', all=all, over_80=over_80)


@app.route("/map")
def map_test():
    sensors = db_handler.get_all_sensor_over_x_capacity(0)
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
    sensors = db_handler.get_all_sensor_over_x_capacity(0)
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
    #db_handler.insert_statistics(content['id'], fake_date, content['capacity'])
    db_handler.insert_statistics(content['id'], datetime.datetime.now().strftime("%Y-%m-%d %H:%M"), content['capacity'])
    if db_handler.get_sensor_by_id(content['id']):
        db_handler.update_sensor_by_id(content['id'], content['address'], content['capacity'], content['lat'], content['lng'], content['status'], fake_date)
    else:
        db_handler.insert_sensor(content['id'], content['address'], content['capacity'], content['lat'], content['lng'], content['status'], fake_date)
    return "ok"


@app.route('/get_trash_bins_to_pickup/')
def get_trash_bins_to_pickup():
    res = db_handler.get_all_sensor_over_x_capacity(50)
    return res


@app.route('/get_count_sensors/')
def get_count_sensors():
    res = db_handler.get_count_sensors()
    return res


@app.route('/get_count_sensors_changed/')
def get_count_sensors_changed():                                #need to get date from UI
    res = db_handler.get_count_sensors_changed()
    return res


@app.route('/get_last_update_sensors/')
def get_count_last_update_sensors():                                #need to get id from UI
    res = db_handler.get_last_update_sensors()
    return res

@app.route('/calc', methods=['GET', 'POST'])
def calc():
    if request.method == 'POST':
        new_threshold = configuration.trash_threshold
        configuration.trash_threshold = new_threshold
        #db_handler.update_treshold(new_threshold)
    capacity = request.args.get('capacity') or 70
    pickup_sensors = db_handler.get_all_sensor_over_x_capacity(capacity)
    remain_sensors = db_handler.get_all_sensor_under_x_capacity(capacity)
    threshold = configuration.trash_threshold
    risk_sensors = []
    for sensor in remain_sensors:
        fill_avg = utils.get_avg_fill_per_sensor(db_handler.get_sensor_stat_by_id(sensor[0]))
        if int(sensor[2]) + fill_avg >= threshold:
            risk_sensors.append(sensor)
    return render_template("Calc.html", sensors=pickup_sensors, capacityint=capacity, total_to_pickup=len(pickup_sensors), trash_treshold=threshold, risked=len(risk_sensors), unrisked=len(pickup_sensors) + len(remain_sensors) - len(risk_sensors))

@app.route("/base")
def base():
    return render_template('base.html')


@app.route("/zzz")
def zzz():
    # for i in range(1000, 1099):
    #     db_handler.insert_battery_data(random.randint(20, 100), i)
    temp = db_handler.get_last_two_days_statistics(1000)
    return "seucess"



if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
