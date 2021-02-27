# -*- coding: utf-8 -*-
"""
Created on Wed Apr 29 20:58:55 2020

@author: carlo
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time
from collections import defaultdict
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.dates import DateFormatter

df=pd.read_csv(r'../../data/training.csv')
test=pd.read_csv(r'../../data/test.csv')
df = df.append(test).reset_index()

def extract_ts(df, time_col, attributes, ts_size = 1440, format = '%Y-%m-%d %H:%M:%S', weekend = True, WED = False):
    attributes = attributes.insert(time_col)
    df[time_col] =  pd.to_datetime(df['date'], format='%Y-%m-%d %H:%M:%S')
    df['Weekday']=df['date'].apply(lambda x:x.weekday())
    
    #splitthe df between days of the week
    mon=df[df['Weekday']==0][attributes].copy()
    tue=df[df['Weekday']==1][attributes].copy()
    wed=df[df['Weekday']==2][attributes].copy() #N.B. -> mancano delle ore tra mezzogioro e le tre, incompleto 
    thu=df[df['Weekday']==3][attributes].copy()
    fri=df[df['Weekday']==4][attributes].copy()
    sat=df[df['Weekday']==5][attributes].copy()
    sun=df[df['Weekday']==6][attributes].copy()
    
    weekdays =[mon,tue,wed,thu,fri,sat,sun]
    #removes sat sun or wed basin on attribute passed... by default wednesday is removes but sat and sun no
    if weekend == False:   
        weekdays.remove(sat)
        weekdays.remove(sun)
    if WED == False: 
        weekdays.remove(wed)
    
    ts_list=[]
    for day in weekdays:
        day[time_col]=day[time_col].apply(lambda x: str(x)[11:19]) #get string %H:%M:%S and lose info about the daydate
        day.rename(columns={time_col:'Time'},inplace=True) 
        day.sort_values('Time', inplace=True)
        day['Time']=pd.to_datetime(day['Time'], format='%H:%M:%S')
        day.sort_values('Time', inplace=True)
        day.set_index('Time',inplace=True)
        while (len(mon)>= ts_size):
            ts=mon.sample(ts_size)
            ts_list.append(ts)
            mon.drop(ts.index, axis=0, inplace=True)
            print(len(ts_list))
            print(len(mon))

    return ts_list

  
fig = plt.figure(figsize=(40,30))
ax = fig.subplots()
for ts in ts_list[:10]:
    ax.plot(ts.index.values,ts[attribute])
ax.set_ylabel(attribute)
date_form = DateFormatter("%H")
ax.xaxis.set_major_formatter(date_form)
plt.show()