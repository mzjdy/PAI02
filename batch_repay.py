# -*- Codeing:UTF-8
# -*- Richard(410982635@qq.com)
# -*- 2018.08.02

import datetime
import os
import random
import time
from tqdm import *

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


def isDate(daypara):
    try:
        time.strptime(daypara, "%Y-%m-%d")
        return True
    except:
        return False


while True:
    daypara = input('\r' + '请输入模拟批量的日期(YYYY-MM-DD): ')
    if isDate(daypara) == True:
        break
    else:
        print('日期格式不合法，请重新输入……')
today = datetime.datetime.strptime(daypara, "%Y-%m-%d")
PDpara = 0.9

repaylist = open(file_repay_plan).readlines()[1:]
repayplan_lines = len(repaylist)
print('\r' + "找到 %s 条还款计划数据，正在生成还款历史及违约历史信息……" % (repayplan_lines))

outfile1 = PWD + '/OutFiles/repay_history.txt'
title1 = "协议编号,借据编号,还款期数,还款日期,实还利息,实还本金,还款金额,还款标志"
open(outfile1, "w").write(title1 + '\n')

outfile2 = PWD + '/OutFiles/loan_defult.txt'
title2 = "协议编号,借据编号,还款期数,应还日期,欠还利息,欠还本金,欠还本息,还款标志"
open(outfile2, "w").write(title2 + '\n')

tempfile = PWD + '/OutFiles/batch_temp.txt'

for i in tqdm(range(0, repayplan_lines - 1)):
    rec_s = repaylist[i].strip('\n').split(',')
    s_id = rec_s[0] + rec_s[1]
    s_date = datetime.datetime.strptime(rec_s[3], "%Y-%m-%d")
    s_flag = rec_s[7]
    rec_t = repaylist[i + 1].strip('\n').split(',')
    t_id = rec_t[0] + rec_t[1]
    t_date = datetime.datetime.strptime(rec_t[3], "%Y-%m-%d")
    t_flag = rec_t[7]
    PD = random.random()
    # 分别处理初笔、末笔、中间数据，并写入中间文件
    if i == 0 and today > s_date:
        if PD > PDpara:
            rec_s[-1] = '3'
            if today > t_date:
                rec_t[-1] = '3'
        else:
            rec_s[-1] = '1'
            if today > t_date:
                rec_t[-1] = '1'
        open(tempfile, 'w').write(','.join(rec_s) + '\n')
        open(tempfile, 'a').write(','.join(rec_t) + '\n')
    elif i == repayplan_lines - 1 and today > s_date:
        if PD > PDpara:
            rec_t[-1] = '3'
        elif today > s_date:
            rec_t[-1] = '1'
        open(tempfile, 'w').write(','.join(rec_t) + '\n')
    elif today > t_date:
        if PD > PDpara:
            rec_t[-1] = '3'
        else:
            rec_t[-1] = '1'
        open(tempfile, 'a').write(','.join(rec_t) + '\n')

# 处理中间文件：同一笔记录违约之后必违约
templist = open(tempfile).readlines()
print("\r" + "中间文件已生成！共 %s 条记录，正在处理……" % (len(templist)))
for t in range(0, len(templist) - 1):
    rec_s = templist[t].strip('\n').split(',')
    s_id = rec_s[0] + rec_s[1]
    rec_t = templist[t + 1].strip('\n').split(',')
    t_id = rec_t[0] + rec_t[1]
    if s_id == t_id:
        if rec_s[-1] == '3':
            rec_t[-1] = '3'
            newrec = ','.join(rec_t) + '\n'
            templist[t + 1] = newrec

open(tempfile, 'w').writelines(templist)
templist = open(tempfile).readlines()

for t in tqdm(range(0, len(templist))):
    rec_s = templist[t].strip('\n').split(',')
    if rec_s[-1] == '3':
        open(outfile2, 'a').write(','.join(rec_s) + '\n')
    else:
        open(outfile1, 'a').write(','.join(rec_s) + '\n')

outfile1_lines = len(open(outfile1).readlines())
outfile2_lines = len(open(outfile2).readlines())
print("还款历史文件已生成！共 %s 条记录，输出文件 %s" % (outfile1_lines - 1, outfile1))
print("违约历史文件已生成！共 %s 条记录，输出文件 %s" % (outfile2_lines - 1, outfile2))
