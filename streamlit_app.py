from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st
import requests
from pprint import pprint
import json

"""
# JustTheWeather
## Because you just want the weather. 
"""
st.image("sun2.jpg", width=250)
st.write("What is your five digit zip code?")
st.write("If you do not know, visit this link to find out: https://www.whatismyzip.com/")
symbol = st.text_input("", "10001")
