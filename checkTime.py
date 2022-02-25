import logging
import requests
import json
from getmac import get_mac_address as gma

currentNetworkTime = 'http://worldtimeapi.org/api/timezone/Asia/Taipei' #http://worldclockapi.com/api/json/utc/now'
headers = {
'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'
}

macs = ["e4:a4:71:04:6b:36", "a0:78:17:73:f4:61", "90:e8:68:16:ae:a9"]

def canIUse():
    mac = gma()
    logging.info(mac)
    isMatch = False
    for it in macs:
        if mac == it:
            isMatch = True

    if isMatch == False:
        return False

    time = requests.get(currentNetworkTime, headers = headers)

    y = json.loads(time.text)
    return int(y["unixtime"]) < 1648741383
