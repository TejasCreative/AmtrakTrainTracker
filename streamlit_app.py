"""
# Amtrak Train Tracker
This is a lightweight app that tracks Amtrak trains in real time.
"""


import streamlit as st
import requests
import json



st.title("Amtrak Train Tracker")
number = st.number_input('Train Number:', value = 715, step = 1)

url = "https://api.amtraker.com/v1/trains/" + str(number)

response = requests.get(url)
st.write(response)
