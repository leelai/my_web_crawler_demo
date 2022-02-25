import logging
import requests
from bs4 import BeautifulSoup
import re
import utils
#https://www.csh.com.tw/Register/QueryRegister.aspx
baseUrl = 'https://www.country.org.tw'
openUrl = baseUrl + '/就醫指南/掛號查詢'
# queryUrl = baseUrl + '/appointment'
queryUrl = baseUrl + '/apptRecord'

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

def checking(name, id):
  store_list = []
  s = requests.Session()
  try:
    x = s.get(baseUrl, headers = headers, timeout = utils.timeout)
    soup2 = BeautifulSoup(x.text, 'html.parser')
    # print(soup2.prettify())
    meta = soup2.find_all('meta', {'name': 'csrf-token'})
    token = meta[0]['content']
    # print(token)
    # print(s.cookies.get_dict())
    utils.delay()
    # x = s.get(openUrl, timeout = utils.timeout) #有這個cookie才有 ASP.NET_SessionId
    # utils.delay()
    myobj = {'id':id, '_token': token } #{'id': id}
    res = s.post(queryUrl,data = myobj, timeout = utils.timeout)
    soup2 = BeautifulSoup(res.text, 'html.parser')
    # print(soup2.prettify())
    divs = soup2.find_all('div', {'class': 'card my-2'})
    # print(divs)
    for div in divs:
      # print(div)
      # print('==================')

      data = div.find('div', {'class': 'card-header text-white bg-primary'})
      data = data.text.strip().replace(' ', '').split('\r\n')
      date = data[0]
      store = data[2]
      # print(date)
      # print(store)
      p = div.find_all('p', {'class': 'title-border-left pl-2'})
      name = p[1].text.strip().replace(' ', '').split('：')[1]
      # print(name)
      app = p[2].text.strip().replace(' ', '').split('：')[1]
      # print(app)

      p2 = div.find('p', {'class': 'title-border-left pl-2 mb-0'})
      time = p2.text.strip().replace(' ', '').split('：')[1]
    # print(time)
    # if tables == None:
    #   return store_list
    # if len(tables) < 1:
    #   return store_list

    # # print(tables[1].prettify())
    # table = tables[1]
    # # if table == None:
    # #   return store_list

    # trs = table.find_all('tr')
      store_details = {"姓名":name, "身份證": id, "日期":None, "科別診室":None, "診號": None, '地點': None, "候診參考時間": None, "醫院": '宏恩綜合醫院'}

    # tds = trs[0].find_all('td')
      store_details['日期'] = date
    # tds = trs[1].find_all('td')
    # store_details['日期'] = store_details['日期'] + tds[1].text.strip().replace(' ', '')

    # tds = trs[2].find_all('td')
      store_details['科別診室'] = store
    # tds = trs[4].find_all('td')
    # store_details['科別診室'] =  store_details['科別診室'] + '/' + tds[1].text.strip().replace(' ', '')
    # store_details['地點'] = store_details['科別診室']

    # tds = trs[5].find_all('td')
      store_details['診號'] = app
    # tds = trs[6].find_all('td')
      store_details['候診參考時間'] = time
      #print(store_details)
      store_list.append(store_details)
  except Exception as e:
    print('http error (' + name + ' ' + id + ' 宏恩綜合醫院 )' + str(e))
  # print(store_list)
  return store_list
# print(checking('test', 'A124365349', '19780210'))