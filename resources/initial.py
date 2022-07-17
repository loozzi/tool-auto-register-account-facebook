from ppadb.client import Client as AdbClient
import time
from datetime import datetime
import json
import os
from threading import Thread


with open("./configs/points.json", 'r') as f:
    points = json.load(f)

with open("./configs/settings.json", 'r') as f:
    settings = json.load(f)

with open("./configs/information.json", 'r', encoding='utf-8') as f:
    listName = json.load(f)


pathApplication = "../storages"
pathLdPlayer = settings['ld-path']

packageWarp = 'com.cloudflare.onedotonedotonedotone'
packageLite = 'com.facebook.lite'

pointsWarp = points['warp']
pointsLite = points['lite']
pointsKeyboardNumber = points['keyboards-number']

d1 = settings['delay1']
d2 = settings['delay2']
d3 = settings['delay3']
d4 = settings['delay4']

numEmulator = settings['number-emulator']
firstPhoneNumber = settings['phone-number']
passwordLength = settings['password-length']
numLoop = settings['number-loop']

language = settings['lang']
