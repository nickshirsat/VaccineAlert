#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
import json
from pprint import pprint
from datetime import datetime,time, timedelta
import time as sleep
import sys
from configparser import ConfigParser
from requests.auth import HTTPBasicAuth
from urllib.parse import quote_plus


# In[2]:


def getStateId(name):
    global hitCount
    s_id = 21
    try:
        url = "https://cdn-api.co-vin.in/api/v2/admin/location/states"
        headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"}
        response = requests.get(url, headers=headers)
#         pprint(response)
        hitCount += 1
        response = response.content.decode()
#         pprint(response)
        jsonData = json.loads(response)
        # print(jsonData)
        for state in jsonData['states']:
            if (state['state_name'].upper() == name.upper()):
                s_id = state['state_id']
    except:
        print(sys.exc_info())
    return s_id


# In[3]:


def getDistrictId(s_name,d_name):
    global hitCount
    s_id = getStateId(s_name);
    d_id = "";
    
    try:
        url = "https://cdn-api.co-vin.in/api/v2/admin/location/districts/"+str(s_id)
        headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"}
        response = requests.get(url, headers=headers)
#         pprint(response)
        hitCount += 1
        response = response.content.decode()
       
        jsonData = json.loads(response)
#         pprint(jsonData)
        for d in d_name:
            for district in jsonData['districts']:
                if (district['district_name'].upper() == d.upper()):
                    if(d_id == ""):
                        d_id += str(district['district_id'])
                    else:
                        d_id += "," + str(district['district_id'])
        print(d_id)
        configur['data']['d_ids'] =  d_id
        with open('config.ini', 'w') as configfile:
            configur.write(configfile)
    except Exception as e:
        print(e)
        print(sys.exc_info())
    return


# In[4]:


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

global hitCount
hitCount = 0

#District data

state = configur.get('data', 'state')
districts = json.loads(configur.get('data', 'districts'))

getDistrictId(state,districts)
d_ids = configur.get('data', 'd_ids')
d_ids = d_ids.split(",")
# print(d_ids)


# In[5]:


def sendMsg(place,name,address,pin,vaccine,v_count,f_dose, s_dose, age, fee, date):
    global bot_chatID
    if(place == "389"): #NashikDistrictCode
        bot_chatID = chatIdNskDistrict
    elif(place == "363"): #PuneDistrictCode
        bot_chatID = chatIdPuneDistrict

    msg = "ALERT! Slot available!\nName: " + str(name) + "\nAddress : " + str(address) + "\nVaccine : " + str(vaccine) + " : " + str(fee) + "\nAge : " + str(age) + "+" + "\n\nPincode : " + str(pin)+ "\nDate : " + str(date) + "\nTotal Slots : " + str(v_count) + "\n1st Dose slots : " + str(f_dose) + "\n2nd Dose slots : " + str(s_dose)
    msg = format(quote_plus(msg))
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&text=' + msg
    
    response = requests.get(send_text)
    return response.json()


# In[15]:


def checkSlotsByDistrict():
    global hitCount

    ids = d_ids
#     print(ids)
    
    for d_id in ids: 
#         print(d_id)
        
        try:
            today = datetime.now().date()
#             print(today)
            today = today.strftime('%d-%m-%Y');
            url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id="+str(d_id)+"&date="+str(today)
#             print(url)
            headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"}
            response = requests.get(url, headers=headers)
            hitCount += 1
            response = response.content.decode()
#             pprint(response)
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
                            print(center['center_id'], entry_list)
#                             return
                            if center['center_id'] in entry_list:
                                print("pass")
                                pass
                            else:
                                print("Slot Available!")
                                print(d_id,centerName,address,pin,sessions['vaccine'],sessions['available_capacity'], sessions['available_capacity_dose1'], sessions['available_capacity_dose2'], sessions['min_age_limit'], fee, sessions['date'])
                                entry_list.append(center['center_id'])
                                sendMsg(d_id,centerName,address,pin,sessions['vaccine'],sessions['available_capacity'], sessions['available_capacity_dose1'], sessions['available_capacity_dose2'], sessions['min_age_limit'], fee, sessions['date'])

            sleep.sleep(5)
        except Exception as e:
            print(e)
        


# In[16]:


done = False
i = 1
entry_list = []
while not done:
    
#     hitCount = 0
#     print(hitCount)
    start = sleep.time()
    now = datetime.now().time()
    
    #By District
    checkSlotsByDistrict()

    
    print("loop : " + str(i) + " Time : " + str(now))
    i += 1
    print(entry_list)
    sleep.sleep(10)
    
    if(i%30 == 0):
        # 10 mins
        #list cleared
        print("list cleared")
        entry_list = []
        end = sleep.time()
        total = end-start
        print("Total time in seconds is : " + str(total))

#     print(hitCount)


# In[ ]:




