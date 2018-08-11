import linecache
import os

import pymysql
from tqdm import *

# 判断依赖文件蝇否存在
PWD = os.getcwd()
file_cus = PWD + '/OutFiles/customer_info.txt'
file_loan = PWD + '/OutFiles/loan_agreement.txt'
file_iou = PWD + '/OutFiles/loan_iou.txt'
file_plan = PWD + '/OutFiles/repay_plan.txt'
file_repay = PWD + '/OutFiles/repay_history.txt'
file_def = PWD + '/OutFiles/loan_defult.txt'
try:
    f1 = open(file_cus)
    f1.close()
except FileNotFoundError:
    print("发现错误：个人客户信息文件 \"%s\" 不存在！" % file_cus)
    os._exit(0)

try:
    f1 = open(file_loan)
    f1.close()
except FileNotFoundError:
    print("发现错误：贷款协议文件 \"%s\" 不存在！" % file_loan)
    os._exit(0)

try:
    f1 = open(file_iou)
    f1.close()
except FileNotFoundError:
    print("发现错误：借据文件 \"%s\" 不存在！" % file_iou)
    os._exit(0)

try:
    f1 = open(file_plan)
    f1.close()
except FileNotFoundError:
    print("发现错误：还款计划文件 \"%s\" 不存在！" % file_plan)
    os._exit(0)

try:
    f1 = open(file_repay)
    f1.close()
except FileNotFoundError:
    print("发现错误：还款历史文件 \"%s\" 不存在！" % file_repay)
    os._exit(0)

try:
    f1 = open(file_def)
    f1.close()
except FileNotFoundError:
    print("发现错误：违约历史文件 \"%s\" 不存在！" % file_def)
    os._exit(0)

# 连接mySQL数据库
con = pymysql.connect(user='python', passwd='pythonpwd', db='PAI', charset='utf8')
cur = con.cursor()

# 重建数据表
cur.execute('truncate table PAI.customer_info;')
cur.execute('truncate table PAI.loan_agreement;')
cur.execute('truncate table PAI.loan_iou;')
cur.execute('truncate table PAI.repay_plan;')
cur.execute('truncate table PAI.repay_history;')
cur.execute('truncate table PAI.loan_default;')

# 转换个人客户信息
t_data = open(file_cus, 'r').readlines()[1:]
t_lines = len(t_data)
print('\r' + "请稍候，正在转换个人客户信息，原文件共 %s 条记录……" % (t_lines))
for i in tqdm(range(2, t_lines + 2)):
    t_list = linecache.getline(file_cus, i).strip('\n').split(',')
    sqli = 'insert into PAI.customer_info(cus_id,cus_name,cus_idtype,cus_idnum,cus_brith,cus_gender,cus_marry,cus_edu,cus_occ,cus_phone,cus_email,cus_livetype,cus_address,cus_bank,cus_cardcode,cus_cardname,cus_cardno,cre_branch,cre_teller,cre_datetime) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
    value = (
        t_list[0], t_list[1], t_list[2], t_list[3], t_list[4], t_list[5], t_list[6], t_list[7], t_list[8], t_list[9], t_list[10], t_list[11],
        t_list[12],
        t_list[13], t_list[14], t_list[15], t_list[16], t_list[17], t_list[18], t_list[19])
    cur.execute(sqli, value)
    con.commit()
    # doper = '{:.2%}'.format((i - 1) / t_lines)
    # print("\r请稍候，正在转换个人客户信息，处理第 %s/%s 条记录 ,已完成 %s" % ((i - 1), t_lines, doper), end='')
cur.execute('select count(*) from PAI.customer_info;')
print('\r' + "个人客户信息已转换完成！共输出 %s 条记录。" % (cur.fetchone()))

# 转换贷款协议信息
t_data = open(file_loan, 'r').readlines()[1:]
t_lines = len(t_data)
print('\r'"请稍候，正在转换贷款协议信息，原文件共 %s 条记录……" % (t_lines))
for i in tqdm(range(2, t_lines + 2)):
    t_list = linecache.getline(file_loan, i).strip('\n').split(',')
    sqli = 'insert into PAI.loan_agreement(cus_id,loan_id,loan_code,loan_name,loan_usedcode,loan_usedname,loan_amount,loan_currency,loan_remamount,loan_rate,loan_term,loan_termunit,loan_guaran,loan_effdate,loan_duedate,loan_repaycardno,loan_branch,loan_status) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
    value = (
        t_list[0], t_list[1], t_list[2], t_list[3], t_list[4], t_list[5], t_list[6], t_list[7], t_list[8], t_list[9], t_list[10], t_list[11],
        t_list[12],
        t_list[13], t_list[14], t_list[15], t_list[16], t_list[17])
    cur.execute(sqli, value)
    con.commit()
    # doper = '{:.2%}'.format((i - 1) / t_lines)
    # print("\r请稍候，正在转换贷款协议信息，处理第 %s/%s 条记录 ,已完成 %s" % ((i - 1), t_lines, doper), end='')
cur.execute('select count(*) from PAI.loan_agreement;')
print("\r" + "贷款协议信息已转换完成！共输出 %s 条记录。" % (cur.fetchone()))

