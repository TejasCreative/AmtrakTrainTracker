"""
# Amtrak Train Tracker
This is a lightweight app that tracks Amtrak trains in real time.
"""


import streamlit as st
import requests
import json
import pandas as pd
import numpy as np
from streamlit_folium import st_folium as stf
import folium
from datetime import datetime
import pytz
from dateutil import tz
import time



timezone_storage = {
    -12: "DST(UTC-12)",
    -11: "UTC-11",
    -10: "HST(UTC-10)",
    -9: "AKST(UTC-9)",
    -8: "PST(UTC-8)",
    -7: "MST(UTC-7)",
    -6: "CST(UTC-6)",
    -5: "EST(UTC-5)",
    -4: "PSST(UTC-4)",
    -3: "NST(UTC-3)",
    -2: "UTC-2",
    -1: "AST(UTC-1)",
    0: "UTC",
    1: "CEST(UTC+1)",
    2: "EEST(UTC+2)",
    3: "AST(UTC+3)",
    4: "RST(UTC+4)",
    5: "PST(UTC+5)",
    6: "BST(UTC+6)",
    7: "NCAST(UTC+7)",
    8: "WAST(UTC+8)",
    9: "KST(UTC+9)",
    10: "ACST(UTC+10)",
    11: "VST(UTC+11)",
    12: "FST(UTC+12)",
}


get5 = "https://api.amtraker.com/v1/trains/5"
response5 = requests.get(get5)

data5 = json.loads(response5.text)

lastValTS = data5[0]['lastValTS']
lastValTS = lastValTS[11:19]
local_zone = tz.tzlocal()
local_dt = datetime.strptime(lastValTS, "%H:%M:%S")

from_zone = tz.tzutc()
to_zone = tz.tzlocal()


utc = local_dt.replace(tzinfo=from_zone)
local_dt = utc.astimezone(to_zone)

timezone_calc = (str(local_dt))

timezone_calc = timezone_calc[19:22]
timezone_calc_int = int(timezone_calc)



timezone = timezone_storage[timezone_calc_int]


st.title("Amtrak Train Tracker")
number = st.number_input('Train Number:', value = 715, step = 1)
now = datetime.now()
current_time = now.strftime("%I:%M:%S %p")
st.caption("Currently it is " + current_time + " " + timezone)

url = "https://api.amtraker.com/v1/trains/" + str(number)

response = requests.get(url)



if(response.status_code == 500):
    st.write("There is no train with that number.")
    st.stop()



data = json.loads(response.text)
if(len(data) == 0 ):
    st.write("There is no train running with that number.")
    st.stop()
latitude = data[0]['lat']



trainCount = len(data)


routeName = data[0]['routeName']
if(trainCount == 1):
    st.write("There is 1 train on the " + routeName + " route.")
else:
    st.write("There are " + str(trainCount) + " trains on the " + routeName + " route.")






    



 



