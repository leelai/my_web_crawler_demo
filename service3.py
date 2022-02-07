import logging
import requests
from bs4 import BeautifulSoup
import re
import utils

baseUrl = 'http://www.fepc.com.tw'
queryUrl = baseUrl + '/web_netreg2/web_netregQuery1.asp'
postUrl = 'http://reg.fepc.com.tw' + '/netreg/web_netregRegQuery_new.asp'

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

def checking(name, id, birth):
  store_list = []
  s = requests.Session()
  try:
    # x = s.get(openUrl, headers = headers, timeout = utils.timeout) #有這個cookie才有 ASP.NET_SessionId
    x = s.get(queryUrl, headers = headers, timeout = utils.timeout)
    x.encoding = 'big5'
    # print("encoding: %s" % x.encoding)
    # print("content: \n%s" % x.text)
    utils.delay()
    # find form1 
    soup = BeautifulSoup(x.text, 'html.parser')
    # print(soup.prettify())
    code = soup.find('input', {"name": "code"}).get('value')
    submit = soup.find('input', {"name": "Submit"}).get('value')
    # print(code)
    # print(submit)
    # print(__VIEWSTATEGENERATOR)
    myobj = {'code':code,'submit': submit, 'idchart': 'id', 'idchartno': id, 'birth': birth}
    # url = baseUrl + form
    res = s.post(postUrl, data = myobj, timeout = utils.timeout)
    res.encoding = 'big5'
    soup2 = BeautifulSoup(res.text, 'html.parser')
    # print(soup2.prettify())
    table = soup2.find('table', {'class': 'text'})
    # print(table.prettify())

    if table == None:
      return store_list

    trs = table.find_all('tr', {'bgcolor': '#FFFFFF'})
    for tr in trs:
      # print(tr.prettify())
      if tr.text.find('退掛') >= 0:
        continue
      store_details = {"姓名":name, "身份證": id, "日期":None, "科別診室":None, "診號": None, '地點': None, "候診參考時間": None, "醫院": '遠東聯合診所'}
      tds = tr.find_all('td')
      # print(tds[1].text)

      store_details['日期'] = tds[1].text.strip().replace(' ', '') + '(' + tds[2].text.strip().replace(' ', '') + ')'


      # pattern = re.compile(r'\s+')
      # sentence = re.sub(pattern, '', tds[2].text)

      store_details['科別診室'] = tds[4].text.strip().replace(' ', '')
      store_details['診號'] = tds[5].text.strip().replace(' ', '')
      store_details['候診參考時間'] = tds[2].text.strip().replace(' ', '')
      store_details['地點'] = '遠東聯合診所'
      store_list.append(store_details)
  except Exception as e:
    print('http error (' + name + ' ' + id + ' 遠東聯合診所 )' + str(e))
  # print(store_list)
  return store_list
# print(checking('test', 'A124365349', '19780210'))