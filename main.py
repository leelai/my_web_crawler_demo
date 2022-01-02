import logging
import utils
import xlsxReader
from xlsxReader import getUsers
from ndmctsgh import checking as checkingNdmctsgh
from mmh import checking as checkingMmh
from vghks import checking as checkVghks
from checkTime import canIUse

utils.initLog()
if canIUse():
    users = getUsers()
    for user in users:
        id = user[xlsxReader.id_str]
        birth = user[xlsxReader.birth_str]
        birth2 = user[xlsxReader.birth2_str]
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
else:
    logging.error('expired!')