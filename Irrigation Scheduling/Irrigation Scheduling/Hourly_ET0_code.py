# -*- coding: utf-8 -*-
"""
Created on Sat Apr  1 00:10:00 2023

@author: High-Tech
"""
import pandas as pd
import math
from datetime import date, datetime

# Input parameter

z = 8
P = 101.3*((293-0.0065*z)/293)**5.26
gamma = 0.665*(10**-3)*P
Lz = 15
Lm = 16.25
Latitude = 16.22

daylight = ['07:00-08:00','08:00-09:00','09:00-10:00','10:00-11:00','11:00-12:00','12:00-13:00','13:00-14:00','14:00-15:00',
            '15:00-16:00','16:00-17:00','17:00-18:00']

nighttime = ['18:00-19:00','19:00-20:00','20:00-21:00','21:00-22:00','22:00-23:00','23:00-00:00','00:00-01:00',
             '01:00-02:00','02:00-03:00','03:00-04:00','04:00-05:00','05:00-06:00','06:00-07:00']


#1. Weather Parameter

data = pd.read_excel(r"E:\MTP_1\Hourly_ET0.xlsx",sheet_name='Sheet2');

data['ET0'] = ''


for i in range(len(data)):
    Time = data['Date_time'][i]
    t = (int(data['Date_time'][i][0:2])+int(data['Date_time'][i][6:8]))/2
    T = data['Temperature (°C)'][i]
    RH = data['RH (%)'][i]
    WS = data['WS (ms-1)'][i]
    RS = data['Solar Radiation (MJ m-2 hour-)'][i]
    J = data['Julian day'][i]
    delta = round(4098*(0.6108*math.exp(17.27*T/(T+237.3)))/((T+237.3)**2),4)
    es = round(0.6108*math.exp(17.27*T/(T+237.3)),4)
    ea = round(RH/100*es,4)
    dr = round(1 + 0.033*math.cos(2*math.pi*J/365),4)
    solar_dec = round(0.409*math.sin((2*math.pi*J/365)-1.39),4)
    b = round(2*math.pi*(J-81)/364,4)
    Sc = round(0.1645*math.sin(2*b)-0.1255*math.cos(b)-0.025*math.sin(b),4)
    w = round(math.pi/12*((t+0.06667*(Lz-Lm)+Sc)-12),4)
    if (w<=0):
        w1 = 0
        w2 = 0
    if (w>0):
        w1 = round(w-math.pi*1/24,4)
        w2 = round(w+math.pi*1/24,4)
    
    Ra = round(12*60/math.pi*0.0820*dr*((w2-w1)*math.sin(math.pi*Latitude/180)*math.sin(solar_dec)+math.cos(math.pi*Latitude/180)*math.cos(solar_dec)*(math.sin(w2)-math.sin(w1))),4)
    Rso = round((0.75 + 2*10**-5*z)*Ra,4)
    Rns = round((1-0.23)*RS,4)
    if Rso == 0:
        rs_rso = 0.8
        Rnl = round(4.903*10**-9*((T+273.16)**4)*(0.34-0.14*math.sqrt(ea))*(1.35*rs_rso-0.35)/24,4)
    if Rso > 0:
        Rnl = round(4.903*10**-9*((T+273.16)**4)*(0.34-0.14*math.sqrt(ea))*(1.35*RS/Rso-0.35)/24,4)
    Rn = round(Rns-Rnl,4)
    if Time in daylight:
        G = round(0.1*Rn,4)
    if Time in nighttime:
        G = round(0.5*Rn,4)
    ET0 = (0.408*delta*(Rn-G)+gamma*37/(T+273)*WS*(es-ea))/(delta+gamma*(1+0.34*WS))
    data['ET0'][i] = ET0       
    
    