for i in range(trainCount):
    st.subheader("Train " + str(i+1) + ":")
    latitude = data[i]['lat']
    longitude = data[i]['lon']
    routeName = data[i]['routeName']
    heading = data[i]['heading']
    velocity = data[i]['velocity']
    lastValTS = data[i]['lastValTS']
    trainTimely = data[i]['trainTimely']
    serviceDisruption = data[i]['serviceDisruption']
    stationCount = len(data[i]['stations'])
    latitudeRounded = round(latitude, 5)
    longitudeRounded = round(longitude, 5)
    trainState = data[i]['trainState']

    # lastValTS = lastValTS[11:23]

    lastValTS = lastValTS[11:19]
    local_zone = tz.tzlocal()
    local_dt = datetime.strptime(lastValTS, "%H:%M:%S")

    from_zone = tz.tzutc()
    to_zone = tz.tzlocal()


    utc = local_dt.replace(tzinfo=from_zone)
    local_dt = utc.astimezone(to_zone)

    timezone_calc = (str(local_dt))

    timezone_calc = timezone_calc[19:22]
    timezone_calc_int = int(timezone_calc)



    timezone = timezone_storage[timezone_calc_int]

    velocityrounded = round(velocity, 2)
    if(trainState != "Completed"):
        st.write("Train " + str(i+1) + " is at Latitude " + str(latitudeRounded) + ", and Longitude " + str(longitudeRounded) + " and is currently heading " + str(heading) + " at " + str(velocityrounded) + " mph.")
    if(trainTimely == "On Time"):
        st.write("This train is running on time.")
    if(trainTimely == "Late"):
        st.write("This train is running late.")
    if(serviceDisruption == True):
        st.write("There is a service disruption on this train.")

    
    local_dt = local_dt.strftime("%I:%M:%S %p")
    lastValTS = local_dt
    
    if(trainState == "Completed"):
        st.write("This train has completed its journey.")
    m  = folium.Map(location=[latitude, longitude], zoom_start=10)
    folium.Marker([latitude, longitude], popup='Train Location',).add_to(m)
    st_data = stf(m, height=500, width=1000)
    st.caption("Last updated at " + lastValTS + " " + timezone + ".")
    first_station = 0
    
    stationinfo = data[i]['stations']

    if(trainState != "Completed"):
        for i in range(stationCount):
            if('stationName' in stationinfo[i]):
                station_Name = stationinfo[i]['stationName']
            else:
                station_Name = stationinfo[i]['code']
            trainline = ""
            trainline = station_Name  + ": "
            if(i == 0):
                if('postDep' not in stationinfo[i]):
                    trainline = trainline + "Scheduled Departure is at " + stationinfo[i]['schDep']
                else:
                    deptiming = stationinfo[i]['postDep']
                    deptiming = deptiming[11:19]
                    deptiming_dt = tz.tzlocal()
                    deptiming_dt = datetime.strptime(deptiming, "%H:%M:%S")
                    deptiming_dt = deptiming_dt.strftime("%I:%M:%S %p")

                    trainline = trainline + "Departed at " + str(deptiming_dt) + ", " + stationinfo[i]['postCmnt'].lower()

            else:
                if('estArr' in stationinfo[i]):
                    deptiming = stationinfo[i]['estArr']
                    deptiming = deptiming[11:19]
                    deptiming_dt = tz.tzlocal()
                    deptiming_dt = datetime.strptime(deptiming, "%H:%M:%S")
                    deptiming_dt = deptiming_dt.strftime("%I:%M:%S %p")
                    trainline = trainline + "Estmiated Arrival is at " + str(deptiming_dt) + ", " + stationinfo[i]['estArrCmnt'].lower()
                elif('estDep' in stationinfo[i]):
                    deptiming = stationinfo[i]['postArr']
                    deptiming = deptiming[11:19]
                    deptiming_dt = tz.tzlocal()
                    deptiming_dt = datetime.strptime(deptiming, "%H:%M:%S")
                    deptiming_dt = deptiming_dt.strftime("%I:%M:%S %p")

                    v_deptiming = stationinfo[i]['postArr']
                    v_deptiming = deptiming[11:19]
                    v_deptiming_dt = tz.tzlocal()
                    v_deptiming_dt = datetime.strptime(v_deptiming, "%H:%M:%S")
                    v_deptiming_dt = v_deptiming_dt.strftime("%I:%M:%S %p")


                    trainline = trainline + "Arrived at " + str(deptiming_dt) + " and estmiated departure is at " + str(v_deptiming_dt) + ', ' + stationinfo[i]['estDepCmnt'].lower()
                elif('postDep' in stationinfo[i]):
                    deptiming = stationinfo[i]['postDep']
                    deptiming = deptiming[11:19]
                    deptiming_dt = tz.tzlocal()
                    deptiming_dt = datetime.strptime(deptiming, "%H:%M:%S")
                    deptiming_dt = deptiming_dt.strftime("%I:%M:%S %p")
                    trainline = trainline + "Departed at " + str(deptiming_dt) + ", " + stationinfo[i]['postCmnt'].lower()
                else:
                    trainline = trainline + "No Data"







            st.write(trainline)
