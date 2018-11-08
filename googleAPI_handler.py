import requests
import csv
import configuration

def get_cords_by_full_address(city_name, street_name, max_number):
    address_list = []
    for x in range(1, max_number+1):
        temp_string = []
        Full_API_Request = 'https://maps.googleapis.com/maps/api/geocode/json?address=' + city_name + str(x) + ',' + street_name + configuration.google_api_token
        response = requests.get(Full_API_Request)
        resp_json_payload = response.json()
        temp_string.append(resp_json_payload['results'][0]['formatted_address'])
        temp_string.append(resp_json_payload['results'][0]['geometry']['location']['lat'])
        temp_string.append(resp_json_payload['results'][0]['geometry']['location']['lng'])
        address_list.append(temp_string)
    return address_list

def write_list_to_csv_file(address_list):
    with open("C:\\Users\\talha\\TrashWise\\Export_data_3.csv", 'w') as resultFile:
        for row in address_list:
            wr = csv.writer(resultFile, dialect='excel')
            wr.writerows(row)
            #for cell in row:



total_list = []
city_name = 'Ramat+Gan+'

street_name = 'Hamelacha'
max_number = 16

street_name1 = 'Anne+Frank+'
max_number1 = 30

street_name2 = 'Yeda+Am+'
max_number2 = 21


#total_list.append(get_cords_by_full_address(city_name, street_name, max_number))
#total_list.append(get_cords_by_full_address(city_name, street_name1, max_number1))
#total_list.append(get_cords_by_full_address(city_name, street_name2, max_number2))

#write_list_to_csv_file(total_list)

