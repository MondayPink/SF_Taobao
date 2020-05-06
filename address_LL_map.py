"""
将转换出来的爬虫表中的经纬度和地址名称查询出来，去掉空值写入到 django 的 map_address_info 表中
"""
# 数据库配置
import pymysql
db = pymysql.connect(host='127.0.0.1',
                     port=3306,
                     user='root',
                     password='password',
                     db='sf',
                     charset='utf8')
cursor = db.cursor()
# 查找爬虫的表
sql ='select * from sf_taobao'
cursor.execute(sql)  # 执行命令
content = cursor.fetchall() # 转换成列表形式
# 遍历列表
for i in content:
    # 看纬度的数据是否为0
    if i[9]=='0':
        print(i)
    # 如果不为0 则插入到 django 的表中去
    else:
        # db.escape() 插入data 时 转义字符报错
        sql = "INSERT INTO map_address_info(longitude,latitude, data)VALUES('%s', '%s',  %s)"%(i[8],i[9],db.escape(i[0]))
        # 执行sql语句
        cursor.execute(sql)
        # 执行sql语句
        db.commit()