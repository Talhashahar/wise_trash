from openpyxl import load_workbook
from math import sin, cos, sqrt, atan2, radians


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


wb = load_workbook('Export_data.xlsx')
ws = wb['Row_Data']

coords_list = []

for row in ws.rows:
    for cell in row:
        if isinstance(cell.value, float):
            coords_list.append(cell.value)
pass


print ('distance in KM: ' + str(calculate_distance(32.0911975, 34.803235, 32.0908856, 34.8026718)))
print ('distance in M: ' + str(1000 * calculate_distance(32.0911975, 34.803235, 32.0908856, 34.8026718)))
