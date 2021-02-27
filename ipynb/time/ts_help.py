# -*- coding: utf-8 -*-
"""
Created on Wed Apr 29 20:58:55 2020

"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time
import random
from collections import defaultdict
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.dates import DateFormatter




def extract_list(df, time_col, attribute, ts_size = 1440, format = '%Y-%m-%d %H:%M:%S', weekend = True, WED = False):
    attributes = [time_col, attribute]
    df[time_col] =  pd.to_datetime(df[time_col], format=format)
    df['Weekday']=df[time_col].apply(lambda x:x.weekday())
    #split the df between days of the week
    mon=df[df['Weekday']==0][attributes].copy()

    tue=df[df['Weekday']==1][attributes].copy()
    print(len(tue))
    wed=df[df['Weekday']==2][attributes].copy() #N.B. -> mancano delle ore tra mezzogioro e le tre, incompleto 
    thu=df[df['Weekday']==3][attributes].copy()
    fri=df[df['Weekday']==4][attributes].copy()
    sat=df[df['Weekday']==5][attributes].copy()
    sun=df[df['Weekday']==6][attributes].copy()
    
    weekdays =[mon,tue,thu,fri]
    #removes sat sun or wed basin on attribute passed... by default wednesday is removes but sat and sun no
    if weekend == True:   
        weekdays.append(sat)
        weekdays.append(sun)
    if WED == True: 
        print('attento')
        weekdays.append(wed) 
    ts_list=[]
    for day in weekdays:
        day.sort_values(time_col, inplace=True)
        #day[time_col]=day[time_col].apply(lambda x: str(x)[11:19]) #get string %H:%M:%S and lose info about the daydate
        #day[time_col]=pd.to_datetime(day[time_col], format='%H:%M:%S')  #now a date is setted automaticaly for all records
        
        day.set_index(time_col, inplace=True)
        while (len(day)>= ts_size):
            ts=day.sample(ts_size)
            ts.sort_values(time_col, inplace=True) #necessary to order
            ts_list.append(ts)
            day.drop(ts.index, axis=0, inplace=True)
            
    return ts_list


    
def ts_split(ts_list,n = 3): # to split in n parts  each ts of ts_list
    new_ts_list = []
    length = len(ts_list[0])//n
    for ts in ts_list:
        i=0
        while(i<n):
            ts_part = ts[:length]
            ts.drop(ts_part.index, axis=0, inplace=True)
            new_ts_list.append(ts_part)
            i+=1
    return(new_ts_list)
    

def draw_list(ts_list, attribute, ts_number=1000, formatter = None):
    if ts_number >= len(ts_list): ts_number = len(ts_list)-1
    fig = plt.figure()
    ax = fig.subplots()
    for ts in ts_list[:ts_number]:
        ax.plot(ts[attribute])
    ax.set_ylabel(attribute)
    if formatter !=None:
        date_form = DateFormatter("%H")
        ax.xaxis.set_major_formatter(date_form)
    plt.show()
    
  
def test_ts_help():
    df=pd.read_csv(r'../../data/datatraining.txt')
    test=pd.read_csv(r'../../data/datatest2.txt')
    time_col = 'date'
    attribute='HumidityRatio'
    ts_list = extract_list(df, time_col, attribute,100)
    test_list=extract_list(test, time_col, attribute, 100 )
    ts_list.extend(test_list)
    #random.shuffle(ts_list)
    draw_list(ts_list, attribute, 15, formatter = '%H')
    ts_list = ts_split(ts_list,10)
    draw_list(ts_list, attribute, 10)
    
test_ts_help()