# -*- coding: utf-8 -*-
import pandas as pd
from pandas import DataFrame
import datetime
import requests
from bs4 import BeautifulSoup

def hostel_miem():
    bus = DataFrame(columns=('id', 'departure_bus'))
    num = ['Первый', 'Второй', 'Третий', 'Четвертый']
    id = 0
    departure_bus = ['06:45:00', '07:10:00', '07:30:00', '07:50:00', '08:05:00', '08:30:00', '08:45:00', '09:05:00',
                     '09:35:00',
                     '10:15:00', '10:30:00', '11:32:00', '11:50:00', '13:25:00', '15:05:00', '15:50:00', '16:12:00',
                     '16:40:00',
                     '17:05:00', '17:25:00', '18:11:00', '18:55:00', '19:20:00', '19:50:00', '20:16:00', '20:35:00',
                     '21:00:00',
                     '21:25:00', '21:50:00', '22:10:00', '22:59:00']  # будни
    for item in departure_bus:  # создает DataFrame (расписание)
        item = pd.to_datetime(item)
        record = {
            'id': id,
            'departure_bus': item,
        }
        bus = bus.append(record, ignore_index=True)
        id = id + 1

    abc = datetime.datetime.now()  # настоящее времся
    r = bus[bus['departure_bus'] > abc].iloc[:4]

    time_1 = []  # Время до приезда автобуса
    for item in range(len(r)):  # создается список time_1(4)
        time_1.append(r.departure_bus.iloc[item] - abc)

    s = ''
    answer_1 = '\tАвтобус будет на остановке:\n'  # Выыодит пользователю времени ожидания автобуса
    for date in num[:len(r)]:
        s = ''' {} через: {} час и {} минут \n'''.format(date, str(time_1[num.index(date)])[8:9],
                                               str(time_1[num.index(date)])[10:12])
        answer_1 = answer_1 + s
        #################################################################
    s = requests.Session()
    s.headers.update({
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'
            })

    url = "https://www.google.com/maps/dir/55.6594766,37.2283472/%D1%81%D1%82.%D0%9E%D0%B4%D0%B8%D0%BD%D1%86%D0%BE%D0%B2%D0%BE,+%D0%9E%D0%B4%D0%B8%D0%BD%D1%86%D0%BE%D0%B2%D0%BE/@55.6692156,37.2233307,13z/data=!3m1!4b1!4m9!4m8!1m0!1m5!1m1!1s0x46b5504c19aefc9f:0x434d5634cfcc75ef!2m2!1d37.281235!2d55.672215!3e0?hl=ru"
    request = s.get(url)
    html = request.content
    soup = str(BeautifulSoup(html,'html.parser'))
    h = soup.find('мин.') + 3
    t = soup[h:].find('мин.')
    time_bus = int(soup[h+t-3:h+t-1]) #время в пути до элки
    answer_2 = """\n\nВремя в пути на автобусе составит: {} минут\n\n""".format(time_bus) # время на дорогу
    time_2 = []# общее время (ИТОГ) время прибытия в Одинцово
    abc = datetime.datetime.now()


    for item in range(len(time_1)):  # создается список time_1(4)
          time_2.append(time_1[item] + datetime.timedelta(minutes=time_bus) + abc)

    answer_3 = "Прибытие в Одинцово:\n"
    for i in range(len(time_1)):
        qwerty = """В {} случае:  {} \n""".format(i+1,(str(time_2[i]).replace('.', ' ')).split()[1])
        answer_3 = answer_3 + qwerty

    answer_2 = answer_2 + answer_3 + '\n'
    #print(answer_2)
    #return answer_2, time_2
    ########################################################
    abc = datetime.datetime.now()
    abc = (str(abc)).split()[0]
    url = 'https://api.rasp.yandex.net/v3.0/search/?apikey=af3262d1-dd33-4e7d-9361-0bad820d9ff2&format=json&from=c10743&to=s9601728&lang=ru_RU&page=1&date={}&transport_types'.format(abc)
    res = requests.get(url)
    res = res.json()
    suburban = pd.read_csv('bot.csv')

    f = 0
    for i in res['segments']:
        id = f
        departure = i['from']['title']
        arrival = i['to']['title']
        trip = i['thread']['title']
        time_departure = pd.to_datetime(i['departure'].replace('+03:00', ''))
        time_arrival = pd.to_datetime(i['arrival'].replace('+03:00', ''))
        travel_time = time_arrival - time_departure
        stops = i['stops']
        comfort = i['thread']['transport_subtype']['title']
        record = {
            'id': id,
            'departure': departure,
            'arrival': arrival,
            'trip': trip,
            'time_departure': time_departure,
            'time_arrival': time_arrival,
            'travel_time': travel_time,
            'stops': stops,
            'comfort': comfort
        }

        suburban = suburban.append(record, ignore_index=True)
        f = f + 1

    answer_3 = ''
    time_3 = []
                #print(time_2)
    abc = datetime.datetime.now()
    for item in range(len(time_2)):
            between = suburban[suburban['time_departure'] > time_2[item]].iloc[:len(time_2)]
            qwerty = """Trip: {}\nDepurture_time: {}\nArrival_time: {}\nTravel_time: {}\ncomfort: {}\ntime_out: {}\n\n """.format(between.trip.iloc[0],
                       str(between.time_departure.iloc[item]).split()[1],
                       str(between.time_arrival.iloc[item]).split()[1],
                       str(between.travel_time.iloc[0]).split()[2], between.comfort.iloc[0],
                       (str(between.time_departure.iloc[item] - abc)).replace('.', ' ').split()[2])
            answer_3 = answer_3 + qwerty

            #time_3.append(str(between.time_arrival.iloc[0]).split()[2])
            time_3.append(str(between.time_arrival.iloc[item]))

            #print(answer_3)
    #return answer_3 , time_3, suburban
    for i in range(len(time_3)):
        time_3[i] = datetime.datetime.strptime(time_3[i], "%Y-%m-%d %H:%M:%S")
            #print(time[i])
        time_3[i] = time_3[i] + datetime.timedelta(minutes=35)

    answer1 = "Прибытие в МИЭМ\n"
    for i in range(len(time_3)):
        qwerty = """В {} случае:  {} \n""".format(i + 1 , (str(time_3[i]).replace('.', ' ')).split()[1])
        answer1 = answer1 + qwerty

    if answer_1 == 'Автобус будет на остановке:':
        return 'Вся спят уже, зачем тебе в такую ночь куда то ехать!?'
    return answer_1 + answer_2 + answer_3 +answer1

def odinsovo_miem():
    abc = datetime.datetime.now()
    abc = (str(abc)).split()[0]
    url = 'https://api.rasp.yandex.net/v3.0/search/?apikey=af3262d1-dd33-4e7d-9361-0bad820d9ff2&format=json&from=c10743&to=s9601728&lang=ru_RU&page=1&date={}&transport_types'.format(
        abc)
    res = requests.get(url)
    res = res.json()
    suburban = pd.read_csv('bot.csv')

    f = 0
    for i in res['segments']:
        id = f
        departure = i['from']['title']
        arrival = i['to']['title']
        trip = i['thread']['title']
        time_departure = pd.to_datetime(i['departure'].replace('+03:00', ''))
        time_arrival = pd.to_datetime(i['arrival'].replace('+03:00', ''))
        travel_time = time_arrival - time_departure
        stops = i['stops']
        comfort = i['thread']['transport_subtype']['title']
        record = {
            'id': id,
            'departure': departure,
            'arrival': arrival,
            'trip': trip,
            'time_departure': time_departure,
            'time_arrival': time_arrival,
            'travel_time': travel_time,
            'stops': stops,
            'comfort': comfort
        }

        suburban = suburban.append(record, ignore_index=True)
        f = f + 1

        answer_3 = ''
        time_3 = []
        # print(time_2)

        abc = datetime.datetime.now()
        between = suburban[suburban['time_departure'] > abc].iloc[:4]
    for item in range(len(between)):

        qwerty = """Trip: {}\nDepurture_time: {}\nArrival_time: {}\nTravel_time: {}\ncomfort: {}\ntime_out: {}\n\n """.format(between.trip.iloc[0], str(between.time_departure.iloc[item]).split()[1],
                          str(between.time_arrival.iloc[item]).split()[1],
                          str(between.travel_time.iloc[0]).split()[2], between.comfort.iloc[0], (str(between.time_departure.iloc[item] - abc)).replace('.',' ').split()[2])
        answer_3 = answer_3 + qwerty

        time_3.append(str(between.time_arrival.iloc[item]))

        # print(answer_3)
    # return answer_3 , time_3, suburban
    for i in range(len(time_3)):
        time_3[i] = datetime.datetime.strptime(time_3[i], "%Y-%m-%d %H:%M:%S")
        # print(time[i])
        time_3[i] = time_3[i] + datetime.timedelta(minutes=35)

    answer1 = "Прибытие в МИЭМ"
    for i in range(len(time_3)):
        qwerty = """
         В {} случае:  {}""".format(i + 1, (str(time_3[i]).replace('.', ' ')).split()[1])
        answer1 = answer1 + qwerty

    print(answer_3 + answer1)

    return answer_3 + answer1

def hostel_odin():
    bus = DataFrame(columns=('id', 'departure_bus'))
    num = ['Первый', 'Второй', 'Третий', 'Четвертый']
    id = 0
    departure_bus = ['06:45:00', '07:10:00', '07:30:00', '07:50:00', '08:05:00', '08:30:00', '08:45:00', '09:05:00',
                     '09:35:00',
                     '10:15:00', '10:30:00', '11:32:00', '11:50:00', '13:25:00', '15:05:00', '15:50:00', '16:12:00',
                     '16:40:00',
                     '17:05:00', '17:25:00', '18:11:00', '18:55:00', '19:20:00', '19:50:00', '20:16:00', '20:35:00',
                     '21:00:00',
                     '21:25:00', '21:50:00', '22:10:00', '22:59:00']  # будни
    for item in departure_bus:  # создает DataFrame (расписание)
        item = pd.to_datetime(item)
        record = {
            'id': id,
            'departure_bus': item,
        }
        bus = bus.append(record, ignore_index=True)
        id = id + 1

    abc = datetime.datetime.now()  # настоящее времся
    r = bus[bus['departure_bus'] > abc].iloc[:4]

    time_1 = []  # Время до приезда автобуса
    for item in range(len(r)):  # создается список time_1(4)
        time_1.append(r.departure_bus.iloc[item] - abc)

    s = ''
    answer_1 = '\tАвтобус будет на остановке:\n'  # Выыодит пользователю времени ожидания автобуса
    for date in num[:len(r)]:
        s = ''' {} через: {} час и {} минут \n'''.format(date, str(time_1[num.index(date)])[8:9],
                                                         str(time_1[num.index(date)])[10:12])
        answer_1 = answer_1 + s
        #################################################################
    s = requests.Session()
    s.headers.update({
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'
    })

    url = "https://www.google.com/maps/dir/55.6594766,37.2283472/%D1%81%D1%82.%D0%9E%D0%B4%D0%B8%D0%BD%D1%86%D0%BE%D0%B2%D0%BE,+%D0%9E%D0%B4%D0%B8%D0%BD%D1%86%D0%BE%D0%B2%D0%BE/@55.6692156,37.2233307,13z/data=!3m1!4b1!4m9!4m8!1m0!1m5!1m1!1s0x46b5504c19aefc9f:0x434d5634cfcc75ef!2m2!1d37.281235!2d55.672215!3e0?hl=ru"
    request = s.get(url)
    html = request.content
    soup = str(BeautifulSoup(html, 'html.parser'))
    h = soup.find('мин.') + 3
    t = soup[h:].find('мин.')
    time_bus = int(soup[h + t - 3:h + t - 1])  # время в пути до элки
    answer_2 = """\n\nВремя в пути на автобусе составит: {} минут\n\n""".format(time_bus)  # время на дорогу
    time_2 = []  # общее время (ИТОГ) время прибытия в Одинцово
    abc = datetime.datetime.now()

    for item in range(len(time_1)):  # создается список time_1(4)
        time_2.append(time_1[item] + datetime.timedelta(minutes=time_bus) + abc)

    answer_3 = "Прибытие в Одинцово:\n"
    for i in range(len(time_1)):
        qwerty = """В {} случае:  {} \n""".format(i + 1, (str(time_2[i]).replace('.', ' ')).split()[1])
        answer_3 = answer_3 + qwerty

    answer_2 = answer_2 + answer_3 + '\n'
    
    return answer_1 + answer_2

def odin_hostel():
    bus = DataFrame(columns=('id', 'departure_bus'))
    num = ['Первый', 'Второй', 'Третий', 'Четвертый']
    id = 0
    departure_bus = ['00:30:00', '01:23:00','09:05:00', '09:55:00', '10:35:00', '10:50:00', '11:55:00', '12:10:00', '13:57:00', '15:28:00', '16:12:00', '16:32:00',
                     '16:57:00',
                     '17:25:00', '17:45:00', '18:35:00', '19:18:00', '19:43:00', '20:14:00', '20:38:00',
                     '20:55:00',
                     '21:20:00', '21:45:00', '22:06:00', '22:30:00', '23:19:00', '23:53:00']  # будни
    for item in departure_bus:  # создает DataFrame (расписание)
        item = pd.to_datetime(item)
        record = {
            'id': id,
            'departure_bus': item,
        }
        bus = bus.append(record, ignore_index=True)
        id = id + 1

    abc = datetime.datetime.now()  # настоящее времся
    r = bus[bus['departure_bus'] > abc].iloc[:4]

    time_1 = []  # Время до приезда автобуса
    for item in range(len(r)):  # создается список time_1(4)
        time_1.append(r.departure_bus.iloc[item] - abc)

    s = ''
    answer_1 = '\tАвтобус будет на остановке:\n'  # Выыодит пользователю времени ожидания автобуса
    for date in num[:len(r)]:
        s = ''' {} через: {} час и {} минут \n'''.format(date, str(time_1[num.index(date)])[8:9],
                                                         str(time_1[num.index(date)])[10:12])
        answer_1 = answer_1 + s
        #################################################################
    s = requests.Session()
    s.headers.update({
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'
    })

    url = "https://www.google.com/maps/dir/55.6727759,37.2811436/55.6604795,37.2274338/@55.6630984,37.2454733,14.21z/data=!4m2!4m1!3e0?hl=ru"
    request = s.get(url)
    html = request.content
    soup = str(BeautifulSoup(html, 'html.parser'))
    h = soup.find('мин.') + 3
    t = soup[h:].find('мин.')
    try:
        time_bus = int(soup[h + t - 3:h + t - 1])  # время в пути до элки
    except Exception as e:
        print(e)
        time_bus = int(soup[h + t - 2:h + t - 1])
    answer_2 = """\n\nВремя в пути на автобусе составит: {} минут\n\n""".format(time_bus)  # время на дорогу
    time_2 = []  # общее время (ИТОГ) время прибытия в Одинцово
    abc = datetime.datetime.now()

    for item in range(len(time_1)):  # создается список time_1(4)
        time_2.append(time_1[item] + datetime.timedelta(minutes=time_bus) + abc)

    answer_3 = "Прибытие в Дубки:\n"
    for i in range(len(time_1)):
        qwerty = """В {} случае:  {} \n""".format(i + 1, (str(time_2[i]).replace('.', ' ')).split()[1])
        answer_3 = answer_3 + qwerty

    answer_2 = answer_2 + answer_3 + '\n'

    return answer_1 + answer_2

def hostel_slav():
    bus = DataFrame(columns=('id', 'departure_bus'))
    num = ['Первый', 'Второй', 'Третий', 'Четвертый']
    id = 0
    departure_bus = ['10:45:00', '12:45:00', '13:05:00', '13:15:00', '22:15:00', '23:20:00']  # будни
    for item in departure_bus:  # создает DataFrame (расписание)
        item = pd.to_datetime(item)
        record = {
            'id': id,
            'departure_bus': item,
        }
        bus = bus.append(record, ignore_index=True)
        id = id + 1

    abc = datetime.datetime.now()  # настоящее времся
    r = bus[bus['departure_bus'] > abc].iloc[:4]

    time_1 = []  # Время до приезда автобуса
    for item in range(len(r)):  # создается список time_1(4)
        time_1.append(r.departure_bus.iloc[item] - abc)

    s = ''
    answer_1 = '\tАвтобус будет на остановке:\n'  # Выыодит пользователю времени ожидания автобуса
    for date in num[:len(r)]:
        s = ''' {} через: {} час и {} минут \n'''.format(date, str(time_1[num.index(date)])[8:9],
                                                         str(time_1[num.index(date)])[10:12])
        answer_1 = answer_1 + s
        #################################################################
    s = requests.Session()
    s.headers.update({
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'
    })

    url = "https://www.google.com/maps/dir/55.6605768,37.2272365/55.7280058,37.4738118/@55.6942048,37.2808937,12z/data=!3m1!4b1!4m4!4m3!2m1!2b1!3e0?hl=ru"
    request = s.get(url)
    html = request.content
    soup = str(BeautifulSoup(html, 'html.parser'))
    h = soup.find('мин.') + 3
    t = soup[h:].find('мин.')
    time_bus = int(soup[h + t - 3:h + t - 1])  # время в пути до элки
    answer_2 = """\n\nВремя в пути на автобусе составит: {} минут\n\n""".format(time_bus)  # время на дорогу
    time_2 = []  # общее время (ИТОГ) время прибытия в Одинцово
    abc = datetime.datetime.now()

    for item in range(len(time_1)):  # создается список time_1(4)
        time_2.append(time_1[item] + datetime.timedelta(minutes=time_bus) + abc)

    answer_3 = "Прибытие на Славянку:\n"
    for i in range(len(time_1)):
        qwerty = """В {} случае:  {} \n""".format(i + 1, (str(time_2[i]).replace('.', ' ')).split()[1])
        answer_3 = answer_3 + qwerty

    answer_2 = answer_2 + answer_3 + '\n'

    return answer_1 + answer_2

def slav_hostel():
    bus = DataFrame(columns=('id', 'departure_bus'))
    num = ['Первый', 'Второй', 'Третий', 'Четвертый']
    id = 0
    departure_bus = ['00:05:00', '12:55:00', '14:30:00', '14:45:00', '15:05:00', '23:05:00']  # будни
    for item in departure_bus:  # создает DataFrame (расписание)
        item = pd.to_datetime(item)
        record = {
            'id': id,
            'departure_bus': item,
        }
        bus = bus.append(record, ignore_index=True)
        id = id + 1

    abc = datetime.datetime.now()  # настоящее времся
    r = bus[bus['departure_bus'] > abc].iloc[:4]

    time_1 = []  # Время до приезда автобуса
    for item in range(len(r)):  # создается список time_1(4)
        time_1.append(r.departure_bus.iloc[item] - abc)

    s = ''
    answer_1 = '\tАвтобус будет на остановке:\n'  # Выыодит пользователю времени ожидания автобуса
    for date in num[:len(r)]:
        s = ''' {} через: {} час и {} минут \n'''.format(date, str(time_1[num.index(date)])[8:9],
                                                         str(time_1[num.index(date)])[10:12])
        answer_1 = answer_1 + s
        #################################################################
    s = requests.Session()
    s.headers.update({
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'
    })

    url = "https://www.google.com/maps/dir/55.7296056,37.4794462/55.6605768,37.2272365/@55.7708404,37.3312127,10.85z/data=!4m4!4m3!2m1!2b1!3e0?hl=ru"
    request = s.get(url)
    html = request.content
    soup = str(BeautifulSoup(html, 'html.parser'))
    h = soup.find('мин.') + 3
    t = soup[h:].find('мин.')
    time_bus = int(soup[h + t - 3:h + t - 1])  # время в пути до элки
    answer_2 = """\n\nВремя в пути на автобусе составит: {} минут\n\n""".format(time_bus)  # время на дорогу
    time_2 = []  # общее время (ИТОГ) время прибытия в Одинцово
    abc = datetime.datetime.now()

    for item in range(len(time_1)):  # создается список time_1(4)
        time_2.append(time_1[item] + datetime.timedelta(minutes=time_bus) + abc)

    answer_3 = "Прибытие на Славянку:\n"
    for i in range(len(time_1)):
        qwerty = """В {} случае:  {} \n""".format(i + 1, (str(time_2[i]).replace('.', ' ')).split()[1])
        answer_3 = answer_3 + qwerty

    answer_2 = answer_2 + answer_3 + '\n'

    return answer_1 + answer_2

def hostel_lubyanka():
    bus = DataFrame(columns=('id', 'departure_bus'))
    num = ['Первый', 'Второй', 'Третий', 'Четвертый']
    id = 0
    departure_bus = ['06:45:00', '07:10:00', '07:30:00', '07:50:00', '08:05:00', '08:30:00', '08:45:00', '09:05:00',
                     '09:35:00',
                     '10:15:00', '10:30:00', '11:32:00', '11:50:00', '13:25:00', '15:05:00', '15:50:00', '16:12:00',
                     '16:40:00',
                     '17:05:00', '17:25:00', '18:11:00', '18:55:00', '19:20:00', '19:50:00', '20:16:00', '20:35:00',
                     '21:00:00',
                     '21:25:00', '21:50:00', '22:10:00', '22:59:00']  # будни
    for item in departure_bus:  # создает DataFrame (расписание)
        item = pd.to_datetime(item)
        record = {
            'id': id,
            'departure_bus': item,
        }
        bus = bus.append(record, ignore_index=True)
        id = id + 1

    abc = datetime.datetime.now()  # настоящее времся
    r = bus[bus['departure_bus'] > abc].iloc[:4]

    time_1 = []  # Время до приезда автобуса
    for item in range(len(r)):  # создается список time_1(4)
        time_1.append(r.departure_bus.iloc[item] - abc)

    s = ''
    answer_1 = '\tАвтобус будет на остановке:\n'  # Выыодит пользователю времени ожидания автобуса
    for date in num[:len(r)]:
        s = ''' {} через: {} час и {} минут \n'''.format(date, str(time_1[num.index(date)])[8:9],
                                                         str(time_1[num.index(date)])[10:12])
        answer_1 = answer_1 + s
        #################################################################
    s = requests.Session()
    s.headers.update({
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'
    })

    url = "https://www.google.com/maps/dir/55.6594766,37.2283472/%D1%81%D1%82.%D0%9E%D0%B4%D0%B8%D0%BD%D1%86%D0%BE%D0%B2%D0%BE,+%D0%9E%D0%B4%D0%B8%D0%BD%D1%86%D0%BE%D0%B2%D0%BE/@55.6692156,37.2233307,13z/data=!3m1!4b1!4m9!4m8!1m0!1m5!1m1!1s0x46b5504c19aefc9f:0x434d5634cfcc75ef!2m2!1d37.281235!2d55.672215!3e0?hl=ru"
    request = s.get(url)
    html = request.content
    soup = str(BeautifulSoup(html, 'html.parser'))
    h = soup.find('мин.') + 3
    t = soup[h:].find('мин.')
    time_bus = int(soup[h + t - 3:h + t - 1])  # время в пути до элки
    answer_2 = """\n\nВремя в пути на автобусе составит: {} минут\n\n""".format(time_bus)  # время на дорогу
    time_2 = []  # общее время (ИТОГ) время прибытия в Одинцово
    abc = datetime.datetime.now()

    for item in range(len(time_1)):  # создается список time_1(4)
        time_2.append(time_1[item] + datetime.timedelta(minutes=time_bus) + abc)

    answer_3 = "Прибытие в Одинцово:\n"
    for i in range(len(time_1)):
        qwerty = """В {} случае:  {} \n""".format(i + 1, (str(time_2[i]).replace('.', ' ')).split()[1])
        answer_3 = answer_3 + qwerty

    answer_2 = answer_2 + answer_3 + '\n'
    # print(answer_2)
    # return answer_2, time_2
    ########################################################
    abc = datetime.datetime.now()
    abc = (str(abc)).split()[0]
    url = 'https://api.rasp.yandex.net/v3.0/search/?apikey=af3262d1-dd33-4e7d-9361-0bad820d9ff2&format=json&from=c10743&to=s9601666&lang=ru_RU&page=1&date={}&transport_types'.format(
        abc)
    res = requests.get(url)
    res = res.json()
    suburban = pd.read_csv('bot.csv')

    f = 0
    for i in res['segments']:
        id = f
        departure = i['from']['title']
        arrival = i['to']['title']
        trip = i['thread']['title']
        time_departure = pd.to_datetime(i['departure'].replace('+03:00', ''))
        time_arrival = pd.to_datetime(i['arrival'].replace('+03:00', ''))
        travel_time = time_arrival - time_departure
        stops = i['stops']
        comfort = i['thread']['transport_subtype']['title']
        record = {
            'id': id,
            'departure': departure,
            'arrival': arrival,
            'trip': trip,
            'time_departure': time_departure,
            'time_arrival': time_arrival,
            'travel_time': travel_time,
            'stops': stops,
            'comfort': comfort
        }

        suburban = suburban.append(record, ignore_index=True)
        f = f + 1

        answer_3 = ''
        time_3 = []
        # print(time_2)
    abc = datetime.datetime.now()
    for item in range(len(time_2)):
        between = suburban[suburban['time_departure'] > time_2[item]].iloc[:len(time_2)]
        if between.empty:
            return 'Электричек с Одинцово на Беговую нет'
        qwerty = """Trip: {}\nDepurture_time: {}\nArrival_time: {}\nTravel_time: {}\ncomfort: {}\ntime_out: {}\n\n """.format(
            between.trip.iloc[0],
            str(between.time_departure.iloc[item]).split()[1],
            str(between.time_arrival.iloc[item]).split()[1],
            str(between.travel_time.iloc[0]).split()[2], between.comfort.iloc[0],
            (str(between.time_departure.iloc[item] - abc)).replace('.', ' ').split()[2])
        answer_3 = answer_3 + qwerty

        # time_3.append(str(between.time_arrival.iloc[0]).split()[2])
        time_3.append(str(between.time_arrival.iloc[item]))

        # print(answer_3)
    # return answer_3 , time_3, suburban
    for i in range(len(time_3)):
        time_3[i] = datetime.datetime.strptime(time_3[i], "%Y-%m-%d %H:%M:%S")
        # print(time[i])
        time_3[i] = time_3[i] + datetime.timedelta(minutes=20)

    answer1 = "Прибытие в библиотеку\n"
    for i in range(len(time_3)):
        qwerty = """В {} случае:  {} \n""".format(i + 1, (str(time_3[i]).replace('.', ' ')).split()[1])
        answer1 = answer1 + qwerty

    if answer_1 == 'Автобус будет на остановке:':
        return 'Вся спят уже, зачем тебе в такую ночь куда то ехать!?'
    return answer_1 + answer_2 + answer_3 + answer1

def lubyanka_hostel():
    abc = datetime.datetime.now()
    abc = (str(abc)).split()[0]
    url = 'https://api.rasp.yandex.net/v3.0/search/?apikey=af3262d1-dd33-4e7d-9361-0bad820d9ff2&format=json&from=s9601666&to=c10743&lang=ru_RU&page=1&date={}&transport_types'.format(
        abc)
    res = requests.get(url)
    res = res.json()
    suburban = pd.read_csv('bot.csv')

    f = 0
    for i in res['segments']:
        id = f
        departure = i['from']['title']
        arrival = i['to']['title']
        trip = i['thread']['title']
        time_departure = pd.to_datetime(i['departure'].replace('+03:00', ''))
        time_arrival = pd.to_datetime(i['arrival'].replace('+03:00', ''))
        travel_time = time_arrival - time_departure
        stops = i['stops']
        comfort = i['thread']['transport_subtype']['title']
        record = {
            'id': id,
            'departure': departure,
            'arrival': arrival,
            'trip': trip,
            'time_departure': time_departure,
            'time_arrival': time_arrival,
            'travel_time': travel_time,
            'stops': stops,
            'comfort': comfort
        }

        suburban = suburban.append(record, ignore_index=True)
        f = f + 1

        answer_3 = ''
        time_3 = []
        # print(time_2)
    abc = datetime.datetime.now()
    between = suburban[suburban['time_departure'] > abc + datetime.timedelta(minutes=20)].iloc[:2]
    for item in range(len(between)):
        qwerty = """Trip: {}\nDepurture_time: {}\nArrival_time: {}\nTravel_time: {}\ncomfort: {}\ntime_out: {}\n\n """.format(
            between.trip.iloc[item],
            str(between.time_departure.iloc[item]).split()[1],
            str(between.time_arrival.iloc[item]).split()[1],
            str(between.travel_time.iloc[item]).split()[2], between.comfort.iloc[item],
            (str(between.time_departure.iloc[item] - abc)).replace('.', ' ').split()[2])
        answer_3 = answer_3 + qwerty

        # time_3.append(str(between.time_arrival.iloc[0]).split()[2])
        time_3.append(str(between.time_arrival.iloc[item]))
    # print(time_3)
    # print(answer_3)

    for i in range(len(time_3)):
        time_3[i] = datetime.datetime.strptime(time_3[i], "%Y-%m-%d %H:%M:%S")
        # print(time[i])
        time_3[i] = time_3[i] + datetime.timedelta(minutes=5)

    bus = DataFrame(columns=('id', 'departure_bus'))
    num = ['Первый', 'Второй', 'Третий', 'Четвертый']
    id = 0
    departure_bus = ['00:30:00', '01:23:00', '09:05:00', '09:55:00', '10:35:00', '10:50:00', '11:55:00', '12:10:00',
                     '13:57:00', '15:28:00', '16:12:00', '16:32:00', '16:57:00',
                     '17:25:00', '17:45:00', '18:35:00', '19:18:00', '19:43:00', '20:14:00', '20:38:00',
                     '20:55:00',
                     '21:20:00', '21:45:00', '22:06:00', '22:30:00', '23:19:00', '23:53:00']  # будни
    for item in departure_bus:  # создает DataFrame (расписание)
        item = pd.to_datetime(item)
        record = {
            'id': id,
            'departure_bus': item,
        }
        bus = bus.append(record, ignore_index=True)
        id = id + 1

    s = requests.Session()
    s.headers.update({
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'
    })

    url = "https://www.google.com/maps/dir/55.6727759,37.2811436/55.6604795,37.2274338/@55.6630984,37.2454733,14.21z/data=!4m2!4m1!3e0?hl=ru"
    request = s.get(url)
    html = request.content
    soup = str(BeautifulSoup(html, 'html.parser'))
    h = soup.find('мин.') + 3
    t = soup[h:].find('мин.')
    try:
        time_bus = int(soup[h + t - 3:h + t - 1])  # время в пути до элки
    except Exception as e:
        print(e)
        time_bus = int(soup[h + t - 2:h + t - 1])

    abc = datetime.datetime.now()  # настоящее времся
    time_1 = []
    s = ''
    solution = ''
    solution_1 = ''
    help = '\n'
    for item in range(len(time_3)):
        r = bus[bus['departure_bus'] > time_3[item]].iloc[:4]
        answer_1 = '{} Автобус будет на остановке:\n'.format(item + 1)  # Выыодит пользователю времени ожидания автобуса
        answer_4 = "{} Прибытие в Дубки:\n".format(item + 1)
        qwerty = ''
        sas = ''
        for i in range(len(r)):
            s = ''' {} через: {} \n'''.format(num[i], (str(r.departure_bus.iloc[i] - abc)).replace('.', ' ').split()[2])
            s_dub = """В {} случае:  {} \n""".format(num[i], (
                str(r.departure_bus.iloc[i] + datetime.timedelta(minutes=time_bus))).replace('.', ' ').split()[1])
            qwerty = qwerty + s_dub
            sas = sas + s
        solution = solution + answer_1 + sas + help
        solution_1 = solution_1 + answer_4 + qwerty + help
        # print(solution)

    answer_2 = """\n\nВремя в пути на автобусе составит: {} минут\n\n""".format(time_bus)  # время на дорогу

    return (answer_3 + solution + answer_2 + solution_1)

def hostel_rest():
    bus = DataFrame(columns=('id', 'departure_bus'))
    num = ['Первый', 'Второй', 'Третий', 'Четвертый']
    id = 0
    departure_bus = ['06:45:00', '07:10:00', '07:30:00', '07:50:00', '08:05:00', '08:30:00', '08:45:00', '09:05:00',
                     '09:35:00',
                     '10:15:00', '10:30:00', '11:32:00', '11:50:00', '13:25:00', '15:05:00', '15:50:00', '16:12:00',
                     '16:40:00',
                     '17:05:00', '17:25:00', '18:11:00', '18:55:00', '19:20:00', '19:50:00', '20:16:00', '20:35:00',
                     '21:00:00',
                     '21:25:00', '21:50:00', '22:10:00', '22:59:00']  # будни
    for item in departure_bus:  # создает DataFrame (расписание)
        item = pd.to_datetime(item)
        record = {
            'id': id,
            'departure_bus': item,
        }
        bus = bus.append(record, ignore_index=True)
        id = id + 1

    abc = datetime.datetime.now()  # настоящее времся
    r = bus[bus['departure_bus'] > abc].iloc[:3]

    time_1 = []  # Время до приезда автобуса
    for item in range(len(r)):  # создается список time_1(4)
        time_1.append(r.departure_bus.iloc[item] - abc)

    s = ''
    answer_1 = '\tАвтобус будет на остановке:\n'  # Выыодит пользователю времени ожидания автобуса
    for date in num[:len(r)]:
        s = ''' {} через: {} час и {} минут \n'''.format(date, str(time_1[num.index(date)])[8:9],
                                                         str(time_1[num.index(date)])[10:12])
        answer_1 = answer_1 + s
        #################################################################
    s = requests.Session()
    s.headers.update({
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'
    })

    url = "https://www.google.com/maps/dir/55.6594766,37.2283472/%D1%81%D1%82.%D0%9E%D0%B4%D0%B8%D0%BD%D1%86%D0%BE%D0%B2%D0%BE,+%D0%9E%D0%B4%D0%B8%D0%BD%D1%86%D0%BE%D0%B2%D0%BE/@55.6692156,37.2233307,13z/data=!3m1!4b1!4m9!4m8!1m0!1m5!1m1!1s0x46b5504c19aefc9f:0x434d5634cfcc75ef!2m2!1d37.281235!2d55.672215!3e0?hl=ru"
    request = s.get(url)
    html = request.content
    soup = str(BeautifulSoup(html, 'html.parser'))
    h = soup.find('мин.') + 3
    t = soup[h:].find('мин.')
    time_bus = int(soup[h + t - 3:h + t - 1])  # время в пути до элки
    answer_2 = """\n\nВремя в пути на автобусе составит: {} минут\n\n""".format(time_bus)  # время на дорогу
    time_2 = []  # общее время (ИТОГ) время прибытия в Одинцово
    abc = datetime.datetime.now()

    for item in range(len(time_1)):  # создается список time_1(4)
        time_2.append(time_1[item] + datetime.timedelta(minutes=time_bus) + abc)

    answer_3 = "Прибытие в Одинцово:\n"
    for i in range(len(time_1)):
        qwerty = """В {} случае:  {} \n""".format(i + 1, (str(time_2[i]).replace('.', ' ')).split()[1])
        answer_3 = answer_3 + qwerty

    answer_2 = answer_2 + answer_3 + '\n'
    # print(answer_2)
    # return answer_2, time_2
    ########################################################
    abc = datetime.datetime.now()
    abc = (str(abc)).split()[0]
    url = 'https://api.rasp.yandex.net/v3.0/search/?apikey=af3262d1-dd33-4e7d-9361-0bad820d9ff2&format=json&from=c10743&to=s9601666&lang=ru_RU&page=1&date={}&transport_types'.format(
        abc)
    res = requests.get(url)
    res = res.json()
    suburban = pd.read_csv('bot.csv')

    f = 0
    for i in res['segments']:
        id = f
        departure = i['from']['title']
        arrival = i['to']['title']
        trip = i['thread']['title']
        time_departure = pd.to_datetime(i['departure'].replace('+03:00', ''))
        time_arrival = pd.to_datetime(i['arrival'].replace('+03:00', ''))
        travel_time = time_arrival - time_departure
        stops = i['stops']
        comfort = i['thread']['transport_subtype']['title']
        record = {
            'id': id,
            'departure': departure,
            'arrival': arrival,
            'trip': trip,
            'time_departure': time_departure,
            'time_arrival': time_arrival,
            'travel_time': travel_time,
            'stops': stops,
            'comfort': comfort
        }

        suburban = suburban.append(record, ignore_index=True)
        f = f + 1

        answer_3 = ''
        time_3 = []
        # print(time_2)
    abc = datetime.datetime.now()
    for item in range(len(time_2)):
        between = suburban[suburban['time_departure'] > time_2[item]].iloc[:len(time_2)]
        if between.empty:
            return 'Электричек с Одинцово на Беговую нет'
        qwerty = """Trip: {}\nDepurture_time: {}\nArrival_time: {}\nTravel_time: {}\ncomfort: {}\ntime_out: {}\n\n """.format(
            between.trip.iloc[0],
            str(between.time_departure.iloc[item]).split()[1],
            str(between.time_arrival.iloc[item]).split()[1],
            str(between.travel_time.iloc[0]).split()[2], between.comfort.iloc[0],
            (str(between.time_departure.iloc[item] - abc)).replace('.', ' ').split()[2])
        answer_3 = answer_3 + qwerty

        # time_3.append(str(between.time_arrival.iloc[0]).split()[2])
        time_3.append(str(between.time_arrival.iloc[item]))

        # print(answer_3)
    # return answer_3 , time_3, suburban
    for i in range(len(time_3)):
        time_3[i] = datetime.datetime.strptime(time_3[i], "%Y-%m-%d %H:%M:%S")
        # print(time[i])
        time_3[i] = time_3[i] + datetime.timedelta(minutes=35)

    answer1 = "Прибытие на Выхино\n"
    for i in range(len(time_3)):
        qwerty = """В {} случае:  {} \n""".format(i + 1, (str(time_3[i]).replace('.', ' ')).split()[1])
        answer1 = answer1 + qwerty

    abc = datetime.datetime.now()
    abc = (str(abc)).split()[0]
    url = 'https://api.rasp.yandex.net/v3.0/search/?apikey=af3262d1-dd33-4e7d-9361-0bad820d9ff2&format=json&from=s9601627&to=s9602223&lang=ru_RU&page=1&date={}&transport_types'.format(
        abc)
    res = requests.get(url)
    res = res.json()
    suburban = pd.read_csv('bot.csv')

    f = 0
    for i in res['segments']:
        id = f
        departure = i['from']['title']
        arrival = i['to']['title']
        trip = i['thread']['title']
        time_departure = pd.to_datetime(i['departure'].replace('+03:00', ''))
        time_arrival = pd.to_datetime(i['arrival'].replace('+03:00', ''))
        travel_time = time_arrival - time_departure
        stops = i['stops']
        comfort = i['thread']['transport_subtype']['title']
        record = {
            'id': id,
            'departure': departure,
            'arrival': arrival,
            'trip': trip,
            'time_departure': time_departure,
            'time_arrival': time_arrival,
            'travel_time': travel_time,
            'stops': stops,
            'comfort': comfort
        }

        suburban = suburban.append(record, ignore_index=True)
        f = f + 1

    answer_6 = ''
    time_6 = []
    # print(time_2)
    abc = datetime.datetime.now()
    for item in range(len(time_3)):
        between = suburban[suburban['time_departure'] > time_3[item]].iloc[:len(time_3)]
        qwerty = """Trip: {}\nDepurture_time: {}\nArrival_time: {}\nTravel_time: {}\ncomfort: {}\ntime_out: {}\n\n """.format(
            between.trip.iloc[0],
            str(between.time_departure.iloc[item]).split()[1],
            str(between.time_arrival.iloc[item]).split()[1],
            str(between.travel_time.iloc[0]).split()[2], between.comfort.iloc[0],
            (str(between.time_departure.iloc[item] - abc)).replace('.', ' ').split()[2])
        answer_6 = answer_6 + qwerty

        # time_3.append(str(between.time_arrival.iloc[0]).split()[2])
        time_6.append(str(between.time_arrival.iloc[item]))

    answer789 = "Прибытие на станцию Отдых:\n"
    for i in range(len(time_6)):
        qwerty = """В {} случае:  {} \n""".format(i + 1, (str(time_6[i]).replace('.', ' ')).split()[1])
        answer789 = answer789 + qwerty

    return(answer_1 + answer_2 + answer_3 + answer1 + answer_6 + answer789)


def rest_odin():
    abc = datetime.datetime.now()
    abc = (str(abc)).split()[0]
    url = 'https://api.rasp.yandex.net/v3.0/search/?apikey=af3262d1-dd33-4e7d-9361-0bad820d9ff2&format=json&from=s9602223&to=s9601627&lang=ru_RU&page=1&date={}&transport_types'.format(
        abc)
    res = requests.get(url)
    res = res.json()
    suburban = pd.read_csv('bot.csv')

    f = 0
    for i in res['segments']:
        id = f
        departure = i['from']['title']
        arrival = i['to']['title']
        trip = i['thread']['title']
        time_departure = pd.to_datetime(i['departure'].replace('+03:00', ''))
        time_arrival = pd.to_datetime(i['arrival'].replace('+03:00', ''))
        travel_time = time_arrival - time_departure
        stops = i['stops']
        comfort = i['thread']['transport_subtype']['title']
        record = {
            'id': id,
            'departure': departure,
            'arrival': arrival,
            'trip': trip,
            'time_departure': time_departure,
            'time_arrival': time_arrival,
            'travel_time': travel_time,
            'stops': stops,
            'comfort': comfort
        }

        suburban = suburban.append(record, ignore_index=True)
        f = f + 1
        #time_6.append(str(between.time_arrival.iloc[item]))

    answer_3 = ''
    time_3 = []
    # print(time_2)

    abc = datetime.datetime.now()
    between = suburban[suburban['time_departure'] > abc].iloc[:4]
    for item in range(len(between)):
        qwerty = """Trip: {}\nDepurture_time: {}\nArrival_time: {}\nTravel_time: {}\ncomfort: {}\ntime_out: {}\n\n """.format(
            between.trip.iloc[item], str(between.time_departure.iloc[item]).split()[1],
            str(between.time_arrival.iloc[item]).split()[1],
            str(between.travel_time.iloc[item]).split()[2], between.comfort.iloc[item],
            (str(between.time_departure.iloc[item] - abc)).replace('.', ' ').split()[2])
        print(qwerty)
        answer_3 = answer_3 + qwerty

        time_3.append(str(between.time_arrival.iloc[item]))

    answer789 = "Прибытие на станцию Отдых:\n"
    for i in range(len(time_3)):
        qwerty = """В {} случае:  {} \n""".format(i + 1, (str(time_3[i]).replace('.', ' ')).split()[1])
        answer789 = answer789 + qwerty

    for i in range(len(time_3)):
        time_3[i] = datetime.datetime.strptime(time_3[i], "%Y-%m-%d %H:%M:%S")
        # print(time[i])
        time_3[i] = time_3[i] + datetime.timedelta(minutes=35)

    abc = datetime.datetime.now()
    abc = (str(abc)).split()[0]
    url = 'https://api.rasp.yandex.net/v3.0/search/?apikey=af3262d1-dd33-4e7d-9361-0bad820d9ff2&format=json&from=s9601666&to=c10743&lang=ru_RU&page=1&date={}&transport_types'.format(
        abc)
    res = requests.get(url)
    res = res.json()
    suburban = pd.read_csv('bot.csv')

    f = 0
    for i in res['segments']:
        id = f
        departure = i['from']['title']
        arrival = i['to']['title']
        trip = i['thread']['title']
        time_departure = pd.to_datetime(i['departure'].replace('+03:00', ''))
        time_arrival = pd.to_datetime(i['arrival'].replace('+03:00', ''))
        travel_time = time_arrival - time_departure
        stops = i['stops']
        comfort = i['thread']['transport_subtype']['title']
        record = {
            'id': id,
            'departure': departure,
            'arrival': arrival,
            'trip': trip,
            'time_departure': time_departure,
            'time_arrival': time_arrival,
            'travel_time': travel_time,
            'stops': stops,
            'comfort': comfort
        }

        suburban = suburban.append(record, ignore_index=True)
        f = f + 1

    answer_6 = ''
    time_6 = []
    # print(time_2)
    abc = datetime.datetime.now()
    for item in range(len(time_3)):
        between = suburban[suburban['time_departure'] > time_3[item]].iloc[:len(time_3)]
        qwerty = """Trip: {}\nDepurture_time: {}\nArrival_time: {}\nTravel_time: {}\ncomfort: {}\ntime_out: {}\n\n """.format(
            between.trip.iloc[0],
            str(between.time_departure.iloc[item]).split()[1],
            str(between.time_arrival.iloc[item]).split()[1],
            str(between.travel_time.iloc[0]).split()[2], between.comfort.iloc[0],
            (str(between.time_departure.iloc[item] - abc)).replace('.', ' ').split()[2])
        answer_6 = answer_6 + qwerty

        # time_3.append(str(between.time_arrival.iloc[0]).split()[2])
        time_6.append(str(between.time_arrival.iloc[item]))

    answer7 = "Прибытие на станцию Одинцово:\n"
    for i in range(len(time_6)):
        qwerty = """В {} случае:  {} \n""".format(i + 1, (str(time_6[i]).replace('.', ' ')).split()[1])
        answer7 = answer7 + qwerty

    return(answer_3 + answer789 + answer_6 + answer7)






