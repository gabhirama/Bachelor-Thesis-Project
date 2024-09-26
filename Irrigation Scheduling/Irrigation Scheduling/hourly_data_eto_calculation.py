# -*- coding: utf-8 -*-
"""Hourly Data ETo calculation.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1qINZihos_rbRgBUwFJTi4afMfWE6s3X7
"""

from datetime import datetime
import math

#Julain Day
user_input = input("Enter a date (YYYY-MM-DD): ")
user_date = datetime.strptime(user_input, "%Y-%m-%d").date()
julian_day = user_date.timetuple().tm_yday

#Time of Data Recording
time_str = input("Enter the time (HH:MM:SS): ")
time_stamp = int(time_str.split(":")[0])+0.5

#Latitude and Longitude of the test site
print("Enter the coordinates of the test site in the format (Degrees°Minutes')\n")

latitude = input("Latitude ")
degrees, minutes = latitude.split("°")
degrees = int(degrees)
minutes = int(minutes[:-1])
latitude = float(degrees + (minutes / 60))
latitude_radians = math.radians(latitude)

longitude = input("Longitude ")
degrees, minutes = longitude.split("°")
degrees = int(degrees)
minutes = int(minutes[:-1])
longitude = float(degrees + (minutes / 60))
longitude_from_west = 360 - longitude

hours_ahead_gmt = float(input("Enter UTC offset (hours ahead of GMT): "))
longitude_of_time_zone = 360 - hours_ahead_gmt * 15

#Elevation of the test site
elevation = int(input("Enter elevation of the test site: "))

#Wind speed at 2meters
wind_speed = float(input("Enter wind speed at 2 meters from ground: "))
wind_speed = 5*wind_speed/18

#Temperatures
max_temp = float(input("Enter the maximum temperature recorded this hour: "))
min_temp = float(input("Enter the miniimum temperature recorded this hour: "))
mean_temp = (max_temp + min_temp)/2

#Relative Humidity
max_RH = int(input("Enter the relative humidty corresponding to this hour's maximum temperature: "))
min_RH = int(input("Enter the relative humidty corresponding to this hour's minimum temperature: "))
mean_RH = (max_RH + min_RH)/2

#Dew Point Temperature
max_DPT = (4030*(235+max_temp)/(4030-((max_temp+235)*math.log(max_RH/100))))-235
min_DPT = (4030*(235+min_temp)/(4030-((min_temp+235)*math.log(min_RH/100))))-235
mean_DPT = (max_DPT + min_DPT)/2

#Constants
lambdaa = 2.45                                                                                                      #Latent Heat of Vapourization
alpha = 0.23                                                                                                        #Albedo / Crop Canopy Coefficient
sigma = 2.043e-10                                                                                                   #Stefan-Bolzmann Constant
Gsc = 0.082                                                                                                         #Solar Constant

PI = math.pi  
solar_dec = 0.409 * math.sin((2 * PI * julian_day / 365) - 1.39)                                                                                        #Solar Declination (in radians)
dr = 1 + 0.033 * math.cos(2 * PI * julian_day / 365)                                                                                                     #Inverse Relative Distance Earth-Sun
b = 2*PI*(julian_day-81)/364
Sc = 0.1645 * math.sin(2*b) - 0.1225 * math.cos(b) - 0.025 * math.sin(b)                                                     
w = PI*(time_stamp + 0.06667*(longitude_of_time_zone - longitude_from_west) + Sc - 12)/12                                                               #Solar time angle at midpoint of hour [rad] 
w1 = w - (PI/24)                                                                                                                                        #Solar time angle at beginning of hour [rad]
w2 = w + (PI/24)                                                                                                                                        #Solar time angle at end of hour [rad]
sinx = ((w2-w1) * math.sin(latitude_radians) * math.sin(solar_dec)) + (math.cos(latitude_radians) * math.cos(solar_dec) * (math.sin(w2)-math.sin(w1)))  #sin(Solar Altitude Angle)
Ra = 12 * 60 * Gsc * dr * sinx / PI                                                                                                                     #Extraterrestrial Radiation

if mean_RH > 65:
  if (time_stamp >6 and time_stamp < 18):
    Rs = 2.45
    Rso = Rs*0.4
    f = 0.19
  else:
    Rs = 0
    Rso = 0
    f = 0.19 
else:
  if (time_stamp >6 and time_stamp < 18):
    Rs = 2.45
    Rso = Rs*0.8
    f = 0.73
  else:
    Rs = 0                                                                                                                                              #Solar Radiation
    Rso = 0                                                                                                                                             #Clear Sky Solar Radiation
    f = 0.73                                                                                                                                            #Cloudiness Function
ea = 0.6108*(math.exp(17.27*mean_DPT/(mean_DPT+237.3)))                                                                                                 #Actual Vapour Pressure
es = 0.6108*(math.exp(17.27*mean_temp/(mean_temp+237.3)))                                                                                               #Saturated Vapour Pressure
epsilon = 0.34 - (0.14 * math.sqrt(ea))                                                                                                                 #Apparent Net Clear Sky Emmisivity
delta = 4098*es/(mean_temp+237.3)**2                                                                                                                    #Slope of Saturation Vapour Pressure Curve
Bp = 101.3 * ((1 - (0.0000221843 * elevation)) ** 5.6)                                                                                                  #Barometric Pressure
gamma = 0.00163*Bp/lambdaa                                                                                                                              #Psychometric Constant
Rns = (1-alpha)*Rs                                                                                                                                      #Net Shortwave Radiation
Rnl = f*epsilon*sigma*(mean_temp + 273.15)**4                                                                                                           #Net Longwave Radiation
Rn = Rns - Rnl                                                                                                                                          #Net Radiation
if (time_stamp >6 and time_stamp < 18):
  G = 0.1*Rn
else:
  G = 0.5*Rn                                                                                                                                            #Soil Heat Flux
numerator = 0.4098*delta*(Rn-G) + gamma*wind_speed*37*(es-ea)/(mean_temp+273)
denominator = delta + gamma*(1+(0.34*wind_speed))
ETo = numerator/denominator                                                                                                                             #Reference Evapotranspiration
print("The calculated Reference Evapotranspiration is",ETo,"mm/hour")

