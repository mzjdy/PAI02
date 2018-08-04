# -*- Codeing:UTF-8
# -*- Richard(410982635@qq.com)
# -*- 2018.08.01

# 贷款借据-loan_iou
#     协议编号,loan_id,chr(12);
#     借据编号,iou_id,char(3);
#     借据金额,iou_amount,float(12,2);
#     借据币种,iou_currency,char(3); 001-人民币
#     剩余本金,iou_remamount,float(12,2);
#     借据利率,iou_rate,float(6,4);
#     借据期限,iou_term,char(5);
#     期限单位,iou_termunit,char(1); 0-天/1-月/2-季/3-年
#     还款方式,iou_method,char(1); 0-等额本息/1-等额本金/2-先息后本
#     还款顺序,repay_order,char(1); 0-费用_利息_本金/1-本金_利息_费用
#     罚息利率,def_rate,float(6,4);
#     提前还款标志,prepay_flag,char(1); 0-允许/1-不允许
#     提前还款费率,prepay_fee,float(6,4);
#     展期标志,change_flag,char(1); 0-允许/1-不允许
#     展期费率,change_fee,float(6,4);
#     生效日期,iou_effdate,date;
#     到期日期,iou_duedate,date;
#     借据状态,iou_stat,char(1); 0-正常/1-结清/2-逾期/3-其他

import os
import linecache
import random

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
print("找到 %s 条贷款协议数据，正在生成借据信息！" % (loanagr_lines - 1))

outfile = PWD + '/OutFiles/loan_iou.txt'
title = "协议编号,借据编号,借据金额,借据币种,剩余本金,借据利率,借据期限,期限单位,还款方式,还款顺序,罚息利率," \
        "提前还款标志,提前还款费率,展期标志,展期费率,生效日期,到期日期,借据状态"
open(outfile, "w").write(title + '\n')

for i in range(2, loanagr_lines + 1):
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
    # 格式化输出内容
    iou_result = loan_id + ',' + iou_id + ',' + iou_amount + ',' + iou_currency + ',' + iou_remamount + ',' + \
                 iou_rate + ',' + iou_term + ',' + iou_termunit + ',' + iou_method + ',' + repay_order + ',' + \
                 def_rate + ',' + prepay_flag + ',' + prepay_fee + ',' + change_flag + ',' + change_fee + ',' + \
                 iou_effdate + ',' + iou_duedate + ',' + iou_stat

    # 输出文件
    doper = '{:.2%}'.format(i / int(loanagr_lines))
    print("\r请稍候，正在处理第 %s 条记录 ,已完成 %s" % (i - 1, doper), end='')
    open(outfile, 'a').write(iou_result + '\n')

outfile_lines = len(open(outfile).readlines())
print("\n" + "借据已生成！共 %s 条记录，输出文件 %s" % (outfile_lines - 1, outfile))
