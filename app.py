import streamlit as st
import pandas as pd
import requests
import datetime


'''
# Luca model
'''

#st.map(latitude=40.7, longitude=-74, zoom=20)

st.markdown('insert taxi journey parameters')
date = st.date_input('insert date ex. 2013-07-06',datetime.date(2013, 7, 6))

time = st.time_input('insert time format ex.17:18:00', datetime.time(17, 18))
date_time = datetime.datetime.combine(date,time)
dt = date_time.strftime("%Y-%m-%d %H:%M:%S")


pickup_longitude = st.number_input('insert pickup longitude ex. 40.783282')
pickup_latitude = st.number_input('insert pickup latitude ex. -73.950655')
dropoff_longitude = st.number_input('insert dropoff longitude ex. 40.769802')
dropoff_latitude = st.number_input('insert dropoff latitude ex. -73.984365')
passenger_count = st.number_input('insert passenger count ex. 1')

#st.write('https://taxifare.lewagon.ai/predict?pickup_datetime=2014-07-06+19:18:00&pickup_longitude=-73.950655&pickup_latitude=40.783282&dropoff_longitude=-73.984365&dropoff_latitude=40.769802&passenger_count=2')

params = {
    'pickup_datetime' : dt,
    'pickup_longitude' : pickup_longitude,
    'pickup_latitude' : pickup_latitude,
    'dropoff_longitude' : dropoff_longitude,
    'dropoff_latitude' : dropoff_latitude,
    'passenger_count' : int(passenger_count)
}

# st.write(params)

url = 'https://taxifare.lewagon.ai/predict'

# req = PreparedRequest()
# req.prepare_url(url, params)

# st.markdown('URL complète :')
# st.write(req.url)


response = requests.get(url, params = params)
res = response.json()

st.markdown('REPONSE : taxi fare :')
if response.status_code == 200 :
    st.write("taxi fare :",res['fare'])


# def get_map_data():

#     return pd.DataFrame(
#             np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
#             columns=['lat', 'lon']
#         )



# df = get_map_data()
# st.write(df)



# '''
# # TaxiFareModel front
# '''

# st.markdown('''
# Remember that there are several ways to output content into your web page...

# Either as with the title by just creating a string (or an f-string). Or as with this paragraph using the `st.` functions
# ''')

# '''
# ## Here we would like to add some controllers in order to ask the user to select the parameters of the ride

# 1. Let's ask for:
# - date and time
# - pickup longitude
# - pickup latitude
# - dropoff longitude
# - dropoff latitude
# - passenger count
# '''

# '''
# ## Once we have these, let's call our API in order to retrieve a prediction

# See ? No need to load a `model.joblib` file in this app, we do not even need to know anything about Data Science in order to retrieve a prediction...

# 🤔 How could we call our API ? Off course... The `requests` package 💡
# '''

# url = 'https://taxifare.lewagon.ai/predict'

# requests.get(url)

# if url == 'https://taxifare.lewagon.ai/predict':

#     st.markdown('Maybe you want to use your own API for the prediction, not the one provided by Le Wagon...')

# '''

# 2. Let's build a dictionary containing the parameters for our API...

# 3. Let's call our API using the `requests` package...

# 4. Let's retrieve the prediction from the **JSON** returned by the API...

# ## Finally, we can display the prediction to the user
# '''
