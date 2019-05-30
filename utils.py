import csv


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


def get_avg_fill_per_sensor(sensor_stats):
    sensor_stats = sensor_stats[::-1]
    days_to_calculate = 0
    max = sensor_stats[0][2]
    sensor_stats.pop(0)
    for sensor_stat in sensor_stats:
        if sensor_stat[2] < max:
            days_to_calculate = days_to_calculate + 1
        else:
            if days_to_calculate == 0:
                return max
            return max // days_to_calculate
    if days_to_calculate == 0:
        return max
    return max // days_to_calculate


def write_sensors_to_csv(sensor_list):
    with open("export.csv", 'w') as myfile:
        wr = csv.writer(myfile)
        wr.writerows(sensor_list)
