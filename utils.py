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
