import logging
import requests
from bs4 import BeautifulSoup
import re
import utils

baseUrl = 'https://webreg.vghks.gov.tw'
queryUrl = baseUrl + '/wps/portal/web/querycancel'

headers = {
  'Cache-Control': 'max-age=0',
  'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"macOS"',
  'Origin': 'https://webreg.vghks.gov.tw',
  'Upgrade-Insecure-Requests': '1',
  'Connection': 'keep-alive',
  'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
  'Content-Type': 'application/x-www-form-urlencoded',
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
  'Sec-Fetch-Site': 'same-origin',
  'Sec-Fetch-Mode': 'navigate',
  'Sec-Fetch-User': '?1',
  'Sec-Fetch-Dest': 'document',
  'Accept-Language': 'en-US,en;q=0.9,zh-TW;q=0.8,zh;q=0.7,zh-CN;q=0.6'
}

cookies_dict = {"com.ibm.wps.state.preprocessors.locale.LanguageCookie": "zh_TW"}

target = '"action", "'

def checking(name, id, birth):
  store_list = []
  s = requests.Session()
  try:
    x = s.get(queryUrl, headers = headers, cookies = cookies_dict, timeout = utils.timeout)
    start = x.text.index(target) + 11
    end = x.text.index(');', start) - 1
    form = x.text[start:end]
    myobj = {'idType': 'RSHIDNO', 'id': id, 'dateOfBirth': birth}
    url = baseUrl + form
    utils.delay()
    res = s.post(url, data = myobj, timeout = utils.timeout)
    soup2 = BeautifulSoup(res.text, 'html.parser')
    table = soup2.find('table', {'class': 'clinic_tb'})

    if table == None:
      return store_list

    trs = table.find_all('tr')
    for tr in trs:
      if tr.text.find('選擇') >= 0:
        continue
      store_details = {"姓名":name, "身份證": id, "日期":None, "科別診室":None, "診號": None, '地點': None, "候診參考時間": None, "醫院": '高雄榮民總醫院'}
      tds = tr.find_all('td')

      store_details['日期'] = tds[1].text.strip().replace(' ', '')
      pattern = re.compile(r'\s+')
      sentence = re.sub(pattern, '', tds[2].text)
      store_details['科別診室'] = sentence
      store_details['診號'] = tds[3].text.strip().replace(' ', '')
      store_details['候診參考時間'] = tds[4].text.strip().replace(' ', '')
      store_details['地點'] = tds[5].text.strip().replace(' ', '')
      store_list.append(store_details)
  except Exception as e:
    print('http error (' + name + ' ' + id + ' 高雄榮民總醫院 )' + str(e))
  return store_list
# print(checking('test', 'A124365349', '19780210'))