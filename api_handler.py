from flask import Flask, request, render_template, jsonify
import db_handler
import json
import datetime
import utils

app = Flask(__name__)

@app.route("/")
def index():
    online = db_handler.get_sensors_by_status("online")
    offline = db_handler.get_sensors_by_status("offline")
    pickup_today = db_handler.get_all_sensor_over_x_capacity(50)
    total = 0
    for bin in pickup_today:
        total = total + bin[2]
    return render_template('index.html', online=online, offline=offline, pickup_count=len(pickup_today), total_weight=total)


@app.route("/insert_driver/", methods=['GET', 'POST'])
def insert_driver():
    content = request.json
    if db_handler.get_driver_by_id(content['id']):
        db_handler.update_driver_by_id(content['id'], content['name'], content['lat'], content['lng'], content['truck_size']) #update
    else:
        db_handler.insert_driver(content['id'], content['name'], content['lat'], content['lng'], content['truck_size'])        #insert new
    return "success"

@app.route("/some_table")
def show_tables():
    all = db_handler.get_all_sensor_over_x_capacity(0)
    over_80 = db_handler.get_all_sensor_over_x_capacity(80)
    return render_template('WTtable.html', all=all, over_80=over_80)


@app.route("/map")
def map():
    return render_template('Map.html')


@app.route("/map_dyn")
def map_test():
    sensors = db_handler.get_all_sensor_over_x_capacity(0)
    print(sensors)

    capacity = request.args.get('capacity')
    if not capacity:
        sensors = [[x[1], x[4], x[5], x[3], x[2], x[0]] for x in sensors]
    else:
        capacity = int(capacity)
        sensors = [[x[1], x[4], x[5], x[3], x[2], x[0]] for x in sensors if int(x[2]) <= capacity]


    return render_template('mapsTEST.html', sensors=json.dumps(sensors))


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
    fake_date = '2019-04-05'
    db_handler.insert_statistics(content['id'], fake_date, content['capacity'])
    #db_handler.insert_statistics(content['id'], datetime.datetime.now().strftime("%Y-%m-%d %H:%M"), content['capacity'])
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


if __name__ == "__main__":
    print ("get starting flask server")
    app.run(debug=True)
