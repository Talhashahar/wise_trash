from random import randrange, choice
import requests
from math import sin, cos, sqrt, atan2, radians
import time



def calculate_distance(a_lat, a_lng, b_lat, b_lng):
    global_radius = 6373.0                                                          #approximate radius of earth in km
    lat1 = radians(a_lat)
    lon1 = radians(a_lng)
    lat2 = radians(b_lat)
    lon2 = radians(b_lng)
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = global_radius * c
    return distance


def get_ordered_list(points, x, y):
   """

   :type points: object list of coords (lan and lng)
   """
   points.sort(key = lambda p: sqrt((p.x - x)**2 + (p.y - y)**2))
   return points


#wb = load_workbook('Export_data.xlsx')
#ws = wb['Row_Data']

#coords_list = []

#for row in ws.rows:
#    for cell in row:
#        if isinstance(cell.value, float):
#            coords_list.append(cell.value)
pass


#print ('distance in KM: ' + str(calculate_distance(32.0911975, 34.803235, 32.0908856, 34.8026718)))
#print ('distance in M: ' + str(1000 * calculate_distance(32.0911975, 34.803235, 32.0908856, 34.8026718)))
#status = ['ok', 'not ok', 'error', 'zibi']
#url = 'http://127.0.0.1:5000/insert_sensors'
#for x in range(1, 100):
#    my_data = {'id':x, 'capacity': randrange(1,100), 'status': choice(status)}
#    requests.post(url, json= my_data)
"""
start_time = time.time()
for x in range(0, 10000000):
    calculate_distance(32.0911975, 34.803235 , 32.089582, 34.8020499)
print("--- %s seconds ---" % (time.time() - start_time))
print ("done")
"""


#import requests
#url = 'http://127.0.0.1:5000/inset_driver/'
#contents = open('C:\\Users\\talha\\Desktop\\wise_trash\\driver_json.json', 'rb').read()
#r = requests.post(url, data=contents)