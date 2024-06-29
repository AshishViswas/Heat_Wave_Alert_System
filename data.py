import pandas as pd
import numpy as np
import requests
from datetime import datetime

#Load mumbai.csv file
data = pd.read_csv('mumbai.csv')

#Load mumbai_old.csv file
data_for_reference = pd.read_csv('mumbai_old.csv')

#  In India, the India Meteorological Department (IMD) considers only maximum temperatures (Tmax) for defining heat waves.
#  According to IMD criteria:
# For Plains: If the maximum temperature of a station reaches at least 40°C or more.
# For Coastal stations: If the maximum temperature reaches at least 37°C or more.
# For Hilly regions: If the maximum temperature reaches at least 30°C or more1.
# The Heat Index combines air temperature and relative humidity to assess heat stress.

# we have chosen the 'mumbai' city weather data for project. As it is a coastal region, any temperature above 37C is considered extremely hot. we also only consider factors such as max Temp and Heat Index in training the model to predict the heat waves

#Initially Loading only required columns into Heat_wave
Heat_wave = data.loc[:, ['date_time','maxtempC']]

# Coverting the values in date_time column to datetime type and setting it as index so as to implement time-related operations
Heat_wave['date_time'] = pd.to_datetime(Heat_wave['date_time'])
Heat_wave.set_index('date_time', inplace=True)

data['date_time'] = pd.to_datetime(data['date_time'])
data.set_index('date_time', inplace=True)

data_for_reference['date_time'] = pd.to_datetime(data_for_reference['date_time'])
data_for_reference.set_index('date_time', inplace=True)

# In India, the **India Meteorological Department (IMD)** considers only **maximum temperatures (Tmax)** for defining heat waves.
#    - According to IMD criteria:
#      - For **Plains**: If the maximum temperature of a station reaches at least **40°C or more**.
#      - For **Coastal stations**: If the maximum temperature reaches at least **37°C or more**.
#      - For **Hilly regions**: If the maximum temperature reaches at least **30°C or more**¹.

# The Normal max temperature of Mumbai is 33.58
Heat_wave.mean(axis= 0)

# As Mumbai is a coastal region, it is considered a heat wave if maxtempC reaches atleast 37C or more and departure from normal is between 4.5 to 6.4 degrees. If these conditions persist for more than two days, then a heat wave is declared for that region.

# For defining heat waves, there are more indices used in scientific literature,especially with area averaged or gridded data. The first one is the 90th percentile
# threshold of maximum temperature (Tmax90) based on a 5-day window. 

# The second index considered is the Excessive Heat Factor (EHF) which is based on two excessive heat indices, namely Excess Heat (EHIsig) and Heat Stress (EHIaccl).

# ***The Excess Heat Index is calculated as 𝐸𝐻𝐼sig = (Ti + Ti−1 + Ti−2)/3− T95***, where T95 is the 95th percentile of DMT (Ti) for the climate reference period of 1961-1990. 

# But since lack of availability of data form 1961-1990, in this project I considered data from 2010-2020 as reference data 

# The daily mean temperature is the average of maximum and minimum temperatures as defined by 𝑇 = (𝑇𝑚𝑎𝑥 + 𝑇𝑚𝑖𝑛)/2 . 

# ***The heat stress is defined as 𝐸𝐻𝐼𝑎𝑐𝑐𝑙 = (𝑇𝑖 + 𝑇𝑖−1 + 𝑇𝑖−2)/3 − (𝑇𝑖−3+. . . +𝑇𝑖−32) /30 where Ti is the DMT on ith day.***      

# ***The Excess Heat Factor (EHF) is defined as follows: 𝐸𝐻𝐹 = 𝐸𝐻𝐹𝑠𝑖𝑔 × max(1,E𝐻𝐼𝑎𝑐𝑐𝑙)***   
       
# A heat wave is considered when the value of EHF is positive, and the daily climatological Tmax is greater than 35°C for consecutive three days or more

#90th percentile threshold of maximum temperature (Tmax90) based on a 5-day window 
Heat_wave['tmean90'] = Heat_wave['maxtempC'].rolling('5D', min_periods = 1).quantile(0.9)

Heat_wave['tmean'] = (data['maxtempC'] + data['mintempC'])/2

Heat_wave['tmean_3D'] = Heat_wave['tmean'].rolling('3D', min_periods = 1).mean()

#reference_t95 is the 95th percentile of DMT (Ti) for the climate reference period of 2010-2020 as data for 1961-2010 is not available
data_for_reference['mean'] = (data_for_reference['maxtempC'] + data_for_reference['mintempC'])/2
reference_t95 = data_for_reference['mean'].quantile(0.95)

