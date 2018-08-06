# -*- Codeing:UTF-8
# -*- Richard(410982635@qq.com)
# -*- 2018.08.02

import datetime
import linecache
import os

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
    amount = float(iou[2])
    rate_y = round(float(iou[5]) / 100, 4)
    rate_m = round(rate_y / 12, 4)
    term = float(iou[6])
    method = iou[8]
    effdate = iou[15]
    return_flag = "0"  # 初始化还款标志为"未到还款日"

    if method == "0":  # 计算等额本息，每月还款额=(贷款本金*月利率*(1+月利率)^还款月数)/((1+月利率)^还款月数－1)
        repay_serial = "1"
        repay_date = cal_date(effdate, repay_serial)
        repay_m = amount * rate_m * pow((1 + rate_m), term) / (pow((1 + rate_m), term) - 1)
        int_m = amount * rate_m
        plan = loan_id + ',' + iou_id + ',' + repay_serial + ',' + repay_date + ',' + '{:.2f}'.format(int_m) \
               + ',' + '{:.2f}'.format(repay_m - int_m) + ',' + '{:.2f}'.format(repay_m) + ',' + return_flag
        open(outfile, "a").write(plan + '\n')
        for t in range(2, int(term) - 1):
            repay_serial = str(t)
            int_n = (amount * rate_m - repay_m) * pow((1 + rate_m), (t - 1)) + repay_m
            repay_date = cal_date(effdate, repay_serial)
            plan = loan_id + ',' + iou_id + ',' + repay_serial + ',' + repay_date + ',' + '{:.2f}'.format(int_n) \
                   + ',' + '{:.2f}'.format(repay_m - int_n) + ',' + '{:.2f}'.format(repay_m) + ',' + return_flag
            open(outfile, "a").write(plan + '\n')
    elif method == "1":  # 计算等额本金
        amount_m = amount / term
        for m in range(1, int(term) + 1):
            repay_serial = str(m)
            int_m = (amount - amount_m * (m - 1)) * rate_m
            repay_m = amount_m + int_m
            repay_date = cal_date(effdate, repay_serial)
            plan = loan_id + ',' + iou_id + ',' + repay_serial + ',' + repay_date + ',' + '{:.2f}'.format(int_m) \
                   + ',' + '{:.2f}'.format(amount_m) + ',' + '{:.2f}'.format(repay_m) + ',' + return_flag
            open(outfile, "a").write(plan + '\n')
    else:  # 计算先息后本
        int_m = amount * rate_m
        for p in range(1, int(term)):
            repay_serial = str(p)
            repay_date = cal_date(effdate, p)
            plan = loan_id + ',' + iou_id + ',' + repay_serial + ',' + repay_date + ',' + '{:.2f}'.format(int_m) \
                   + ',0.00,' + '{:.2f}'.format(int_m) + ',' + return_flag
            open(outfile, "a").write(plan + '\n')
        repay_serial = iou[6]
        repay_date = cal_date(effdate, repay_serial)
        plan = loan_id + ',' + iou_id + ',' + repay_serial + ',' + repay_date + ',' + '{:.2f}'.format(int_m) \
               + ',' + '{:.2f}'.format(amount) + ',' + '{:.2f}'.format(int_m + amount) + ',' + return_flag
        open(outfile, "a").write(plan + '\n')

    # doper = '{:.2%}'.format((i - 1) / (int(loaniou_lines) - 1))
    # print("\r请稍候，正在处理第 %s 条记录 ,已完成 %s" % (i - 1, doper), end='')

outfile_lines = len(open(outfile).readlines())
print("还款计划已生成！共 %s 条记录，输出文件 %s" % (outfile_lines - 1, outfile))
