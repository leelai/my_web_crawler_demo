import logging
import requests
from bs4 import BeautifulSoup
import re
import utils
#https://www.csh.com.tw/Register/QueryRegister.aspx
baseUrl = 'https://www.tahsda.org.tw'
openUrl = baseUrl + '/Register/delete.php'
queryUrl = baseUrl + '/Register/qry_delete.php'

headers = {
  'Cache-Control': 'max-age=0',
  'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="97", "Chromium";v="97"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"macOS"',
  'Upgrade-Insecure-Requests': '1',
  'Connection': 'keep-alive',
  'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36',
  'Content-Type': 'application/x-www-form-urlencoded',
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
  'Sec-Fetch-Site': 'none',
  'Sec-Fetch-Mode': 'navigate',
  'Sec-Fetch-User': '?1',
  'Sec-Fetch-Dest': 'document',
  'Accept-Language': 'en-US,en;q=0.9,zh-TW;q=0.8,zh;q=0.7,zh-CN;q=0.6',
}

target = '"action", "'

def checking(name, id, year, month, day):
  store_list = []
  s = requests.Session()
  try:
    x = s.get(openUrl, headers = headers, timeout = utils.timeout) #有這個cookie才有 ASP.NET_SessionId
    utils.delay()
    myobj = {'PID': id, 'year': year, 'mon': month, 'day': day, 'Submit': '查詢', 'PhoneNum':'', 'IP':''}
    res = s.post(queryUrl, data = myobj, timeout = utils.timeout)
    soup2 = BeautifulSoup(res.text, 'html.parser')
    # print(soup2.prettify())
    tables = soup2.find_all('table', {'class': 'table table-striped table-bordered'})
    if tables == None:
      return store_list
    if len(tables) < 1:
      return store_list

    # print(tables[1].prettify())
    table = tables[1]
    # if table == None:
    #   return store_list

    trs = table.find_all('tr')
    store_details = {"姓名":name, "身份證": id, "日期":None, "科別診室":None, "診號": None, '地點': None, "候診參考時間": None, "醫院": '臺安醫院'}
    tds = trs[0].find_all('td')
    store_details['日期'] = tds[1].text.strip().replace(' ', '')
    tds = trs[1].find_all('td')
    store_details['日期'] = store_details['日期'] + tds[1].text.strip().replace(' ', '')

    tds = trs[2].find_all('td')
    store_details['科別診室'] = tds[1].text.strip().replace(' ', '')
    tds = trs[4].find_all('td')
    store_details['科別診室'] =  store_details['科別診室'] + '/' + tds[1].text.strip().replace(' ', '')
    store_details['地點'] = store_details['科別診室']

    tds = trs[5].find_all('td')
    store_details['診號'] = tds[1].text.strip().replace(' ', '')
    tds = trs[6].find_all('td')
    store_details['候診參考時間'] = tds[1].text.strip().replace(' ', '')
    store_list.append(store_details)
  except Exception as e:
    print('http error (' + name + ' ' + id + ' 臺安醫院 )' + str(e))
  # print(store_list)
  return store_list
# print(checking('test', 'A124365349', '19780210'))