Heat_wave['Excess_Heat_Index'] = Heat_wave['tmean_3D'] - reference_t95
Heat_wave['Heat_Stress'] = Heat_wave['tmean_3D'] - (Heat_wave['tmean'].rolling(window=30).mean().shift(3)) / 30
Heat_wave['Excess_Heat_Factor'] = Heat_wave['Excess_Heat_Index'] * Heat_wave['Heat_Stress'].apply(lambda x: max(1, x))

# Conditions for the classes
# if the temperature is 4.5C more than normal max temp which is 33.5C then it is considered as a Heat Wave
conditions = [
    (Heat_wave['maxtempC'] < 33.5 + 4.5),
    (Heat_wave['maxtempC'] >= 33.5 + 4.5) & (Heat_wave['Excess_Heat_Factor'] > 0)
]

# Class labels
class_labels = [False,True]

# Create a new column with class labels based on the conditions
Heat_wave['Heat_Condition'] = np.select(conditions, class_labels)

# Create a new column initialized with False
Heat_wave['Heat_Wave'] = False

#Condition for Two days
Heat_wave['Heat_Wave'] = (Heat_wave['Heat_Condition']==1) & (Heat_wave['Heat_Condition'].shift(1)==1) & (Heat_wave['Heat_Condition'].shift(2)==1)

# exporting it as Heat_wave.csv file
Heat_wave.to_csv('Heat_wave.csv',index=True,header=True)

# Code to make a API call to get daily weather data in real-time
# import json
from model import prediction

# Function to obtain today's weather data and make predictions using model from model.py
# It is called from Flask Backend every morning at 8:00 AM to retreive today's weather data and use it to predict the heat wave for the day
def Heat_Wave_Update():
    # Replace 'api_key' with your actual API key
    api_key = 'api_key'
    location = 'mumbai'
    url = f'http://api.worldweatheronline.com/premium/v1/weather.ashx?key={api_key}&q={location}&format=json'

    response = requests.get(url)
    weather_data = response.json()

    # Access the 'maxtempC' parameter
    max_temp_c = int(weather_data['data']['weather'][0]['maxtempC'])
    min_temp_c = int(weather_data['data']['weather'][0]['mintempC'])
    mean = (max_temp_c + min_temp_c)/2
    date = weather_data['data']['weather'][0]['date']
    time = weather_data['data']['weather'][0]['hourly'][0]['time']
    time_value = time.zfill(4)
    formatted_time = f"{time_value[:2]}:{time_value[2:]}"

    # Combine date and time to create a datetime string
    datetime_str = f"{date} {formatted_time}"

    # Convert the string to a datetime object
    period_datetime = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M')

    tmean90 = Heat_wave['maxtempC'][-5:].quantile(0.9)

    tmean_3D = (Heat_wave['tmean'][-2:].mean() + mean)/2

    Excess_Heat_Index = tmean_3D - reference_t95
    Heat_Stress = tmean_3D - (Heat_wave['tmean'][-33:].shift(3).mean()) / 30
    Excess_Heat_Factor = Excess_Heat_Index * max(1,Heat_Stress)

    if max_temp_c > 33.8 + 4.5 and Excess_Heat_Factor > 0:
      Heat_Condition = 1
    else:
      Heat_Condition = 0

    new_row = {'date_time': period_datetime, 'maxtempC': max_temp_c, 'tmean90': tmean90, 'tmean': mean, 'tmean_3D': tmean_3D, 'Excess_Heat_Index': Excess_Heat_Index, 'Heat_Stress': Heat_Stress, 'Excess_Heat_Factor': Excess_Heat_Factor, 'Heat_Condition': Heat_Condition}

    # Convert the new record to a DataFrame with the first column as the index
    new_record = pd.DataFrame([new_row]).set_index('date_time')
    new_wave = Heat_wave
    # Append the new record DataFrame to the original DataFrame
    new_wave = pd.concat([new_wave, new_record])

    new_wave.loc[new_wave.index[-1], 'Heat_Wave'] = (
    (new_wave.loc[new_wave.index[-1], 'Heat_Condition'] == 1) &
    (new_wave.loc[new_wave.index[-2], 'Heat_Condition'] == 1) &
    (new_wave.loc[new_wave.index[-3], 'Heat_Condition'] == 1)
     )
    
    #read new_wave as csv file
    new_wave.to_csv('Heat_wave.csv',index = True, header = True)

    #Predict the occurence of heat_wave using model imported from model.py
    a = prediction(new_record)
    return a