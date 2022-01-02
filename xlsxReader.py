import openpyxl
import easygui

pos_name = 'A'
pos_birth = 'C'
pos_id = 'E'

id_str = "身份證"
name_str = "姓名"
birth_str= "生日"
birth2_str= "生日2"

def getUsers():
    myFile = easygui.fileopenbox()
    wb_obj = openpyxl.load_workbook(myFile)
    sheet = wb_obj.active

    store_list = []
    total = int(sheet.max_row/3) - 1
    x = range(total)
    for n in x:
        store_details = {id_str: None, name_str:None, birth_str:None, birth2_str:None}
        pos = pos_name + str(5 + n * 3)
        name = sheet[pos].value
        start = name.index('\n')
        name = name[start+1:20].strip()
        # print(name)

        pos = pos_birth + str(5 + n * 3)
        birth = sheet[pos].value.replace('/','')
        if birth.index('0') == 0 :
            birth = birth[1:20].strip()
        birth2 = sheet[pos].value.split("/")
        year = int(birth2[0]) + 1911
        birth2 = str(year) + birth2[1] + birth2[2]
        # print(birth)

        pos = pos_id + str(5 + n * 3)
        id = sheet[pos].value
        # print(id)

        store_details[id_str] = id
        store_details[name_str] = name
        store_details[birth_str] = birth
        store_details[birth2_str] = birth2
        store_list.append(store_details)
    return store_list