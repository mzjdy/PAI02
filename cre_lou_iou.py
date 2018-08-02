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
#     还款方式,iou_method,char(1); 0-等额本息/1-等额本金/2-先息后本
#     还款顺序,repay_order,char(1); 0-费用_利息_本金/1-本金_利息_费用
#     罚息利率,def_rate,float(6,4);
#     提前还款标志,prepay_flag,char(1); 0-允许/1-不允许
#     提前还款费率,prepay_fee,float(6,4);
#     展期标志,change_flag,char(1); 0-允许/1-不允许
#     展期费率,change_fee,float(6,4);
#     生效日期,iou_effdate,date;
#     到期日期,iou_duedate,date;
#     借据状态,iou_stat.char(1); 0-正常/1-结清/2-逾期/3-其他

import os

PWD = os.getcwd()
file_loan_info = PWD + '/OutFiles/loan_agreement.txt'

# 检查依赖文件是否存在
try:
    f1 = open(file_loan_info)
    f1.close()
except FileNotFoundError:
    print("发现错误：贷款协议文件 \"%s\" 不存在！" % (file_loan_info))
    os._exit(0)
