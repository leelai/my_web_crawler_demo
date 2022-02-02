import logging
import utils
import xlsxReader
from xlsxReader import getUsers
from ndmctsgh import checking as checkingNdmctsgh
from mmh import checking as checkingMmh
from vghks import checking as checkVghks
from service import checking as checkService
from service1 import checking as checkService1
from service2 import checking as checkService2
from service3 import checking as checkService3
from checkTime import canIUse

utils.initLog()
# result4 = checkService3('name', 'V121311981', '770418')

if canIUse():
    users = getUsers()
    for user in users:
        id = user[xlsxReader.id_str]
        birth = user[xlsxReader.birth_str]
        birth2 = user[xlsxReader.birth2_str]
        year = user[xlsxReader.year_]
        month = user[xlsxReader.month]
        day = user[xlsxReader.day]
        name = user[xlsxReader.name_str]

        #三軍總醫院
        utils.delay()
        result = checkingNdmctsgh(name, id)
        if len(result) == 0:
            print(name + " " + id + " 查無資料(三軍總醫院)")
        if len(result) > 0:
            logging.info(result)

        #馬偕紀念醫院
        utils.delay()
        result2 = checkingMmh(name, id, birth)
        if len(result2) == 0:
            print(name + " " + id + " 查無資料(馬偕紀念醫院)")
        if len(result2) > 0:
            logging.info(result2)

        #高雄榮民總醫院
        utils.delay()
        result3 = checkVghks(name, id, birth2)
        if len(result3) == 0:
            print(name + " " + id + " 查無資料(高雄榮民總醫院)")
        if len(result3) > 0:
            logging.info(result3)

        #新北市立聯合
        utils.delay()
        result4 = checkService(name, id, birth)
        if len(result4) == 0:
            print(name + " " + id + " 查無資料(新北市立聯合)")
        if len(result4) > 0:
            logging.info(result4)

        #中山醫院
        utils.delay()
        result4 = checkService1(name, id, birth)
        if len(result4) == 0:
            print(name + " " + id + " 查無資料(中山醫院)")
        if len(result4) > 0:
            logging.info(result4)

        #台安醫院
        utils.delay()
        result4 = checkService2(name, id, year, month, day)
        if len(result4) == 0:
            print(name + " " + id + " 查無資料(台安醫院)")
        if len(result4) > 0:
            logging.info(result4)

        #遠東聯合診所
        utils.delay()
        result4 = checkService3(name, id, birth)
        if len(result4) == 0:
            print(name + " " + id + " 查無資料(遠東聯合診所)")
        if len(result4) > 0:
            logging.info(result4)
else:
    logging.error('expired!')