# 转换贷款借据信息
t_data = open(file_iou, 'r').readlines()[1:]
t_lines = len(t_data)
print('\r' + "请稍候，正在转换贷款借据信息，原文件共 %s 条记录……" % (t_lines))
for i in tqdm(range(2, t_lines + 2)):
    t_list = linecache.getline(file_iou, i).strip('\n').split(',')
    sqli = 'insert into PAI.loan_iou(loan_id,iou_id,iou_amount,iou_cerrency,iou_remamount,iou_rate,iou_term,iou_termunit,iou_method,iou_repayorder,iou_defrate,iou_prepayflag,iou_prepayfee,iou_changeflag,iou_changefee,iou_effdate,iou_duedate,iou_status) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
    value = (
        t_list[0], t_list[1], t_list[2], t_list[3], t_list[4], t_list[5], t_list[6], t_list[7], t_list[8], t_list[9], t_list[10], t_list[11],
        t_list[12],
        t_list[13], t_list[14], t_list[15], t_list[16], t_list[17])
    cur.execute(sqli, value)
    con.commit()
    # doper = '{:.2%}'.format((i - 1) / t_lines)
    # print("\r请稍候，正在转换贷款借据信息，处理第 %s/%s 条记录 ,已完成 %s" % ((i - 1), t_lines, doper), end='')
cur.execute('select count(*) from PAI.loan_iou;')
print("\r" + "贷款借据信息已转换完成！共输出 %s 条记录。" % (cur.fetchone()))

# 转换还款计划信息
t_data = open(file_plan, 'r').readlines()[1:]
t_lines = len(t_data)
print('\r' + "请稍候，正在转换还款计划信息，原文件共 %s 条记录……" % (t_lines))
for i in tqdm(range(2, t_lines + 2)):
    t_list = linecache.getline(file_plan, i).strip('\n').split(',')
    sqli = 'insert into PAI.repay_plan(loan_id,iou_id,repay_serial,repay_date,repay_int,repay_prin,repay_amount,return_flag) values (%s,%s,%s,%s,%s,%s,%s,%s)'
    value = (t_list[0], t_list[1], t_list[2], t_list[3], t_list[4], t_list[5], t_list[6], t_list[7])
    cur.execute(sqli, value)
    con.commit()
    # doper = '{:.2%}'.format((i - 1) / t_lines)
    # print("\r请稍候，正在转换还款计划信息，处理第 %s/%s 条记录 ,已完成 %s" % ((i - 1), t_lines, doper), end='')
cur.execute('select count(*) from PAI.repay_plan;')
print("\r" + "还款计划信息已转换完成！共输出 %s 条记录。" % (cur.fetchone()))

# 转换还款历史信息
t_data = open(file_repay, 'r').readlines()[1:]
t_lines = len(t_data)
print('\r' + "请稍候，正在转换还款历史信息，原文件共 %s 条记录……" % (t_lines))
for i in tqdm(range(2, t_lines + 2)):
    t_list = linecache.getline(file_repay, i).strip('\n').split(',')
    sqli = 'insert into PAI.repay_history(loan_id,iou_id,return_bill,return_date,return_int,return_prin,return_amount,retrurn_flag) values (%s,%s,%s,%s,%s,%s,%s,%s)'
    value = (t_list[0], t_list[1], t_list[2], t_list[3], t_list[4], t_list[5], t_list[6], t_list[7])
    cur.execute(sqli, value)
    con.commit()
    # doper = '{:.2%}'.format((i - 1) / t_lines)
    # print("\r请稍候，正在转换还款历史信息，处理第 %s/%s 条记录 ,已完成 %s" % ((i - 1), t_lines, doper), end='')
cur.execute('select count(*) from PAI.repay_history;')
print("\r" + "还款历史信息已转换完成！共输出 %s 条记录。" % (cur.fetchone()))

# 转换违约历史信息
t_data = open(file_def, 'r').readlines()[1:]
t_lines = len(t_data)
print('\r' + "请稍候，正在转换违约历史信息，原文件共 %s 条记录……" % (t_lines))
for i in tqdm(range(2, t_lines + 2)):
    t_list = linecache.getline(file_def, i).strip('\n').split(',')
    sqli = 'insert into PAI.loan_default(loan_id,iou_id,repay_serial,repay_date,def_int,def_prin,def_amount,return_flag) values (%s,%s,%s,%s,%s,%s,%s,%s)'
    value = (t_list[0], t_list[1], t_list[2], t_list[3], t_list[4], t_list[5], t_list[6], t_list[7])
    cur.execute(sqli, value)
    con.commit()
    # doper = '{:.2%}'.format((i - 1) / t_lines)
    # print("\r请稍候，正在转换还款计划信息，处理第 %s/%s 条记录 ,已完成 %s" % ((i - 1), t_lines, doper), end='')
cur.execute('select count(*) from PAI.loan_default;')
print("\r" + "还款计划信息已转换完成！共输出 %s 条记录。" % (cur.fetchall()))

# print("\n" + "文件转换完成！执行结束！")
