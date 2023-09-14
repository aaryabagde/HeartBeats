import requests
import urllib.request as urllib2
import neurokit2 as nk
import numpy as np
import pickle
READ_API_KEY = '8SVJWFROR7BY9Z4P'
CHANNEL_ID = 2095762

# Set the number of readings to retrieve
num_readings = 200
model_a = pickle.load(open('dt_arousal.sav', 'rb'))
model_v = pickle.load(open('dt_valence.sav', 'rb'))


def get_emotion():
    # Build the URL for the ThingSpeak API
    url = f"https://api.thingspeak.com/channels/{CHANNEL_ID}/feeds.json?api_key={READ_API_KEY}&results={num_readings}"

    # Make a GET request to the URL
    response = requests.get(url)
    # Get the JSON data from the response
    data = response.json()
    # Extract the field values from the data and store them as a list
    readings = []
    for feed in data["feeds"]:
        readings.append(float(feed["field1"]))
    # Print the list of readings
    # print(readings)
    # Find peaks
    peaks, info = nk.ecg_peaks(readings, sampling_rate=1)
    # Compute HRV indices
    features = nk.hrv(readings, sampling_rate=1, show=False, size=1)
    arousal = model_a.predict(features)
    valence = model_v.predict(features)

    if valence == 0 and arousal == 0:
        return 'sad'
    if valence == 0 and arousal == 1:
        return 'angry'
    if valence == 1 and arousal == 0:
        return 'relaxed'
    if valence == 1 and arousal == 1:
        return 'happy'
