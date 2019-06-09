import numpy as np
import datetime
import json
import random
import googleAPI_handler
import requests
import db_handler

#url = 'http://3.16.166.50:80/insert_sensor/'
url = 'http://localhost:5000/insert_sensor/'
headers = {'content-type': 'application/json'}
#response = requests.post(url, data=json.dumps(data), headers=headers)


#import mysql.connector


#print('before')
#mysql.connector.connect(host='35.241.162.141', database='mysql', user='root', password='')
#mysql.connector.connect(host='localhost', database='mysql', user='root', password='Password1', port=3307)
#print ('after')
#pass

mydict = {
    "id": None,
    "address": None,
    'capacity': None,
    'status': None,
    'lat': None,
    'lng': None
}
mydict_date = {
    "id": None,
    "address": None,
    'capacity': None,
    'status': None,
    'lat': None,
    'lng': None,
    'date': None
}
'''

index = 1
for i in range(1, 100):
    mydict['id'] = random.randint(1, 30)
    mydict['capacity'] = random.randint(1, 100)
    if random.randint(0, 1):
        mydict['status'] = 'ok'
    else:
        mydict['status'] = 'broken'
    mydict['lat'] = random.randint(1, 120)
    mydict['lng'] = random.randint(1, 120)
    response = requests.post(url, data=json.dumps(mydict), headers=headers)
    print(index)
    index = index + 1
'''

total_list = []
city_name = 'Ramat+Gan+'
streets = ['Hamelacha', 'Anne+Frank+', 'Yeda+Am+', 'Brurya', 'Yehudit', 'Charusim']
streets_numbers = [16, 30, 21, 5, 13, 14]
thin_arr = ['Brurya', 'Yehudit']
thin_arr_numbers = [5, 13]
st_s = ['Anne+Frank+', 'Yeda+Am+']
st_n_s = [30, 21]

#
# print("create all addresses from google api")
# index = 0
# for i in range(0, len(streets)):
#     total_list.append(googleAPI_handler.get_cords_by_full_address(city_name, streets[i], streets_numbers[i]))
# print('done')
'''
n_list = []
for li in total_list:
    n_list.append(list(set(li)))
'''
#
# print("insert all sensors to our db")
# index = 1
# sumlist = sum(streets_numbers)
# count_id = 1000
# for street in total_list:
#     for house in street:
#         resp = requests.get('http://localhost:5000/get_sensor_by_id/1000')
#         mydict['id'] = str(count_id)
#         mydict['address'] = house['full_address']
#         mydict['capacity'] = random.randint(1, 100)
#         if random.randint(0, 1):
#             mydict['status'] = 'online'
#         else:
#             mydict['status'] = 'offline'
#         mydict['lat'] = float(house['lat'])
#         mydict['lng'] = float(house['lng'])
#         response = requests.post(url, data=json.dumps(mydict), headers=headers)
#         print(str(index) + " of : " + str(sumlist))
#         index = index + 1
#         count_id = count_id + 1


def init_sensor_for_capacity_0():
    #init all sensor for 0 capcity and
    for i in range(1000, 1099):
        link = 'http://localhost:5000/get_sensor_by_id/' + str(i)
        resp = requests.get(link).json()
        resp['status'] = 'online'
        resp['capacity'] = 0
        response = requests.post(url, data=json.dumps(resp), headers=headers)


def inc_sensor_capacity_for_statistics():
    url = 'http://localhost:5000/insert_sensor_date/'
    #inc all sensor capcity for statistics
    fake_date = datetime.datetime.strptime("2017-06-07", "%Y-%m-%d")
    max_days = 5*365
    index_days = 1
    for years in range(1, 2):
        for days in range(1, 365):
            data = np.random.normal(15, 2, 100)
            index = 0
            for i in range(1000, 1099):
                print('insert sensor number: ' + str(i) + ' day number: ' + str(index_days) + ' of: ' + str(max_days))
                link = 'http://localhost:5000/get_sensor_by_id/' + str(i)
                resp = requests.get(link).json()
                mydict_date['id'] = resp['id']
                mydict_date['address'] = resp['address']
                mydict_date['capacity'] = int(resp['capacity']) + int(data[index])
                mydict_date['lat'] = resp['lat']
                mydict_date['lng'] = resp['lng']
                mydict_date['status'] = resp['status']
                mydict_date['date'] = str(fake_date)
                response = requests.post(url, data=json.dumps(mydict_date), headers=headers)
                index += 1
            db_handler.set_sensor_capacity_to_zero(70)
            fake_date = fake_date + datetime.timedelta(days=1)
            index_days += 1


def dec_sensor_capacity_for_statistics():
    # inc all sensor capcity for statistics
    for i in range(1000, 1099):
        temp_num = random.randint(1, 4)
        if temp_num == 1:
            link = 'http://localhost:5000/get_sensor_by_id/' + str(i)
            resp = requests.get(link).json()
            resp['status'] = 'online'
            resp['capacity'] = random.randint(1, 20)
            if resp['capacity'] > 100:
                resp['capacity'] = 100
            response = requests.post(url, data=json.dumps(resp), headers=headers)


def init_db_with_data():
    total_list = []
    city_name = 'Ramat+Gan+'
    streets = ['Hamelacha', 'Anne+Frank+']
    streets_numbers = [3, 3]
    #streets = ['Hamelacha', 'Anne+Frank+', 'Yeda+Am+', 'Brurya', 'Yehudit', 'Charusim']
    #streets_numbers = [16, 30, 21, 5, 13, 14]
    print("create all addresses from google api")
    index = 0
    for i in range(0, len(streets)):
        total_list.append(googleAPI_handler.get_cords_by_full_address(city_name, streets[i], streets_numbers[i]))
    print("insert all sensors to our db")
    index = 1
    sumlist = sum(streets_numbers)
    count_id = 1000
    for street in total_list:
        for house in street:
            #resp = requests.get('http://localhost:5000/get_sensor_by_id/1000')
            mydict['id'] = str(count_id)
            mydict['address'] = house['full_address']
            mydict['capacity'] = random.randint(1, 100)
            randnumber = random.randint(0, 10)
            if randnumber > 8:
                mydict['status'] = 'online'
            else:
                mydict['status'] = 'offline'
            mydict['lat'] = float(house['lat'])
            mydict['lng'] = float(house['lng'])
            response = requests.post(url, data=json.dumps(mydict), headers=headers)
            print(str(index) + " of : " + str(sumlist))
            index = index + 1
            count_id = count_id + 1


def init_db_with_data_date():
    total_list = []
    city_name = 'Ramat+Gan+'
    streets = ['Hamelacha', 'Anne+Frank+']
    streets_numbers = [3, 3]
    # streets = ['Hamelacha', 'Anne+Frank+', 'Yeda+Am+', 'Brurya', 'Yehudit', 'Charusim']
    # streets_numbers = [16, 30, 21, 5, 13, 14]
    print("create all addresses from google api")
    index = 0
    for i in range(0, len(streets)):
        total_list.append(googleAPI_handler.get_cords_by_full_address(city_name, streets[i], streets_numbers[i]))
    print("insert all sensors to our db")
    sumlist = sum(streets_numbers)
    fake_date = datetime.datetime.strptime("2018-06-07", "%Y-%m-%d")
    for day_index in range(1, 366):
        data = np.random.normal(15, 2, 100)
        index = 1
        count_id = 1000
        for street in total_list:
            for house in street:
                #resp = requests.get('http://localhost:5000/get_sensor_by_id/1000')
                mydict_date['id'] = str(count_id)
                mydict_date['address'] = house['full_address']
                mydict_date['capacity'] = random.randint(1, 100)
                randnumber = random.randint(0, 10)
                if randnumber > 8:
                    mydict_date['status'] = 'online'
                else:
                    mydict_date['status'] = 'offline'
                mydict_date['lat'] = float(house['lat'])
                mydict_date['lng'] = float(house['lng'])
                mydict_date['data'] = fake_date
                #response = requests.post(url, data=json.dumps(mydict), headers=headers)
                #print(str(index) + " of : " + str(sumlist))
                index = index + 1
                count_id = count_id + 1
                print("sensor id: " + mydict_date['id'] + "date insered: " + str(mydict_date['data']))
        fake_date = fake_date + datetime.timedelta(days=1)


def get_random_normal_array():
    mu, sigma = 15, 2  # mean and standard deviation
    YEARS = 5
    DAYS = 365
    data = np.random.normal(mu, sigma, 100)
    return data
    # for x in data:
    #     print(x)
    # datelist = pd.date_range(end=pd.datetime.today(), periods=DAYS * YEARS).tolist()  # 5 years before until today
    # df = pd.DataFrame(data, index=datelist)
    # print (df)


#init_sensor_for_capacity_0()
#inc_sensor_capacity_for_statistics()
#inc_sensor_capacity_for_statistics()
#inc_sensor_capacity_for_statistics()
#dec_sensor_capacity_for_statistics()
#init_db_with_data_date()
inc_sensor_capacity_for_statistics()
#text_numpy()