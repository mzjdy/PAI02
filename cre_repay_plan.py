# -*- Codeing:UTF-8
# -*- Richard(410982635@qq.com)
# -*- 2018.08.02

import datetime
import linecache
import os
from decimal import *

from dateutil.relativedelta import relativedelta
from tqdm import *

PWD = os.getcwd()
file_loan_iou = PWD + '/OutFiles/Loan_iou.txt'

# 检查工作目录是否存在，不存在则创建目录
if not os.path.exists(PWD + '/Parameters'):
    os.mkdir(PWD + '/Parameters')

if not os.path.exists(PWD + '/OutFiles'):
    os.mkdir(PWD + '/OutFiles')

# 检查依赖文件是否存在
try:
    f1 = open(file_loan_iou)
    f1.close()
except FileNotFoundError:
    print("发现错误：借据文件 \"%s\" 不存在！" % file_loan_iou)
    os._exit(0)

loaniou_lines = len(open(file_loan_iou).readlines())
print('\r' + "找到 %s 条借据数据，正在生成还款计划信息……" % (loaniou_lines - 1))

outfile = PWD + '/OutFiles/repay_plan.txt'
title = "协议编号,借据编号,还款期数,应还日期,应还利息,应还本金,应还本息,还款标志"
open(outfile, "w").write(title + '\n')


def cal_date(date, para):
    s = datetime.datetime.strptime(date, "%Y{y}%m{m}%d{d}".format(y='-', m='-', d=''))
    t = str(s + relativedelta(months=+int(para)))[: 10]
    return t


for i in tqdm(range(2, loaniou_lines + 1)):
    iou = linecache.getline(file_loan_iou, i).split(',')
    loan_id = iou[0]
    iou_id = iou[1]
    amount = Decimal(iou[2])
    rate_y = Decimal(iou[5]) / 100
    rate_m = Decimal(iou[5]) / 12 / 100
    term = Decimal(iou[6])
    method = iou[8]
    effdate = iou[15]
    return_flag = "0"  # 初始化还款标志为"未到还款日"

    if method == "0":  # 计算等额本息，每月还款额=(贷款本金*月利率*(1+月利率)^还款月数)/((1+月利率)^还款月数－1)
        repay_serial = "1"
        repay_date = cal_date(effdate, repay_serial)
        repay_m = amount * rate_m * pow((1 + rate_m), term) / (pow((1 + rate_m), term) - 1)
        repay_mD = Decimal(repay_m).quantize(Decimal('0.00'))
        int_m = amount * rate_m
        int_mD = Decimal(int_m).quantize((Decimal('0.00')))
        total_prin = repay_mD - int_mD
        plan = loan_id + ',' + iou_id + ',' + repay_serial + ',' + repay_date + ',' + str(int_mD) + ',' \
               + str(repay_mD - int_mD) + ',' + str(repay_mD) + ',' + return_flag
        open(outfile, "a").write(plan + '\n')
        for t in range(2, int(term) + 1):
            repay_serial = str(t)
            int_n = (amount * rate_m - repay_m) * pow((1 + rate_m), (t - 1)) + repay_m
            int_nD = Decimal(int_n).quantize(Decimal('0.00'))
            repay_date = cal_date(effdate, repay_serial)
            total_prin = total_prin + repay_mD - int_nD
            prin_l = total_prin - amount
            if t == int(term):
                plan = loan_id + ',' + iou_id + ',' + repay_serial + ',' + repay_date + ',' + str(int_nD + prin_l) + ',' \
                       + str(repay_mD - int_nD - prin_l) + ',' + str(repay_mD) + ',' + return_flag
            else:
                plan = loan_id + ',' + iou_id + ',' + repay_serial + ',' + repay_date + ',' + str(int_nD) + ',' \
                       + str(repay_mD - int_nD) + ',' + str(repay_mD) + ',' + return_flag
            open(outfile, "a").write(plan + '\n')
    elif method == "1":  # 计算等额本金
        amount_m = amount / term
        amount_mD = Decimal(amount_m).quantize(Decimal('0.00'))
        amount_l = amount_mD * term - amount
        amount_lD = Decimal(amount_l).quantize(Decimal('0.00'))
        for m in range(1, int(term) + 1):
            repay_serial = str(m)
            int_m = (amount - amount_m * (m - 1)) * rate_m
            int_mD = Decimal(int_m).quantize((Decimal('0.00')))
            repay_m = amount_m + int_m
            repay_mD = Decimal(repay_m).quantize(Decimal('0.00'))
            repay_date = cal_date(effdate, repay_serial)
            if repay_serial == '1':
                plan = loan_id + ',' + iou_id + ',' + repay_serial + ',' + repay_date + ',' + str(int_mD) + ',' \
                       + str(amount_mD - amount_lD) + ',' + str(repay_mD - amount_lD) + ',' + return_flag
            else:
                plan = loan_id + ',' + iou_id + ',' + repay_serial + ',' + repay_date + ',' + str(int_mD) + ',' \
                       + str(amount_mD) + ',' + str(repay_mD) + ',' + return_flag
            open(outfile, "a").write(plan + '\n')
    else:  # 计算先息后本
        int_m = amount * rate_m
        int_mD = Decimal(int_m).quantize((Decimal('0.00')))
        for p in range(1, int(term)):
            repay_serial = str(p)
            repay_date = cal_date(effdate, p)
            plan = loan_id + ',' + iou_id + ',' + repay_serial + ',' + repay_date + ',' + str(int_mD) + ',' \
                   + '0.00' + ',' + str(int_mD) + ',' + return_flag
            open(outfile, "a").write(plan + '\n')
        repay_serial = iou[6]
        repay_date = cal_date(effdate, repay_serial)
        plan = loan_id + ',' + iou_id + ',' + repay_serial + ',' + repay_date + ',' + str(int_mD) + ',' \
               + str(amount) + ',' + str(int_mD + amount) + ',' + return_flag

        open(outfile, "a").write(plan + '\n')

outfile_lines = len(open(outfile).readlines())
print("还款计划已生成！共 %s 条记录，输出文件 %s" % (outfile_lines - 1, outfile))
