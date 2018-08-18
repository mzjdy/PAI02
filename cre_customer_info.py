# -*- Codeing:UTF-8
# -*- Richard(410982635@qq.com)
# -*- 2018.07.31

import csv
import linecache
import os
import random
import time
from luhn import *
from tqdm import *

PWD = os.getcwd()
file_areano = PWD + '/Parameters/icbc_areano.txt'
file_city = PWD + '/Parameters/cus_cityname.txt'
file_street = PWD + '/Parameters/cus_streetname.txt'
file_lastname = PWD + '/Parameters/cus_lastname.txt'
file_firstname = PWD + '/Parameters/cus_firstname.txt'
file_email = PWD + '/Parameters/cus_emailtype.txt'
file_pid = PWD + '/Parameters/cus_pidtype.txt'
file_phone = PWD + '/Parameters/cus_phonetype.txt'
file_bin = PWD + '/Parameters/cardbin.csv'

# 检查工作目录是否存在，不存在则创建目录
if not os.path.exists(PWD + '/Parameters'):
    os.mkdir(PWD + '/Parameters')

if not os.path.exists(PWD + '/OutFiles'):
    os.mkdir(PWD + '/OutFiles')

# 检查依赖文件是否存在
try:
    f1 = open(file_areano)
    f1.close()
except FileNotFoundError:
    print("发现错误：地区号文件 \"%s\" 不存在！" % file_areano)
    os._exit(0)

try:
    f1 = open(file_city)
    f1.close()
except FileNotFoundError:
    print("发现错误：城市名文件 \"%s\" 不存在！" % file_city)
    os._exit(0)

try:
    f1 = open(file_street)
    f1.close()
except FileNotFoundError:
    print("发现错误：街区名文件 \"%s\" 不存在！" % file_street)
    os._exit(0)

try:
    f1 = open(file_lastname)
    f1.close()
except FileNotFoundError:
    print("发现错误：客户姓氏文件 \"%s\" 不存在！" % file_lastname)
    os._exit(0)

try:
    f1 = open(file_firstname)
    f1.close()
except FileNotFoundError:
    print("发现错误：客户名字文件 \"%s\" 不存在！" % file_firstname)
    os._exit(0)

try:
    f1 = open(file_email)
    f1.close()
except FileNotFoundError:
    print("发现错误：邮箱类型文件 \"%s\" 不存在！" % file_email)
    os._exit(0)

try:
    f1 = open(file_pid)
    f1.close()
except FileNotFoundError:
    print("发现错误：身份证区域代码文件 \"%s\" 不存在！" % file_pid)
    os._exit(0)

try:
    f1 = open(file_phone)
    f1.close()
except FileNotFoundError:
    print("发现错误：移动电话号段文件 \"%s\" 不存在！" % file_phone)
    os._exit(0)

try:
    f1 = open(file_bin)
    f1.close()
except FileNotFoundError:
    print("发现错误：银行卡BIN码文件 \"%s\" 不存在！" % file_bin)
    os._exit(0)


