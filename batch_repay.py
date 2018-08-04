# -*- Codeing:UTF-8
# -*- Richard(410982635@qq.com)
# -*- 2018.08.02

# 还款历史-repay_history
#     协议编号,loan_id,chr(12);
#     借据编号,iou_id,char(3);
#     还款日期,return_date,date;
#     还款期数,return_bill,char(5);
#     还款金额,return_amount,float(12,2);
#     实还利息,return_imt,float(12,2);
#     实还本金,return_prin,flost(12,2);

# 贷款违约-loan_default
#     协议编号,loan_id,chr(12);
#     借据编号,iou_id,char(3);
#     还款期数,repay_serial,char(5);
#     应还日期,repay_date,date;
#     欠还利息,def_int,float(12,2);
#     欠还本金,def_prin,float(12,2);
#     欠款本息,def_amount,float(12,2);

import datetime
import linecache
import os
import random

PWD = os.getcwd()
file_loan_agr = PWD + '/OutFiles/loan_agreement.txt'
file_loan_iou = PWD + '/OutFiles/loan_iou.txt'
file_repay_plan = PWD + '/OutFiles/repay_plan.txt'

# 检查工作目录是否存在，不存在则创建目录
if not os.path.exists(PWD + '/Parameters'):
    os.mkdir(PWD + '/Parameters')

if not os.path.exists(PWD + '/OutFiles'):
    os.mkdir(PWD + '/OutFiles')

# 检查依赖文件是否存在
try:
    f1 = open(file_loan_agr)
    f1.close()
except FileNotFoundError:
    print("发现错误：贷款协议文件 \"%s\" 不存在！" % file_loan_agr)
    os._exit(0)

try:
    f1 = open(file_loan_iou)
    f1.close()
except FileNotFoundError:
    print("发现错误：借据文件 \"%s\" 不存在！" % file_loan_iou)
    os._exit(0)

try:
    f1 = open(file_repay_plan)
    f1.close()
except FileNotFoundError:
    print("发现错误：还款计划文件 \"%s\" 不存在！" % file_repay_plan)
    os._exit(0)

repayplan_lines = len(open(file_repay_plan).readlines())
print("找到 %s 条还款计划数据，正在生成还款历史及违约信息！" % (repayplan_lines - 1))

outfile1 = PWD + '/OutFiles/repay_history.txt'
title1 = "协议编号,借据编号,还款日期,还款期数,还款金额,实还利息,实还本金"
open(outfile1, "w").write(title1 + '\n')

outfile2 = PWD + '/OutFiles/loan_defult.txt'
title2 = "协议编号,借据编号,还款期数,应还日期,欠还利息,欠还本金,欠还本息"
open(outfile2, "w").write(title2 + '\n')

today = datetime.datetime.today()

for i in range(3, repayplan_lines + 1):
    # for i in range(3,30):
    rec_s = linecache.getline(file_repay_plan, i - 1).strip('\n').split(',')
    s_id = rec_s[0] + rec_s[1]
    s_date = datetime.datetime.strptime(rec_s[3], "%Y-%m-%d")
    s_flag = rec_s[7]
    s_int = rec_s[4]
    s_prin = rec_s[5]
    s_amount = rec_s[6]
    rec_t = linecache.getline(file_repay_plan, i).strip('\n').split(',')
    t_id = rec_t[0] + rec_t[1]
    t_date = datetime.datetime.strptime(rec_t[3], "%Y-%m-%d")
    t_flag = rec_t[7]
    t_int = rec_t[4]
    t_prin = rec_t[5]
    t_amount = rec_t[6]
    if s_id == t_id and today > s_date:
        PD = random.random()
        if PD > 0.9:
            rec_s.remove("0")
            rec_s.append("3")
            newrec = ','.join(rec_s)
            open(file_repay_plan)
        else:
            rec_s.remove("0")
            rec_s.append("1")
            newrec = ','.join(rec_s)

        print(str(PD), rec_s)
        print(str(PD), rec_t)

# print(today, s_date, t_date)
# print(today >= s_date)
# print(s_date < t_date)
