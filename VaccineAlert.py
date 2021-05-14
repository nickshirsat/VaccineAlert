#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import requests
import json
from pprint import pprint
from datetime import datetime,time
import time as sleep
import sys
from configparser import ConfigParser
from requests.auth import HTTPBasicAuth
from urllib.parse import quote_plus


# In[ ]:


configur = ConfigParser() 
configur.read('config.ini')

# Telegram setup
bot_token = configur.get('telegram', 'bot_token')

# Telegram setup Pune
# Pune District
chatIdPuneDistrict = configur.get('telegram', 'PuneDistrict')

# Telegram setup Nashik Group
# Nashik District
chatIdNskDistrict = configur.get('telegram', 'NashikDistrict')

#District data
state = configur.get('data', 'state')
districts = json.loads(configur.get('data', 'districts'))
global hitCount
hitCount = 0


# In[ ]:


def sendMsg(place,name,address,pin,vaccine,v_count,age,fee):
    if(place == 389): #NashikDistrictCode
        bot_chatID = chatIdNskDistrict
    elif(place == 363): #PuneDistrictCode
        bot_chatID = chatIdPuneDistrict

    msg = "ALERT! Slot available!\nName: " + str(name) + "\nAddress : " + str(address) + "\nPincode : " + str(pin) + "\nVaccine : " + str(vaccine) + " : " + str(fee) + "\nAge : " + str(age) + "+" + "\nTotal Slots : " + str(v_count)
    msg = format(quote_plus(msg))
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&text=' + msg
#     print(send_text)
    response = requests.get(send_text)
    return response.json()


# In[ ]:


def getStateId(name):
    global hitCount
    s_id = 21
    try:
        url = "https://cdn-api.co-vin.in/api/v2/admin/location/states"
        headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"}
        response = requests.get(url, headers=headers)
#         print(response)
        hitCount += 1
        response = response.content.decode()
        jsonData = json.loads(response)
#         print(jsonData)
        for state in jsonData['states']:
            if (state['state_name'].upper() == name.upper()):
                s_id = state['state_id']
    except:
        print(sys.exc_info())
    return s_id


# In[ ]:


def getDistrictId(s_name,d_name):
    global hitCount
    s_id = getStateId(s_name);
    d_id = [];
    
    try:
        url = "https://cdn-api.co-vin.in/api/v2/admin/location/districts/"+str(s_id)
        headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"}
        response = requests.get(url, headers=headers)
        hitCount += 1
        response = response.content.decode()
        jsonData = json.loads(response)
        for d in d_name:
            for district in jsonData['districts']:
                if (district['district_name'].upper() == d.upper()):
                    d_id.append(district['district_id'])
    except:
        print(sys.exc_info())
    return d_id


# In[ ]:


def checkSlotsByDistrict(s_name, d_name):
    global hitCount
    ids = getDistrictId(s_name, d_name)
    for d_id in ids: 
        sleep.sleep(1)
        try:
            today = datetime.now().date() + timedelta(1)
#                 print(today)
            today = today.strftime('%d-%m-%Y');
            url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/calendarByDistrict?district_id="+str(d_id)+"&date="+str(today)

            headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"}
            response = requests.get(url, headers=headers)
            print(response)
            hitCount += 1
            response = response.content.decode()
            jsonData = json.loads(response)
            jsonData = jsonData['centers']

            for center in jsonData:
                centerName = center['name']
                address = center['address']
                pin = center['pincode']
                fee = center['fee_type']
                for sessions in center['sessions']:
                    if (today == sessions['date']):
                        if(sessions['available_capacity'] > 0):
                            if center['center_id'] in entry_list:
                                pass
                            else:
                                print("Slot Available!")
                                print(center['center_id'],centerName,address,sessions['vaccine'],sessions['available_capacity'],sessions['min_age_limit'],fee)
                                entry_list.append(center['center_id'])
                                sendMsg(d_id,centerName,address,pin,sessions['vaccine'],sessions['available_capacity'],sessions['min_age_limit'],fee)
        except:
            pass


# In[ ]:


done = False
i = 1
entry_list = []
while not done:
    
    hitCount = 0
    print(hitCount)
    now = datetime.now().time()
    
    if(now > time(7,00) and now < time(23,59)):
        
        #By District
        checkSlotsByDistrict(state,districts)
    
        
        print("loop : " + str(i) + " Time : " + str(now))
        i += 1
        print(entry_list)
        sleep.sleep(5)
        if(i%120 == 0):
            #list cleared
            entry_list = []
    else:
        done = True
    print(hitCount)


# In[ ]:




