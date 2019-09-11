# -*- coding: utf-8 -*-
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import vk_api
from datetime import datetime
import random
import time
import search
import trip
# import get_pictures

#login, password='login','password'
# vk_session = vk_api.VkApi(login, password)
# vk_session.auth()
token ='8a38ef5ecee5252436d65da1f6722978e8785fd0b67a6d9843fa162aa99ac2208e75a10dc515895143ddb'
vk_session = vk_api.VkApi(token=token)

# session_api = vk_session.get_api()
# longpoll = VkLongPoll(vk_session)

def check(vk_session):
    longpoll = VkLongPoll(vk_session)
    return longpoll

try:
    longpoll = check(vk_session)
except Exception as e:
    print(e)
    time.sleep(5)


def create_keyboard(response):
    keyboard = VkKeyboard(one_time=False)

    if response == 'weather' :

        keyboard.add_button('Weather in Moscow', color=VkKeyboardColor.POSITIVE)
        keyboard.add_button('Weather in Lyubertsy', color=VkKeyboardColor.POSITIVE)

        keyboard.add_line()  # Переход на вторую строку
        keyboard.add_button('Weather in Odintsovo', color=VkKeyboardColor.POSITIVE)
        keyboard.add_button('Weather in Stavropol', color=VkKeyboardColor.POSITIVE)

        keyboard.add_line()
        keyboard.add_button('To main menu', color=VkKeyboardColor.NEGATIVE)

        # keyboard.add_line()
        # keyboard.add_button('Синяя кнопка', color=VkKeyboardColor.PRIMARY)
        # keyboard.add_button('Привет', color=VkKeyboardColor.PRIMARY)

    elif response == 'trip':
        keyboard.add_button('Hostel - MIEM', color=VkKeyboardColor.PRIMARY)
        keyboard.add_button('Odintsovo - MIEM', color=VkKeyboardColor.PRIMARY)

        keyboard.add_line()
        keyboard.add_button('Hostel - Odintsovo', color=VkKeyboardColor.PRIMARY)
        keyboard.add_button('Odintsovo - Hostel', color=VkKeyboardColor.PRIMARY)

        keyboard.add_line()
        keyboard.add_button('Hostel - Slav', color=VkKeyboardColor.PRIMARY)
        keyboard.add_button('Slav - Hostel', color=VkKeyboardColor.PRIMARY)

        keyboard.add_line()
        keyboard.add_button('Hostel - Lubyanka', color=VkKeyboardColor.PRIMARY)
        keyboard.add_button('Lubyanka - Hostel', color=VkKeyboardColor.PRIMARY)

        keyboard.add_line()
        keyboard.add_button('Hostel - Rest', color=VkKeyboardColor.PRIMARY)
        keyboard.add_button('Rest - Odintsovo', color=VkKeyboardColor.PRIMARY)

        keyboard.add_line()
        keyboard.add_button('To main menu', color=VkKeyboardColor.NEGATIVE)

    elif response == "weather in moscow" or response == "weather in odintsovo" or response == "weather in lyubertsy" or response == "weather in stavropol":

        keyboard.add_button('3', color=VkKeyboardColor.PRIMARY)
        keyboard.add_button('6', color=VkKeyboardColor.PRIMARY)

        keyboard.add_line()
        keyboard.add_button('9', color=VkKeyboardColor.PRIMARY)
        keyboard.add_button('12', color=VkKeyboardColor.PRIMARY)

        keyboard.add_line()
        keyboard.add_button('To main menu', color=VkKeyboardColor.NEGATIVE)



    elif response == 'hello' or response == 'start' or 'to main menu':
        keyboard.add_button('Weather', color=VkKeyboardColor.POSITIVE)
        keyboard.add_button('Trip', color=VkKeyboardColor.POSITIVE)

    elif response == 'close':
        print('close keyboard')
        return keyboard.get_empty_keyboard()

    keyboard = keyboard.get_keyboard()
    return keyboard


def send_message(vk_session, id_type, id, message=None, attachment=None, keyboard=None):
    vk_session.method('messages.send',{id_type: id, 'message': message, 'random_id': random.randint(-2147483648, +2147483648),
                                       "attachment": attachment, 'keyboard': keyboard})


while True:
    try:
        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW:
                print('The message came in: ' + str(datetime.strftime(datetime.now(), "%H:%M:%S")))
                print('Message text: ' + str(event.text))
                print(event.user_id)
                response = event.text.lower()
                keyboard = create_keyboard(response)

                if response == 'weather in moscow':
                    copy = 1
                if response == 'weather in lyubertsy':
                    copy = 2
                if response == 'weather in odintsovo':
                    copy = 3
                if response == 'weather in stavropol':
                    copy = 4

                if event.from_user and not event.from_me:

                    if response == 'hello' or response == 'start' or response == 'to main menu':
                        send_message(vk_session, 'user_id', event.user_id, message="Hi, well, let's get started =)",keyboard=keyboard)
                    elif response == 'trip':
                        send_message(vk_session, 'user_id', event.user_id, message='Select a destination',keyboard=keyboard)
                    elif response == 'weather':
                        send_message(vk_session, 'user_id', event.user_id, message='Choose the weather',keyboard=keyboard)


                    elif response == "weather in moscow" or response == "weather in odintsovo" or response == "weather in lyubertsy" or response == "weather in stavropol":
                        send_message(vk_session, 'user_id', event.user_id, message='Select the number of hours',keyboard=keyboard)

                    elif (response == '3' or response == '6' or response == '9' or response == '12') and copy == 1: #Москва
                        if response == '3':
                            dude = search.weather('weather in moscow', 3)
                        elif response == '6':
                            dude = search.weather('weather in moscow', 6)
                        elif response == '9':
                            dude = search.weather('weather in moscow', 9)
                        elif response == '12':
                            dude = search.weather('weather in moscow', 12)
                        for i in dude:
                            send_message(vk_session, 'user_id', event.user_id, message=i)

                    elif (response == '3' or response == '6' or response == '9' or response == '12') and copy == 2: #Люберцы
                        if response == '3':
                            dude = search.weather('weather in lyubertsy', 3)
                        elif response == '6':
                            dude = search.weather('weather in lyubertsy', 6)
                        elif response == '9':
                            dude = search.weather('weather in lyubertsy', 9)
                        elif response == '12':
                            dude = search.weather('weather in lyubertsy', 12)
                        for i in dude:
                            send_message(vk_session, 'user_id', event.user_id, message=i)

                    elif (response == '3' or response == '6' or response == '9' or response == '12') and copy == 3: #Одинцово
                        if response == '3':
                            dude = search.weather('weather in odintsovo', 3)
                        elif response == '6':
                            dude = search.weather('weather in odintsovo', 6)
                        elif response == '9':
                            dude = search.weather('weather in odintsovo', 9)
                        elif response == '12':
                            dude = search.weather('weather in odintsovo', 12)
                        for i in dude:
                            send_message(vk_session, 'user_id', event.user_id, message=i)

                    elif (response == '3' or response == '6' or response == '9' or response == '12') and copy == 4: #Ставрополе
                        if response == '3':
                            dude = search.weather('weather in stavropol', 3)
                        elif response == '6':
                            dude = search.weather('weather in stavropol', 6)
                        elif response == '9':
                            dude = search.weather('weather in stavropol', 9)
                        elif response == '12':
                            dude = search.weather('weather in stavropol', 12)
                        for i in dude:
                            send_message(vk_session, 'user_id', event.user_id, message=i)
                    elif response == 'hostel - odintsovo':
                        hostel_odin = trip.hostel_odin()
                        send_message(vk_session, 'user_id', event.user_id, message=hostel_odin)
                    elif response == 'odintsovo - miem':
                        odin_miem = trip.odinsovo_miem()
                        send_message(vk_session, 'user_id', event.user_id, message=odin_miem)
                    elif response == 'hostel - miem':
                        hostel_miem = trip.hostel_miem()
                        send_message(vk_session, 'user_id', event.user_id, message=hostel_miem)
                    elif response == 'odintsovo - hostel':
                        odin_hostel = trip.odin_hostel()
                        send_message(vk_session, 'user_id', event.user_id, message=odin_hostel)
                    elif response == 'slav - hostel':
                        slavynka_hostel = trip.slav_hostel()
                        send_message(vk_session, 'user_id', event.user_id, message=slavynka_hostel)
                    elif response == 'hostel - slav':
                        hostel_slavynka = trip.hostel_slav()
                        send_message(vk_session, 'user_id', event.user_id, message=hostel_slavynka)
                    elif response == 'hostel - lubyanka':
                        hos_lubyanka = trip.hostel_lubyanka()
                        send_message(vk_session, 'user_id', event.user_id, message=hos_lubyanka)
                    elif response == 'lubyanka - hostel':
                        lub_hos = trip.lubyanka_hostel()
                        send_message(vk_session, 'user_id', event.user_id, message=lub_hos)
                    elif response == 'hostel - rest':
                        hos_res = trip.hostel_rest()
                        send_message(vk_session, 'user_id', event.user_id, message=hos_res)
                    elif response == 'rest - odintsovo':
                        rest_host = trip.rest_odin()
                        send_message(vk_session, 'user_id', event.user_id, message=rest_host)

                    elif response=='close':
                        send_message(vk_session, 'user_id', event.user_id, message='Close',keyboard=keyboard)
    except Exception as e:
        print('Error:', e)
