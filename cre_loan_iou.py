# -*- Codeing:UTF-8
# -*- Richard(410982635@qq.com)
# -*- 2018.08.01

import linecache
import os
import random
from tqdm import *

PWD = os.getcwd()
file_loan_info = PWD + '/OutFiles/loan_agreement.txt'

# 检查工作目录是否存在，不存在则创建目录
if not os.path.exists(PWD + '/Parameters'):
    os.mkdir(PWD + '/Parameters')

if not os.path.exists(PWD + '/OutFiles'):
    os.mkdir(PWD + '/OutFiles')

# 检查依赖文件是否存在
try:
    f1 = open(file_loan_info)
    f1.close()
except FileNotFoundError:
    print("发现错误：贷款协议文件 \"%s\" 不存在！" % file_loan_info)
    os._exit(0)

loanagr_lines = len(open(file_loan_info).readlines())
print('\r' + "找到 %s 条贷款协议数据，正在生成借据信息……" % (loanagr_lines - 1))

outfile = PWD + '/OutFiles/loan_iou.txt'
title = "协议编号,借据编号,借据金额,借据币种,剩余本金,借据利率,借据期限,期限单位,还款方式,还款顺序,罚息利率," \
        "提前还款标志,提前还款费率,展期标志,展期费率,生效日期,到期日期,借据状态,欠款期数,起欠期数,欠还利息,欠还本金,欠还金额"
open(outfile, "w").write(title + '\n')

for i in tqdm(range(2, loanagr_lines + 1)):
    agreement = linecache.getline(file_loan_info, i).split(',')
    loan_id = agreement[1]
    iou_id = str(random.randint(100, 120))
    iou_amount = agreement[6]
    iou_currency = agreement[7]
    iou_remamount = agreement[8]
    iou_rate = agreement[9]
    iou_term = agreement[10]
    iou_termunit = agreement[11]
    iou_method = random.choice(["0", "1", "2"])
    repay_order = "0"
    def_rate = random.choice(["0.5", "0.8", "1.0", "1.2", "1.5"])
    prepay_flag = random.choice(["0", "1"])
    if prepay_flag == "0":
        prepay_fee = random.choice(["1.0", "2.0", "3.0"])
    else:
        prepay_fee = "0.0"
    change_flag = random.choice(["0", "1"])
    if change_flag == "0":
        change_fee = random.choice(["3.0", "4.0", "5.0"])
    else:
        change_fee = "0.0"
    iou_effdate = agreement[13]
    iou_duedate = agreement[14]
    iou_stat = "0"
    iou_defcount = "0"
    iou_defstart = "0"
    iou_defint = "0.00"
    iou_defprin = "0.00"
    iou_defamount = "0.00"
    # 格式化输出内容
    iou_result = loan_id + ',' + iou_id + ',' + iou_amount + ',' + iou_currency + ',' + iou_remamount + ',' + \
                 iou_rate + ',' + iou_term + ',' + iou_termunit + ',' + iou_method + ',' + repay_order + ',' + \
                 def_rate + ',' + prepay_flag + ',' + prepay_fee + ',' + change_flag + ',' + change_fee + ',' + \
                 iou_effdate + ',' + iou_duedate + ',' + iou_stat + ',' + iou_defcount + ',' + iou_defstart + ',' + \
                 iou_defint + ',' + iou_defprin + ',' + iou_defamount

    # 输出文件
    open(outfile, 'a').write(iou_result + '\n')
outfile_lines = len(open(outfile).readlines())
print('\r' + "借据已生成！共 %s 条记录，输出文件 %s" % (outfile_lines - 1, outfile))
