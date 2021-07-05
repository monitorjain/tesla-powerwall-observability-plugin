import requests
import pprint
import json
from requests.models import CaseInsensitiveDict
import schedule 
import time
from datetime import datetime
import datetime

while True:

### variables
    city_name = ''
    percentage_charged = 0
    energy_left = 0
    weather_desc = ''

###### CITY WEATHER POLL SECTION ############
    weather_token = "ababxbabsabasbdabdabda" # create your own token on openweathermap or other similar weather sites 
    city_name = "add your city name" # replace the text string with your city name 

    query = {'q':'City,State,CountryCode', 'appid':'ababxbabsabasbdabdabda'} # replace with your city, state, appID on OpenWeather and country code
    resp2 = requests.get('https://api.openweathermap.org/data/2.5/weather', params=query)
    data1 = resp2.json()

    #pprint.pprint(data1)

    dat = json.dumps(data1)
    dat2 = json.loads(dat)

    weather_desc = dat2['weather'][0]['description']
    #print(weather_desc)

    ###### CITY WEATHER POLL SECTION END ############

    ###### TESLA POWERWALL OR CAR AUTHORIZATION AND DATA FETCH SECTION ############

    url = "https://owner-api.teslamotors.com/api/1/products" # if you want to monitor Tesla car instead, you will need to change this section

    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"
    headers["Authorization"] = "Bearer qts-ababxbabsabasbdabdabda" # generate this token on iOS and Android AuthAppForTesla

    resp = requests.get(url, headers=headers)

        #print(resp.status_code)

    data = resp.json()

    #pprint.pprint(data)

    data = json.dumps(data)
    data2 = json.loads(data)

    battery_id = data2['response'][0]['id']
    total_energy = data2['response'][0]['total_pack_energy']

    #print(battery_id)
    #print(total_energy)

    ###### TESLA POWERWALL OR CAR AUTHORIZATION AND DATA FETCH SECTION ############

    ####### BATTERY STATUS SECTION ##########

    url = "https://owner-api.teslamotors.com/api/1/powerwalls/"+battery_id+"/status"

    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"
    headers["Authorization"] = "Bearer qts-ababxbabsabasbdabdabda" # generate this token on iOS and Android AuthAppForTesla

    resp3 = requests.get(url, headers=headers)
    resp3 = resp3.json()

    energy_left = resp3['response']['energy_left']
    percentage_charged = resp3['response']['percentage_charged']

    #print(energy_left)
    #print(percentage_charged)


        ####### BATTERY STATUS SECTION END ##########

        ####### BATTERY DATA FETCH SECTION ##########   

    url = "https://owner-api.teslamotors.com/api/1/powerwalls/"+battery_id

    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"
    
    headers["Authorization"] = "Bearer qts-ababxbabsabasbdabdabda" # generate this token on iOS and Android AuthAppForTesla
    
    resp4 = requests.get(url, headers=headers)
    resp4 = resp4.json()

    #pprint.pprint(resp4)
    #resp4['response']['power_reading']
    load_power = resp4['response']['power_reading'][0]['load_power']
    grid_power = resp4['response']['power_reading'][0]['grid_power']
    generator_power = resp4['response']['power_reading'][0]['generator_power']
    battery_power = resp4['response']['power_reading'][0]['battery_power']

    if(load_power == 0):
        system_down = 1
    else:
        system_down = 0

    if(grid_power == 0 & battery_power == 0):
        system_down = 1
    else:
        system_down = 0

    if(battery_power == 0):
        grid_used = 1
        battery_used = 0
    else:
        grid_used = 0
        battery_used = 1  
    
    print(system_down)
    print(battery_used)
    print(grid_used)

    #energy_left = resp3['response']['energy_left']
    #percentage_charged = resp3['response']['percentage_charged']

    #print(energy_left)
    #print(percentage_charged)

        ####### BATTERY TIME SERIES DATA FETCH SECTION END ##########

        ####### POST metric via DT Metric API ##########
    def remove(string):
        return "".join(string.split())

    dt_metric_data = 'energy_left,battery_id='+str(battery_id)+',city='+city_name+',weather='+remove(weather_desc)+',percentage_left='+str(percentage_charged)+' '+str(energy_left)+''


    dt_metric_data2 = 'total_energy,battery_id='+str(battery_id)+',city='+city_name+',weather='+remove(weather_desc)+',percentage_left='+str(percentage_charged)+' '+str(total_energy)+''

    dt_metric_data3 = 'system_down,battery_id='+str(battery_id)+',city='+city_name+',weather='+remove(weather_desc)+',percentage_left='+str(percentage_charged)+' '+str(system_down)+''

    dt_metric_data4 = 'grid_used,battery_id='+str(battery_id)+',city='+city_name+',weather='+remove(weather_desc)+',percentage_left='+str(percentage_charged)+' '+str(grid_used)+''

    dt_metric_data5 = 'battery_used,battery_id='+str(battery_id)+',city='+city_name+',weather='+remove(weather_desc)+',percentage_left='+str(percentage_charged)+' '+str(battery_used)+''

    dt_metric_data6 = 'load_power,battery_id='+str(battery_id)+',city='+city_name+',weather='+remove(weather_desc)+',percentage_left='+str(percentage_charged)+' '+str(load_power)+''

    dt_metric_data7 = 'grid_power,battery_id='+str(battery_id)+',city='+city_name+',weather='+remove(weather_desc)+',percentage_left='+str(percentage_charged)+' '+str(grid_power)+''

    dt_metric_data8 = 'generator_power,battery_id='+str(battery_id)+',city='+city_name+',weather='+remove(weather_desc)+',percentage_left='+str(percentage_charged)+' '+str(generator_power)+''

    dt_metric_data9 = 'battery_power,battery_id='+str(battery_id)+',city='+city_name+',weather='+remove(weather_desc)+',percentage_left='+str(percentage_charged)+' '+str(battery_power)+''
    print(dt_metric_data4)
    print(dt_metric_data3)
    
 

    headers = {
        'Authorization': 'Api-Token dt0c01.aasxdasfafaassf', #API Token generated in Dynatrace or similar Observability platform for metrics ingestion
        'Content-Type': 'text/plain',
    }

    # adjust this section if not using Dynatrace as an Observability solution
    
    metric1 = dt_metric_data
    metric2 = dt_metric_data2
    metric3 = dt_metric_data3
    metric4 = dt_metric_data4
    metric5 = dt_metric_data5
    metric6 = dt_metric_data6
    metric7 = dt_metric_data7
    metric8 = dt_metric_data8
    metric9 = dt_metric_data9

    response1 = requests.post('https://nfu29200.live.dynatrace.com/api/v2/metrics/ingest', headers=headers, data=metric1)
    response2 = requests.post('https://nfu29200.live.dynatrace.com/api/v2/metrics/ingest', headers=headers, data=metric2)
    response3 = requests.post('https://nfu29200.live.dynatrace.com/api/v2/metrics/ingest', headers=headers, data=metric3)
    response4 = requests.post('https://nfu29200.live.dynatrace.com/api/v2/metrics/ingest', headers=headers, data=metric4)
    response5 = requests.post('https://nfu29200.live.dynatrace.com/api/v2/metrics/ingest', headers=headers, data=metric5)
    response6 = requests.post('https://nfu29200.live.dynatrace.com/api/v2/metrics/ingest', headers=headers, data=metric6)
    response7 = requests.post('https://nfu29200.live.dynatrace.com/api/v2/metrics/ingest', headers=headers, data=metric7)
    response8 = requests.post('https://nfu29200.live.dynatrace.com/api/v2/metrics/ingest', headers=headers, data=metric8)
    response9 = requests.post('https://nfu29200.live.dynatrace.com/api/v2/metrics/ingest', headers=headers, data=metric9)

    resp5 = response1.json()
    resp6 = response9.json()

    print(resp5)
    print(resp6)

    time.sleep(300) # 5 mins delay in sending the next stream of metrics, adjust as per required resolution.

