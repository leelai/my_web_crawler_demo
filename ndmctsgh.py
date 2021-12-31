import requests
import json

url = 'https://www2.ndmctsgh.edu.tw/newwebreg/Register/RegCancel'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'
  }

def checking(name, id):
  myobj = {'ActionChoice': '2', 'cnoid': id, 'hcnoid': '', 'cno':'', 'passport':'', 'Action1':'', 'rid':''}
  x = requests.post(url, data = myobj, headers = headers)
  start = x.text.index('JSON.parse(') + 12
  end = x.text.index(');', start) - 1
  store_list = []
  books = json.loads(x.text[start:end])
  for item in books:
    store_details = {"姓名":name, "身份證": None, "日期":None, "科別":None, "診室":None, "診號": None, "院區": None, '醫院': '三軍總醫院'}
    store_details['身份證'] = item['Id'].strip()
    store_details['日期'] = item['Date'].strip()
    store_details['科別'] = item['Segtime'].strip()
    store_details['診室'] = item['Room'].strip()
    store_details['診號'] = item['Number'].strip()
    store_details['院區'] = item['Position'].strip()
    store_list.append(store_details)
  return store_list