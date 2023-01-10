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

st.title("Amtrak Train Tracker")
number = st.number_input('Train Number:', value = 715, step = 1)

url = "https://api.amtraker.com/v1/trains/" + str(number)

response = requests.get(url)

data = json.loads(response.text)
latitude = data[0]['lat']
trainCount = len(data)


routeName = data[0]['routeName']
if(trainCount == 1):
    st.write("There is 1 train on the " + routeName + " route.")
else:
    st.write("There are " + str(trainCount) + " trains on the " + routeName + " route.")

for i in range(trainCount):
    latitude = data[i]['lat']
    longitude = data[i]['lon']
    routeName = data[i]['routeName']
    heading = data[i]['heading']
    velocity = data[i]['velocity']
    lastValTS = data[i]['lastValTS']
    trainTimely = data[i]['trainTimely']
    serviceDisruption = data[i]['serviceDisruption']
    stationCount = len(data[i]['stations'])
    
    st.write("Train " + str(i+1) + " is at " + str(latitude) + ", " + str(longitude) + ".")
    m  = folium.Map(location=[latitude, longitude], zoom_start=10)
    folium.Marker([latitude, longitude], popup='Train Location',).add_to(m)
    st_data = stf(m, height=500, width=1000)







# df = pd.DataFrame(data)
# df = df[['lat', 'lon', 'routeName', 'heading', 'velocity', 'lastValTS', 'trainTimely', 'serviceDisruption']]
# df = df.rename(columns = {'lat': 'Latitude', 'lon': 'Longitude', 'routeName': 'Route Name', 'heading': 'Heading', 'velocity': 'Velocity', 'lastValTS': 'Last Value Timestamp', 'trainTimely': 'Train Timely', 'serviceDisruption': 'Service Disruption'})
# df = df.transpose()
# df.index.name = 'Data'
# df.columns = ['Train Data']
# df = df.reset_index()
# df = df.rename(columns = {'index': 'Data'})
# df = df.set_index('Data')
# df = df.replace({True: 'Yes', False: 'No'})







# st.write(df)


# st.table(df)


# st.write(data)
