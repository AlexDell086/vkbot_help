# -*- coding: utf-8 -*-
# 295608 - Stavropol
# 294021 - Moscow
# 294010 - Oditsovo
# 294009 - Люберцы

import requests
import datetime

# test = 'погода в Москве'
s = ''
res = ''
def weather(test, number):
    try:
        if test == 'weather in moscow':
            res = requests.get(
                'http://dataservice.accuweather.com/forecasts/v1/hourly/12hour/294021?apikey=53PHe37Gi7o1AHGXSReqyeR0BDAJxMFH&details=true')
    except Exception as e:
        print("Exception (forecast):", e)
    try:
        if test == 'weather in stavropol':
            res = requests.get(
                'http://dataservice.accuweather.com/forecasts/v1/hourly/12hour/295608?apikey=53PHe37Gi7o1AHGXSReqyeR0BDAJxMFH&language=ru&details=true')
    except Exception as e:
        print("Exception (forecast):", e)
    try:
        if test == 'weather in odintsovo':
            res = requests.get(
                'http://dataservice.accuweather.com/forecasts/v1/hourly/12hour/294010?apikey=53PHe37Gi7o1AHGXSReqyeR0BDAJxMFH&language=ru&details=true')
    except Exception as e:
        print("Exception (forecast):", e)
    try:
        if test == 'weather in lyubertsy':
            res = requests.get(
                'http://dataservice.accuweather.com/forecasts/v1/hourly/12hour/294009?apikey=53PHe37Gi7o1AHGXSReqyeR0BDAJxMFH&language=ru&details=true')

    except Exception as e:
        print("Exception (forecast):", e)
    s = []
    count = 0

    for element in res.json():
        description = element['IconPhrase']
        foo = element['DateTime'].replace('T', ' ')
        foo = foo.replace('+03:00', '')
        date = datetime.datetime.strptime(foo, "%Y-%m-%d %H:%M:%S").hour
        print(datetime.datetime.strptime(foo, "%Y-%m-%d %H:%M:%S"))
        temperature = ((element['Temperature']['Value']) - 32) * (5 / 9)
        realTemperature = ((element['RealFeelTemperature']['Value']) - 32) * (5 / 9)
        wind = element['Wind']['Speed']['Value'] * 0.44704
        direction = element['Wind']['Direction']['Localized']
        if direction == 'Г':
            direction = 'В'
        windGust = element['WindGust']['Speed']['Value'] * 0.44704
        humidity = element['RelativeHumidity']
        visible = element['Visibility']['Value'] * 1609.344
        precipitationProbability = element['PrecipitationProbability']
        rainProbability = element['RainProbability']
        snowProbability = element['SnowProbability']
        iceProbability = element['IceProbability']
        totalLiquid = element['TotalLiquid']['Value']
        rain = element['Rain']['Value']
        snow = element['Snow']['Value']
        ice = element['Ice']['Value']
        cloud = element['CloudCover']
        answer = """
        Basic information:
           Time: {}: 00
           Description: {}
           Temperature: {: .2f} C
           RealFeelTemperature: {: .2f} C
           Precipitation probability: {}%
           Rain probability: {}%
           Snow probability: {}%
           Ice probability: {}%
           Total liquid: {} mm

         Additional Information:
           Wind speed: {: .2f} m / s
           Direction of the wind: {}
           Wind gusts: {: .2f} m / s
           Relative humidity: {}%
           Visibility: {: .2f} m
           Cloudiness: {}%
           Rain: {} mm
           Snow: {} mm
           Ice: {} mm
    
        """.format(date, description, temperature, realTemperature, precipitationProbability, rainProbability,
                   snowProbability, iceProbability, totalLiquid, wind, direction, windGust, humidity, visible,
                   cloud, rain, snow, ice)
        if number > count:
            s.append(answer)
        count = count + 1
    #print(s)

    return s


