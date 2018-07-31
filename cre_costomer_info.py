# -*- Codeing:UTF-8
# -*- Richard(410982635@qq.com)
# -*- 2018.07.31

# 个人客户信息-customer_info
#     客户编号,cus_id,char(12);
#     客户姓名,cus_name,char(20);
#     证件类型,id_type,char(1); 0-居民身份证
#     证件号码,id_num,char(20);
#     出生日期,cus_brith,date;
#     客户性别,cus_gender,char(1); 0-男/1-女
#     婚姻状况,mar_status,char(1); 0-已婚/1-未婚/2-其他
#     教育程度,edu_level,char(1); 0-初中及以下/1-高中/2-大学/3-硕士研究生/4-博士研究生
#     客户职业,occ_type,char(2); 0-公务员/1-事业员工/2-金融员工/3-公司职员/4-军人/5-学生/6-自由职业/7-其他
#     联系电话,cus_phone,char(20);
#     电子邮件,cus_email,char(30);
#     居住类型,live_type,char(1); 0-自有无贷款/1-自有有贷款/2-租赁/3-宿舍/4-其他
#     居住地址,cus_address,char(100);
#     银行卡号,cus_cardno,char(20); luhn校验
#     开户银行,cus_bank,char(100);
#     卡种代码,card_typecode,char(2); 1-借记卡/2-贷记卡/3-准贷记卡/4-预付费卡
#     卡种名称,card_typename,char(20);
#     创建机构,cre_branch,char(10);
#     创建柜员,cre_teller,char(10);
#     创建日期,cre_date,date;
#     创建时间,cre_time,time;

import os
import io
import linecache
import random
import csv
from datetime import timedelta, date
from luhn import *

PWD = os.getcwd()
file_areano = PWD + '/icbc_areano.txt'
file_city = PWD + '/cus_cityname.txt'
file_street = PWD + '/cus_streetname.txt'
file_xing = PWD + '/cus_lastname.txt'
file_ming = PWD + '/cus_firstname.txt'
file_email = PWD + '/cus_emailtype.txt'
file_pid = PWD + '/cus_pidtype.txt'
file_phone = PWD + '/cus_phonetype.txt'
file_bin = PWD + '/cardbin.csv'

# 检查依赖文件是否存在
try:
    f1 = open(file_areano)
    f1.close()
except FileNotFoundError:
    print("发现错误：地区号文件 \"%s\" 不存在！" % (file_areano))
    os._exit(0)

try:
    f1 = open(file_city)
    f1.close()
except FileNotFoundError:
    print("发现错误：城市名文件 \"%s\" 不存在！" % (file_city))
    os._exit(0)

try:
    f1 = open(file_street)
    f1.close()
except FileNotFoundError:
    print("发现错误：街区名文件 \"%s\" 不存在！" % (file_street))
    os._exit(0)

try:
    f1 = open(file_xing)
    f1.close()
except FileNotFoundError:
    print("发现错误：客户姓氏文件 \"%s\" 不存在！" % (file_xing))
    os._exit(0)

try:
    f1 = open(file_ming)
    f1.close()
except FileNotFoundError:
    print("发现错误：客户名字文件 \"%s\" 不存在！" % (file_ming))
    os._exit(0)

try:
    f1 = open(file_email)
    f1.close()
except FileNotFoundError:
    print("发现错误：邮箱类型文件 \"%s\" 不存在！" % (file_email))
    os._exit(0)

try:
    f1 = open(file_pid)
    f1.close()
except FileNotFoundError:
    print("发现错误：身份证区域代码文件 \"%s\" 不存在！" % (file_pid))
    os._exit(0)

try:
    f1 = open(file_phone)
    f1.close()
except FileNotFoundError:
    print("发现错误：移动电话号段文件 \"%s\" 不存在！" % (file_phone))
    os._exit(0)

try:
    f1 = open(file_bin)
    f1.close()
except FileNotFoundError:
    print("发现错误：银行卡BIN码文件 \"%s\" 不存在！" % (file_bin))
    os._exit(0)

# 生成客户编号
areano_lines = len(open(file_areano).readlines())
areano = linecache.getline(file_areano, random.randint(1, areano_lines)).split(',')[0]
cus_id = areano + "".join(random.choice("0123456789") for i in range(8))

# 生成客户姓名

# 生成证件类型、号码、出生日期、客户性别

# 生成婚姻状况

# 生成教育程度

# 生成客户职业

# 生成联系电话

# 生成电子邮件

# 生成居住类型、居住地址

# 生成银行卡号、开户银行、卡种代码、卡种名称

# 生成创建机构、创建柜员、创建日期、创建时间

# 输出文件
# info_num = input("请输入拟生成的客户信息条数：")


print(cus_id)
