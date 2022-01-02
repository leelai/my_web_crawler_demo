import logging
import requests
import json
from getmac import get_mac_address as gma

currentNetworkTime = 'http://worldtimeapi.org/api/timezone/Asia/Taipei' #http://worldclockapi.com/api/json/utc/now'
headers = {
'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'
}

def canIUse():
    mac = gma()
    logging.info(mac)
    if mac != 'a0:78:17:73:f4:61':
        return False

    time = requests.get(currentNetworkTime, headers = headers)

    y = json.loads(time.text)
    # print(y["unixtime"]) #2628288 + 1640928403 = 1643556691
    return int(y["unixtime"]) < 1643556691
