#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
import json
from pprint import pprint
from datetime import datetime,time
import time as sleep
import sys
from configparser import ConfigParser
from requests.auth import HTTPBasicAuth
from urllib.parse import quote_plus


# In[2]:


configur = ConfigParser() 
configur.read('config.ini')

# Telegram setup
bot_token = configur.get('telegram', 'bot_token')

# Telegram setup Pune
# Pune City
chatIdPuneCity = configur.get('telegram', 'PuneCity')

# Telegram setup Nashik Group
# Nashik City
chatIdNskCity = configur.get('telegram', 'NashikCity')

pincodeNashik = json.loads(configur.get('data', 'pincodeNashik'))
pincodePune = json.loads(configur.get('data', 'pincodePune'))
pincodes = [pincodeNashik] + [pincodePune]
pinCity = json.loads(configur.get('data', 'pinCity'))
global hitCount
hitCount = 0


# In[3]:


def sendMsg(place,name,address,pin,vaccine,v_count,age,fee):
    if(place.upper() == "NashikCity".upper()):
        bot_chatID = chatIdNskCity
    elif(place.upper() == "PuneCity".upper()):
        bot_chatID = chatIdPuneCity

    msg = "ALERT! Slot available!\nName: " + str(name) + "\nAddress : " + str(address) + "\nPincode : " + str(pin) + "\nVaccine : " + str(vaccine) + " : " + str(fee) + "\nAge : " + str(age) + "+" + "\nTotal Slots : " + str(v_count)
    msg = format(quote_plus(msg))
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&text=' + msg
#     print(send_text)
    response = requests.get(send_text)
    return response.json()


# In[6]:


def checkSlotsByPin(pincodes):
    global hitCount
#     print(hitCount)
    i = 0
    for pincode in pincodes:
        for pin in pincode:
            sleep.sleep(1)
            try:
                today = datetime.now().date().strftime('%d-%m-%Y');
                url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/calendarByPin?pincode="+str(pin)+"&date="+str(today)

                headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"}
                response = requests.get(url, headers=headers)
                # print(response)
                # print(hitCount)
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
                                    sendMsg(pinCity[i],centerName,address,pin,sessions['vaccine'],sessions['available_capacity'],sessions['min_age_limit'],fee)
            except:
                pass
#                 print(sys.exc_info())
            i += 1


# In[7]:


done = False
i = 1
entry_list = []
while not done:
    
    hitCount = 0
    print(hitCount)
    now = datetime.now().time()
    
    if(now > time(7,00) and now < time(23,00)):
        
        #By Pin
        checkSlotsByPin(pincodes)
        
        print("loop : " + str(i) + " Time : " + str(now))
        i += 1
        print(entry_list)
        sleep.sleep(10)
        if(i%120 == 0):
            #list cleared
            entry_list = []
    else:
        done = True
    print(hitCount)


# In[ ]:





# In[ ]:




