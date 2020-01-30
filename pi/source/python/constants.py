#!/usr/bin/python3

ARD_DEVICE_ID = "1"


LOGFILE = "./logs/smarthome.log"

# --- Unicodes --- #
USSR = '☭'
HOME = ' ⌂'
HOMEON = ' ☗'
KEY = ' ⚿'
CLOUD = ' ☁'
STAR = ' ★'
SUN = ' ☀'
REFRESH = ' 🗘'
CHECKED = ' ✔'
POINT = ' ☛'
MISSING = ' ✘'
MODESSYMBOL = ' ❖'
MENUSYMBOL = ' ☰'
TERMOMETER = ' 🌡'
MUSIC = ' ♫'
EMAIL = ' ✉'
NOTIFICATION = ' 🔔'
DEGREES = ' °C'
SMILE = ' ☺'
MOON = ' ☾'
QUATER_MOON = '☽'
PEACE = ' ☮'
WHITESTAR = ' ⚝'

# --- Arduino Serial Commands --- #
cmds = {
        'h': 'S>',
        'start': '01',
        'pwm': '02',
        'dio': '03',
        'adc': '04',
        'stop': '05',
        'trl':  '<E*'
        }


START_CMD = cmds['h'] + cmds['start'] + cmds['trl']
STOP_CMD = cmds['h'] + cmds['stop'] + cmds['trl']
ADC_CMD = cmds['h'] + cmds['adc'] + cmds['trl']

POSITIVE_RESPONSE = "Ok"

# --- Modes --- #

LIGHT_TRESHOLD = 400

