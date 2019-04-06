import requests
import csv
import configuration
import json


def get_cords_by_full_address(city_name, street_name, max_number):
    address_list = []
    json_list = []
    for x in range(1, max_number+1):
        temp_json = {'full_address': None, 'lat': None, 'lng': None}
        temp_string = []
        Full_API_Request = 'https://maps.googleapis.com/maps/api/geocode/json?address=' + city_name + str(x) + ',' + street_name + configuration.google_api_token
        response = requests.get(Full_API_Request)
        resp_json_payload = response.json()
        temp_json['full_address'] = resp_json_payload['results'][0]['formatted_address']
        temp_json['lat'] = resp_json_payload['results'][0]['geometry']['location']['lat']
        temp_json['lng'] = resp_json_payload['results'][0]['geometry']['location']['lng']
        #json_list.
        #temp_string.append(resp_json_payload['results'][0]['formatted_address'])
        #temp_string.append(resp_json_payload['results'][0]['geometry']['location']['lat'])
        #temp_string.append(resp_json_payload['results'][0]['geometry']['location']['lng'])
        #address_list.append(temp_string)
        address_list.append(temp_json)
    return address_list

def write_list_to_csv_file(address_list):
    with open("C:\\Users\\talha\\TrashWise\\Export_data_3.csv", 'w') as resultFile:
        for row in address_list:
            wr = csv.writer(resultFile, dialect='excel')
            wr.writerows(row)
            #for cell in row:

def write_list_to_json_file(address_list):
    for x in address_list:
        with open('address_data.json', 'w') as outfile:
            json.dump(x, outfile)

def write_to_json_file(json_data):
    with open('address_data_1.json', 'w') as outfile:
        json.dump(json_data, outfile)

total_list = []
city_name = 'Ramat+Gan+'

street_name = 'Hamelacha'
max_number = 16

street_name1 = 'Anne+Frank+'
max_1 = 30

street_name2 = 'Yeda+Am+'
max_2 = 21

street_name3 = 'Brurya'
max_3 = 5

street_name4 = 'Yehudit'
max_4 = 13

street_name5 = 'Charusim'
max_5 = 14



pass
#total_list.append(get_cords_by_full_address(city_name, street_name, max_number))
pass
#write_list_to_json_file(total_list)
#zzz = get_cords_by_full_address(city_name, street_name, max_number)
#write_to_json_file(zzz)
pass
#total_list.append(get_cords_by_full_address(city_name, street_name1, max_number1))
#total_list.append(get_cords_by_full_address(city_name, street_name2, max_number2))
#write_list_to_json_file(total_list)

#write_list_to_csv_file(total_list)

