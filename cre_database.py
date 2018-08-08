import pymysql

# 连接mySQL服务器
print('正在连接mySQL服务器……')
con = pymysql.connect(user='python', passwd='pythonpwd', charset='utf8')
print('服务器连接成功！')
cur = con.cursor()

# 重建PAI库
cur.execute('DROP SCHEMA IF EXISTS PAI;')
cur.execute('CREATE SCHEMA IF NOT EXISTS PAI;')
con.commit()
print('数据库(PAI)已成功创建！')

# 创建个人客户信息表
cus = '''
    CREATE TABLE customer_info
    (
        cus_id varchar(12) NOT NULL primary key comment '客户编号',
        cus_name varchar(20) comment '客户姓名',
        cus_idtype varchar(1) comment '证件类型',
        cus_idnum varchar(20) comment '证件号码',
        cus_brith date comment '出生日期',
        cus_gender varchar(1) comment '客户性别',
        cus_marry varchar(1) comment '婚姻状态',
        cus_edu varchar(1) comment '教育程度',
        cus_occ varchar(1) comment '职业类别',
        cus_phone varchar(20) comment '联系电话',
        cus_email varchar(50) comment '电子邮件',
        cus_livetype varchar(1) comment '居住类型',
        cus_address varchar(100) comment '居住地址',
        cus_bank varchar(100) comment '开户银行',
        cus_cardcode varchar(1) comment '卡种代码',
        cus_cardname varchar(50) comment '卡种名称',
        cus_cardno varchar(20) comment '银行卡号',
        cre_branch varchar(10) comment '创建机构',
        cre_teller varchar(10) comment '创建柜员',
        cre_datetime datetime comment '创建时间'
    );
'''

# 创建贷款协议表
agree = '''
    CREATE TABLE loan_agreement
    (
        cus_id varchar(12) NOT NULL comment '客户编号',
        loan_id varchar(12) NOT NULL primary key comment '协议编号',
        loan_code varchar(5) comment '产品代码',
        loan_name varchar(100) comment '产品名称',
        loan_usedcode varchar(10) comment '用途代码',
        loan_usedname varchar(100) comment '贷款用途',
        loan_amount double(12,2) comment '贷款金额',
        loan_currency varchar(3) comment '贷款币种',
        loan_remamount double(12,2) comment '剩余本金',
        loan_rate double(6,4) comment '贷款利率',
        loan_term varchar(5) comment '贷款期限',
        loan_termunit varchar(1) comment '期限单位',
        loan_guaran varchar(1) comment '担保方式',
        loan_effdate date comment '生效日期',
        loan_duedate date comment '失效日期',
        loan_repaycardno varchar(20) comment '还款卡号',
        loan_branch varchar(10) comment '归属机构',
        loan_status varchar(1) comment '协议状态'
    );
'''

# 创建贷款借据表
iou = '''
    CREATE TABLE loan_iou
    (
        loan_id varchar(12) NOT NULL primary key comment '协议编号',
        iou_id varchar(3) NOT NULL comment '借据编号',
        iou_amount double(12,2) comment '借据金额',
        iou_cerrency varchar(3) comment '借据币种',
        iou_remamount double(12,2) comment '剩余本金',
        iou_rate double(6,4) comment '借据利率',
        iou_term varchar(5) comment '借据期限',
        iou_termunit varchar(1) comment '期限单位',
        iou_method varchar(1) comment '还款方式',
        iou_repayorder varchar(1) comment '还款顺序',
        iou_defrate double(6,4) comment '违约利率',
        iou_prepayflag varchar(1) comment '提前还款标志',
        iou_prepayfee double(6,4) comment '提前还款费率',
        iou_changeflag varchar(1) comment '变更标志',
        iou_changefee double(6,4) comment '变更费率',
        iou_effdate date comment '生效日期',
        iou_duedate date comment '失效日期',
        iou_status varchar(1) comment '借据状态'
    );
'''

# 创建还款计划表
plan = '''
    CREATE TABLE repay_plan
    (
        loan_id varchar(12) NOT NULL comment '协议编号',
        iou_id varchar(3) NOT NULL comment '借据编号',
        repay_serial varchar(5) comment '还款期数',
        repay_date date comment '应还日期',
        repay_int double(12,2) comment '应还利息',
        repay_prin double(12,2) comment '应还本金',
        repay_amount double(12,2) comment '应还金额',
        return_flag varchar(1) comment '还款标志'
    );
'''

# 创建还款历史表
his = '''
    CREATE TABLE repay_history
    (
        loan_id varchar(12) NOT NULL comment '协议编号',
        iou_id varchar(3) NOT NULL comment '借据编号',
        return_bill varchar(3) comment '还款期数',
        return_date date comment '还款日期',
        return_int double(12,2) comment '实还利息',
        return_prin double(12,2) comment '实还本金',
        return_amount double(12,2) comment '实还金额',
        retrurn_flag varchar(1) comment '还款标志'
    );
'''

# 创建违约历史表
defa = '''
    CREATE TABLE loan_default
    (
        loan_id varchar(12) NOT NULL comment '协议编号',
        iou_id varchar(3) NOT NULL comment '借据编号',
        repay_serial varchar(5) comment '还款期数',
        repay_date date comment '应还日期',
        def_int double(12,2) comment '欠还利息',
        def_prin double(12,2) comment '欠还本金',
        def_amount double(12,2) comment '欠还金额',
        return_flag varchar(1) comment '还款标志'
    );
'''
cur.execute('USE PAI;')
cur.execute(cus)
print('个人客户信息数据表(customer_info)已成功创建！')
cur.execute(agree)
print('贷款协议数据表(loan_agreement)已成功创建！')
cur.execute(iou)
print('贷款借据数据表(loan_iou)已成功创建！')
cur.execute(plan)
print('还款计划数据表(repay_plan)已成功创建！')
cur.execute(his)
print('还款历史数据表(repay_history)已成功创建！')
cur.execute(defa)
print('违约历史数据表(loan_default)已成功创建！')
con.commit()
