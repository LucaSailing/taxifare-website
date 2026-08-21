import streamlit as st
import requests
import datetime
import folium
from streamlit_folium import st_folium

'''
# Luca's taxi
'''

NY_CENTER = [40.7128, -74.0060]

# Mémoire de session pour garder les points entre les reruns
for key in ('pickup', 'dropoff', 'last_click'):
    st.session_state.setdefault(key, None)

st.markdown('### 1. Choisis le départ et l\'arrivée sur la carte')

point_type = st.radio(
    'Point à placer au prochain clic',
    ['Départ (pickup)', 'Arrivée (dropoff)'],
    horizontal=True
)

# Construction de la carte + marqueurs déjà posés
m = folium.Map(location=NY_CENTER, zoom_start=12)
if st.session_state.pickup:
    folium.Marker(st.session_state.pickup, tooltip='Départ',
                  icon=folium.Icon(color='green')).add_to(m)
if st.session_state.dropoff:
    folium.Marker(st.session_state.dropoff, tooltip='Arrivée',
                  icon=folium.Icon(color='red')).add_to(m)
if st.session_state.pickup and st.session_state.dropoff:
    folium.PolyLine([st.session_state.pickup, st.session_state.dropoff],
                    color='blue', weight=2).add_to(m)

map_data = st_folium(m, height=400, width=700)

# Capture du clic (une seule fois par clic grâce à last_click)
if map_data and map_data.get('last_clicked'):
    click = (map_data['last_clicked']['lat'], map_data['last_clicked']['lng'])
    if click != st.session_state.last_click:
        st.session_state.last_click = click
        if point_type.startswith('Départ'):
            st.session_state.pickup = list(click)
        else:
            st.session_state.dropoff = list(click)
        st.rerun()

col1, col2 = st.columns(2)
col1.write(f"Départ : {st.session_state.pickup}")
col2.write(f"Arrivée : {st.session_state.dropoff}")

if st.button('Réinitialiser les points'):
    st.session_state.pickup = None
    st.session_state.dropoff = None
    st.session_state.last_click = None
    st.rerun()

st.markdown('### 2. Date, heure et passagers')
columns = st.columns(2)
date = columns[0].date_input('Date', datetime.date(2013, 7, 6))
time = columns[1].time_input('Heure', datetime.time(17, 18))
dt = datetime.datetime.combine(date, time).strftime("%Y-%m-%d %H:%M:%S")
passenger_count = st.number_input('Nombre de passagers', min_value=1, value=1)

st.markdown('### 3. Prédiction')

if st.session_state.pickup and st.session_state.dropoff:
    params = {
        'pickup_datetime': dt,
        'pickup_longitude': st.session_state.pickup[1],
        'pickup_latitude': st.session_state.pickup[0],
        'dropoff_longitude': st.session_state.dropoff[1],
        'dropoff_latitude': st.session_state.dropoff[0],
        'passenger_count': int(passenger_count)
    }
    response = requests.get('https://taxifare.lewagon.ai/predict', params=params)
    if response.status_code == 200:
        fare = response.json()['fare']
        st.write(f"Prix estimé : **{round(fare, 2)} $**")
    else:
        st.error(f"Erreur API ({response.status_code})")
else:
    st.info('Place un point de départ et un point d\'arrivée sur la carte.')
