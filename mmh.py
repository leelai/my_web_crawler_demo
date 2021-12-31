import random
import time
import requests
from bs4 import BeautifulSoup

url = 'https://www.mmh.org.tw/check_registerdone.php'
area1 = 'tp'
area2 = 'ts'
headers = {
  'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
}

def checkingPriv(name, id, birth, area):
  myobj = {'workflag': 'checkreg', 'area': area, 'txtID': id, 'txtBirth':birth, 'txtwebword':''}
  x = requests.post(url, data = myobj, headers = headers)
  soup = BeautifulSoup(x.text, 'html.parser')
  area = soup.find('h2', {'class': False, 'id': False})

  store_list = []
  trs = soup.find_all('tr')
  for tr in trs:
    store_details = {"姓名":name, "身份證": id, "日期":None, "科別":None, "診室":None, "診號": None, "候診參考時間": None, '院區': area.string.strip(), "醫院": '馬偕紀念醫院'}
    td = tr.find('td', attrs={"data-title": "日期"})
    if td is not None:
      store_details['日期'] = td.string

    if td is None:
      continue

    td = tr.find('td', attrs={"data-title": "科別"})
    if td is not None:
      store_details['科別'] = td.string
    td = tr.find('td', attrs={"data-title": "診室"})
    if td is not None:
      store_details['診室'] = td.string
    td = tr.find('td', attrs={"data-title": "診號"})
    if td is not None:
      store_details['診號'] = td.string
    td = tr.find('td', attrs={"data-title": "候診參考時間"})
    if td is not None:
      store_details['候診參考時間'] = td.string
    store_list.append(store_details)
  return store_list

def checking(name, id, birth):
  ret1 = checkingPriv(name, id, birth, area1)
  time.sleep(random.uniform(1.0, 2.0))
  ret2 = checkingPriv(name, id, birth, area2)
  return ret1 + ret2