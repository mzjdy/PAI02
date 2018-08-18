# -*- Codeing:UTF-8
# -*- Richard(410982635@qq.com)
# -*- 2018.08.01

import datetime
import linecache
import os
import random
import time
from dateutil.relativedelta import relativedelta
from tqdm import *

PWD = os.getcwd()
file_cus_info = PWD + '/OutFiles/customer_info.txt'
file_loanproduct = PWD + '/Parameters/loan_product.txt'
file_loanused = PWD + '/Parameters/loan_usedcode.txt'

# 检查工作目录是否存在，不存在则创建目录
if not os.path.exists(PWD + '/Parameters'):
    os.mkdir(PWD + '/Parameters')

if not os.path.exists(PWD + '/OutFiles'):
    os.mkdir(PWD + '/OutFiles')

# 检查依赖文件是否存在
try:
    f1 = open(file_cus_info)
    f1.close()
except FileNotFoundError:
    print("发现错误：个人客户信息文件 \"%s\" 不存在！" % file_cus_info)
    os._exit(0)

try:
    f1 = open(file_loanproduct)
    f1.close()
except FileNotFoundError:
    print("发现错误：贷款产品信息文件 \"%s\" 不存在！" % file_loanproduct)
    os._exit(0)

try:
    f1 = open(file_loanused)
    f1.close()
except FileNotFoundError:
    print("发现错误：贷款用途代码文件 \"%s\" 不存在！" % file_loanused)
    os._exit(0)


def get_loan_agreement():
    # 读取个人客户信息文件中的"客户编号"、"银行卡号"
    cusifno_lines = len(open(file_cus_info).readlines())
    record = linecache.getline(file_cus_info, random.randint(2, cusifno_lines)).split(',')
    cus_id = record[0]
    repay_cardno = record[16]

    loan_id = cus_id[:4] + "".join(random.choice("0123456789") for i in range(8))

    # 生成产品编号、名称
    productinfo_lines = len(open(file_loanproduct).readlines())
    productinfo = linecache.getline(file_loanproduct, random.randint(2, productinfo_lines)).strip('\n').split(',')
    loan_code = productinfo[0]
    loan_name = productinfo[1]
    amount_mix = productinfo[2]
    amount_max = productinfo[3]

    # 生成用途代码、贷款用途
    loanused_lines = len(open(file_loanused).readlines())
    while True:
        loanused = linecache.getline(file_loanused, random.randint(1, loanused_lines)).strip('\n').split(',')
        loan_usedcode = loanused[0]
        loan_used = loanused[1]
        if loan_usedcode[:3] == productinfo[0]:
            break

    # 生成贷款金额、币种，初始化剩余本金=贷款本金，初始化贷款状态为"正常"
    preamount = random.randint(int(amount_mix), int(amount_max))
    loan_amount = str(preamount * 1000) + '.00'
    loan_currency = '156'
    loan_remamount = loan_amount
    loan_stat = '0'

    # 生成贷款利率、期限、期限单位、担保方式、贷款机构
    loan_rate = random.choice(["7.2", "8.4", "9.6", "10.8", "12.0"])
    loan_term = random.choice(["3", "6", "12", "18", "24"])
    loan_termunit = '1'
    loan_guaran = random.choice(["0", "1", "2", "3"])
    loan_branch = cus_id[:4] + "".join(random.choice("0123456789") for i in range(4))

    # 生成生效日期
    starttime = time.mktime((2018, 1, 1, 0, 0, 0, 0, 0, 0))
    endtime = time.mktime((2018, 7, 31, 23, 59, 59, 0, 0, 0))
    randomtime = time.localtime(random.randint(starttime, endtime))
    loan_effdate = time.strftime("%Y-%m-%d", randomtime)

    # 计算到期日期
    predate = datetime.datetime.strptime(loan_effdate, "%Y{y}%m{m}%d{d}".format(y='-', m='-', d=''))
    loan_duedate = str(predate + relativedelta(months=+int(loan_term)))[:10]

    # 格式化输出内容
    loan_result = cus_id + ',' + loan_id + ',' + loan_code + ',' + loan_name + ',' + loan_usedcode + ',' + loan_used \
                  + ',' + loan_amount + ',' + loan_currency + ',' + loan_remamount + ',' + loan_rate + ',' + loan_term \
                  + ',' + loan_termunit + ',' + loan_guaran + ',' + loan_effdate + ',' + loan_duedate + ',' + \
                  repay_cardno + ',' + loan_branch + ',' + loan_stat

    return loan_result


# 输出文件
outfile = PWD + '/OutFiles/loan_agreement.txt'
title = "客户编号,协议编号,产品编号,产品名称,用途代码,贷款用途,贷款金额,贷款币种,剩余本金,贷款利率,贷款期限,期限单位,担保方式," \
        "生效日期,到期日期,还款卡号,贷款机构,贷款状态"
open(outfile, "w").write(title + '\n')
# info_num = input('\r' + "请输入拟生成的贷款协议条数：")
while True:
    info_num = input('\r' + "请输入拟生成的贷款协议数量：")
    if str.isdigit(info_num) == True:
        break
    else:
        print('数字格式不合法，请重新输入……')
for i in tqdm(range(0, int(info_num))):
    open(outfile, 'a').write(get_loan_agreement() + '\n')
outfile_lines = len(open(outfile).readlines())
print("贷款协议已生成！共 %s 条记录，输出文件 %s" % (outfile_lines - 1, outfile))