def get_cus_info():
    # 生成客户编号
    areano_lines = len(open(file_areano).readlines())
    areano = linecache.getline(file_areano, random.randint(1, areano_lines)).split(',')[0]
    cus_id = areano + "".join(random.choice("0123456789") for i in range(8))

    # 生成客户姓名
    lastname_lines = len(open(file_lastname).readlines())
    firstname_lines = len(open(file_firstname).readlines())
    lastname = linecache.getline(file_lastname, random.randint(1, lastname_lines)).strip('\n')
    firstname = linecache.getline(file_firstname, random.randint(1, firstname_lines)).strip('\n')
    cus_name = lastname + firstname

    # 生成证件类型、号码、出生日期、客户性别
    pid_lines = len(open(file_pid).readlines())
    while True:
        pidcode = linecache.getline(file_pid, random.randint(1, pid_lines))[:6]
        if pidcode[-2:] != '00':
            break
    brithstarttime = time.mktime((1960, 1, 1, 0, 0, 0, 0, 0, 0))
    brithendtime = time.mktime((2000, 12, 31, 23, 59, 59, 0, 0, 0))
    randombrith = time.localtime(random.randint(brithstarttime, brithendtime))
    cus_brith = time.strftime("%Y-%m-%d", randombrith)
    pidbrith = ''.join(cus_brith.split('-'))
    pidserial = random.randint(100, 999)
    if pidserial % 2 == 0:
        cus_gender = "1"
    else:
        cus_gender = "0"
    prepid = pidcode + pidbrith + str(pidserial)
    pidcount = 0
    pidweight = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
    pidcheck = {'0': '1', '1': '0', '2': 'X', '3': '9', '4': '8', '5': '7', '6': '6', '7': '5', '8': '5', '9': '3',
                '10': '2'}
    for pidi in range(0, len(prepid)):
        pidcount = pidcount + int(prepid[pidi]) * pidweight[pidi]
    cus_pid = "0," + prepid + pidcheck[str(pidcount % 11)]

    # 生成婚姻状况
    mar_status = random.choice(["0", "1", "2"])

    # 生成教育程度
    edu_level = random.choice(["0", "1", "2", "3", "4"])

    # 生成客户职业
    occ_type = random.choice(["0", "1", "2", "3", "4", "5", "6", "7"])

    # 生成联系电话
    phone_lines = len(open(file_phone).readlines())
    phoneid = linecache.getline(file_phone, random.randint(1, phone_lines)).strip('\n')[:3]
    cus_phone = phoneid + "".join(random.choice("0123456789") for i in range(8))

    # 生成电子邮件
    email_lines = len(open(file_email).readlines())
    emailname = "".join(random.choice("0123456789qbcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPWRSTUVWXYZ_-") for i in
                        range(random.randint(6, 10)))
    emailtype = linecache.getline(file_email, random.randint(1, email_lines)).strip('\n')
    cus_email = emailname + emailtype

    # 生成居住类型、居住地址
    live_type = random.choice(["0", "1", "2", "3", "4"])
    city_lines = len(open(file_city).readlines())
    street_lines = len(open(file_street).readlines())
    city = linecache.getline(file_city, random.randint(1, city_lines)).strip('\n')
    street = linecache.getline(file_street, random.randint(1, street_lines)).strip('\n')
    cus_address = city + street + "".join(random.choice("123456789") for i in range(random.randint(1, 4))) + "号"

    # 生成银行卡号、开户银行、卡种代码、卡种名称
    with open(file_bin, 'r', encoding='utf-8') as binfile:
        binlist = []
        targe = csv.reader(binfile)
        for i in targe:
            bincode = i[5]
            binlist.append(bincode)

        def get_cardpara():
            targebin = random.choice(binlist[1:])
            with open(file_bin, 'r', encoding='utf-8') as binparafile:
                record = csv.DictReader(binparafile)
                for i in record:
                    if i["卡BIN取值"] == targebin:
                        return i

        cardpara = get_cardpara()
        cus_bank = cardpara["发卡行名"]
        cardlen = cardpara["卡号长度"]
        binlen = cardpara["卡BIN长度"]
        cardbin = cardpara["卡BIN取值"]
        cus_cardcode = cardpara["卡种代码"]
        cus_cardname = cardpara["卡种"]
        cardran = int(cardlen) - int(binlen) - 1
        precardno = cardbin + "".join(random.choice("0123456789") for i in range(cardran))
        cus_cardno = append(precardno)

        # 生成创建机构、创建柜员
        cre_branch = areano + "".join(random.choice("0123456789") for i in range(4))
        cre_teller = "".join(random.choice("0123456789") for i in range(4))

        # 生成创建日期、创建时间
        starttime = time.mktime((2010, 1, 1, 0, 0, 0, 0, 0, 0))
        endtime = time.mktime((2017, 12, 31, 23, 59, 59, 0, 0, 0))
        randomtime = time.localtime(random.randint(starttime, endtime))
        cre_datetime = time.strftime("%Y-%m-%d %H:%M:%S", randomtime)

        # 格式化输出内容
        cus_result = cus_id + ',' + cus_name + ',' + cus_pid + ',' + cus_brith + ',' + cus_gender + ',' + mar_status \
                     + ',' + edu_level + ',' + occ_type + ',' + cus_phone + ',' + cus_email + ',' + live_type + ',' + \
                     cus_address + ',' + cus_bank + ',' + cus_cardcode + ',' + cus_cardname + ',' + cus_cardno + ',' + \
                     cre_branch + ',' + cre_teller + ',' + cre_datetime

        return cus_result


# 输出文件
outfile = PWD + '/OutFiles/customer_info.txt'
title = "客户编号,客户姓名,证件类型,证件号码,出生日期,客户性别,婚姻状况,教育程度,客户职业,联系电话,电子邮件,居住状态,居住地址," \
        "银行卡号,开户银行,卡种代码,卡种名称,创建机构,创建柜员,创建日期,创建时间"
open(outfile, 'w').write(title + '\n')
# info_num = input('\r' + "请输入拟生成的客户信息条数：")
while True:
    info_num = input('\r' + "请输入拟生成的客户信息数量：")
    if str.isdigit(info_num) == True:
        break
    else:
        print('数字格式不合法，请重新输入……')
for i in tqdm(range(0, int(info_num))):
    open(outfile, 'a').write(get_cus_info() + '\n')
outfile_lines = len(open(outfile).readlines())
print("个人客户信息已生成！共 %s 条记录，输出文件 %s" % (outfile_lines - 1, outfile))
