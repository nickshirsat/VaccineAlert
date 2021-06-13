#!/usr/bin/env python
# coding: utf-8

# In[8]:


import requests
import json
from pprint import pprint
from datetime import datetime,time, timedelta
from datetime import timedelta
import time as sleep
import sys
from configparser import ConfigParser
from requests.auth import HTTPBasicAuth
from urllib.parse import quote_plus


# In[9]:


configur = ConfigParser() 
configur.read('config.ini')

# Telegram setup
bot_token = configur.get('telegram', 'bot_token')

# Telegram setup Pune
# Pune City
#chatIdPuneCity = configur.get('telegram', 'PuneCity')

# Telegram setup Nashik Group
# Nashik City
chatIdNskCity = configur.get('telegram', 'nashikdistrict18')

pincodeNashik = json.loads(configur.get('data', 'pincodenashik18'))
# pincodePune = json.loads(configur.get('data', 'pincodePune'))
pincodes = [pincodeNashik]
# pinCity = json.loads(configur.get('data', 'pinCity'))
pinCity = ['NashikCity']
global hitCount
hitCount = 0


# In[10]:


def sendMsg(place,name,address,pin,vaccine,v_count,f_dose, s_dose, age, fee, date):
    try:
        # if(place.upper() == "NashikCity".upper()):
        #     bot_chatID = chatIdNskCity
        # elif(place.upper() == "PuneCity".upper()):
        #     bot_chatID = chatIdPuneCity
        bot_chatID = chatIdNskCity
        msg = "ALERT! Slot available!\nName: " + str(name) + "\nAddress : " + str(address) + "\nVaccine : " + str(vaccine) + " : " + str(fee) + "\n\nAge : " + str(age) + "+" + "\nPincode : " + str(pin)+ "\nDate : " + str(date) + "\nTotal Slots : " + str(v_count) + "\n1st Dose slots : " + str(f_dose) + "\n2nd Dose slots : " + str(s_dose)
        msg = format(quote_plus(msg))
        send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&text=' + msg
        # print(send_text)
        response = requests.get(send_text)
        return response.json()
    except:
#         pass
        print(sys.exc_info())


# In[11]:


def checkSlotsByPin(pincodes):
    global hitCount
    global dateFlag
    # print(dateFlag)
    
#     print(hitCount)
    i = 0
    # print(pincodes)
    for pincode in pincodes:
        for pin in pincode:
            try:
                print(pin)
                if(dateFlag):
                    today = datetime.now().date() + timedelta(1)
    #                 print(today)
                else:
                    today = datetime.now().date()
                today = today.strftime('%d-%m-%Y')
                if(i == 0):
                    print(today)
                url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode="+str(pin)+"&date="+str(today)

                headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"}
                response = requests.get(url, headers=headers)
                print(response)
#                 print(hitCount)
                hitCount += 1
                response = response.content.decode()
#                 print(response)

                jsonData = json.loads(response)
                jsonData = jsonData['centers']
#                 pprint(jsonData)
                for center in jsonData:
                    centerName = center['name']
                    address = center['address']
                    pin = center['pincode']
                    fee = center['fee_type']
                    for sessions in center['sessions']:
#                         print(sessions)
                        if (today == sessions['date']):
                            if(sessions['available_capacity'] > 0):
                                if(sessions['min_age_limit'] == 18):
                                    if(sessions['available_capacity_dose1'] > 0):
                                        if center['center_id'] in entry_list:
                                            pass
                                        else:
                                            print("Slot Available!")
                                            entry_list.append(center['center_id'])
                                            sendMsg(pinCity[i],centerName,address,pin,sessions['vaccine'],sessions['available_capacity'], sessions['available_capacity_dose1'], sessions['available_capacity_dose2'], sessions['min_age_limit'], fee, sessions['date'])
                                            print(pinCity[i],centerName,address,pin,sessions['vaccine'],sessions['available_capacity'], sessions['available_capacity_dose1'], sessions['available_capacity_dose2'], sessions['min_age_limit'], fee, sessions['date'])
            
            except:
                pass
            sleep.sleep(0.3)
#                 print(sys.exc_info())
#         print(i)
            i += 1


# In[ ]:


done = False
i = 1
entry_list = []
dateFlag = False
loop2 = 0
while not done:
    
    hitCount = 0
    print(hitCount)
    now = datetime.now().time()
    
    
    #By Pin
    checkSlotsByPin(pincodes)
    
    # print(dateFlag)
    dateFlag = not dateFlag
    
    print("loop : " + str(i) + " Time : " + str(now))
    i += 1
    loop2 += 1
    print(entry_list)
    if(loop2%2 == 0):
        loop2 = 0
        sleep.sleep(180)
    if(i%3 == 0):
        # ~10 mins
        #list cleared
        entry_list = []
    print(hitCount)


# In[ ]:




