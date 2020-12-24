import os
from typing import Dict, List, Any

import openpyxl
from pypinyin import lazy_pinyin
import mysql.connector


def parseWork(path, img_path, post):
    wb = openpyxl.load_workbook(path)
    all_sheets = wb.sheetnames
    for i in range(len(all_sheets)):
        sheet = wb[all_sheets[i]]
        data = parseSheet(sheet, img_path, post)
        updateDb(data)


def parseSheet(sheet, img_path, post):
    data: List[Dict[str, Any]] = []
    columnIndex = getColumnIndex(sheet)
    if columnIndex == -1:
        print("未找到name列")
        return data
    while sheet["B" + str(columnIndex)].value is not None:
        name = sheet["C" + str(columnIndex)].value.strip().replace(' ', '')
        record = {"name": name}
        columnIndex = columnIndex + 1
        record["dept"] = sheet["C" + str(columnIndex)].value
        columnIndex = columnIndex + 1
        tags = sheet["C" + str(columnIndex)].value
        if tags is not None:
            tags = tags.replace("；", ",")
            tags = tags.replace("，", ",")
            tags = tags.replace(";", ",")
            tags = tags.replace("。", "")
        record["tags"] = tags
        columnIndex = columnIndex + 1
        record["desc"] = sheet["C" + str(columnIndex)].value
        columnIndex = columnIndex + 1
        record["performance"] = sheet["C" + str(columnIndex)].value
        columnIndex = columnIndex + 1
        img = parseImg(img_path, name)
        record["img"] = img
        pinyin = ''.join(lazy_pinyin(name))
        record["pinyin"] = pinyin
        record["post"] = post
        data.append(record)
    return data


def getColumnIndex(sheet):
    columnIndex = 1
    while sheet["B" + str(columnIndex)].value is not None:
        name = sheet["B" + str(columnIndex)].value.strip()
        if "姓名" in name:
            return columnIndex
        columnIndex = columnIndex + 1
    return -1


def parseImg(path, name):
    files = os.listdir(path)
    for file in files:
        if name in file:
            return file
    print(f"未找到匹配照片：{name}")
    return ""


def updateDb(data):
    config = {
        'user': 'test',
        'password': 'test',
        'host': 'localhost',
        'database': 'spring',
        'raise_on_warnings': True,
        'charset': 'utf8mb4',
        "connection_timeout": 5,
        "use_pure": True,
        'pool_size': 10,
        "pool_name": "offlineserver",
        "pool_reset_session": False
    }
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor(buffered=True)
    for i in range(len(data)):
        record = data[i]
        sql = "select * from cx_staff where name = %s and dep_name = %s"
        insert_sql = "insert into cx_staff (name,name_spell,head_img_id,post,dep_name,tags,description,performace_desc,number_of_votes,status)" \
                     "values(%(name)s,%(pinyin)s,%(img)s,%(post)s,%(dept)s,%(tags)s,%(desc)s,%(performance)s,0,0)"
        update_sql = "update cx_staff set name=%s,name_spell=%s,head_img_id=%s,post=%s,dep_name=%s,tags=%s,description=%s,performace_desc=%s where id=%s"
        cursor.execute(sql, (record["name"], record["dept"]))
        if cursor.rowcount > 0:
            row = cursor.fetchall()
            id = row[-1][0]
            cursor.execute(update_sql, (
                record["name"], record["pinyin"], record["img"], record["post"], record["dept"], record["tags"],
                record["desc"], record["performance"], id))
        else:
            cursor.execute(insert_sql, record)

    cnx.commit()
    cursor.close()
    cnx.close()


if __name__ == "__main__":
    base_dir = "F:/tsm/财富/微信投票/doc/"
    fileList = [item for item in os.listdir(base_dir) if item.endswith("xlsx")]
    for file in fileList:
        parseWork(base_dir + file, "F:/3/compress", file[0:4])
