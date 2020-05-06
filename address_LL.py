'''
将爬虫抓到的所有地址的经纬度通过高德地图的API转换出来
'''
import requests
import json
# 数据库配置
import pymysql
db = pymysql.connect(host='127.0.0.1',
                     port=3306,
                     user='root',
                     password='password',
                     db='sf',
                     charset='utf8')
cursor = db.cursor()

# try:
# 从表 sf_taobao 表中搜索数据
sql ='select * from sf_taobao'
cursor.execute(sql)  # 执行命令
content = cursor.fetchall() # 返回列表类型
# 遍历列表
for i in content:
    print(i[0])
    # 获取 address 的数据 因为是第一列 取每个数据的第一个元素
    keyword = i[0]
    # 拼接到高德地图的坐标拾取器访问链接
    url = 'https://restapi.amap.com/v3/place/text?s=rsv3&children=&key=8325164e247e15eea68b59e89200988b&page=1&offset=10&city=430500&language=zh_cn&callback=jsonp_751534_&platform=JS&logversion=2.0&sdkversion=1.3&appname=https%3A%2F%2Flbs.amap.com%2Fconsole%2Fshow%2Fpicker&csid=4A507AE3-28EE-47D5-9EB9-FB7CCA482B49&keywords={}'.format(keyword)
    # 关键是 cookie 值
    headers={
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-HK,zh;q=0.9,zh-CN;q=0.8,en;q=0.7,en-US;q=0.6,zh-TW;q=0.5",
        "Connection": "keep-alive",
        "Cookie": "UM_distinctid=171dabe788a2af-0658bec6864d5d-5313f6f-1fa400-171dabe788b724; cna=EjzNFcjlwBgCAW41PyFszgpg; isg=BHJyrIOUeD9afEc1BovWZLdew7hUA3adVoYmqTxK6CUQzxDJJJbRrMZmu2Pzv-41; l=eBSt4d_eqKMUUqYYBO5Zlurza77tXIObzsPzaNbMiIHca6OO6hL7UNQcuqCyJdtj_t5jTetPijrhsdE9rRUU-nkDBeYIVi3iOe96-e1..",
        "Host": "restapi.amap.com",
        "Referer": "https//lbs.amap.com/console/show/picker",
        "Sec-Fetch-Dest": "script",
        "Sec-Fetch-Mode": "no-cors",
        "Sec-Fetch-Site": "same-site",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36",
    }
    # 请求到的数据转换成 txt 格式
    # 必须去掉 jsonp_751534_( 内容数据 ) 去掉前面的部分可以使用替换 去掉后面的部分直接切片即可
    # 请求数据
    con = requests.get(url,headers=headers).text.replace('jsonp_751534_(','')[:-1]
    print(con)
    # 请求到的数据转换成 dict 格式
    con_dict = json.loads(con)
    print(con_dict)
    # 提取经纬度
    # 如果提取不到 则跳过
    try:
        data = con_dict['pois'][0]['location']
        # 将字符串的数据切割成2个部分值 一个经度一个纬度  必须进行一次转换成 str 才可
        final_data = str(data).split(',')
        # 输出经纬度进程提示
        print(final_data[0])
        print(final_data[1])

        # try:
        # 更新数据时报错 转义字符
        # https://yq.aliyun.com/articles/618481?type=2 如何使用 escape 函数
        # 如何解决转义字符的问题 https://blog.csdn.net/u013075468/article/details/51455745?utm_source=blogxgwz7
        # update_sql = "UPDATE sf_taobao set longitude='12' where url=%s UNION UPDATE sf_taobao set latitude='12' where url=%s"%db.escape(i[1]) %db.escape(i[1])
        # print(update_sql)
        # 将经度更新进去
        cursor.execute("UPDATE sf_taobao set longitude=%s where url=%s"%(final_data[0],db.escape(i[1])))
        # 不填加的话更新数据但是不改变值
        db.commit()

        # 将纬度更新进去
        cursor.execute("UPDATE sf_taobao set latitude=%s where url=%s"%(final_data[1],db.escape(i[1])))
        db.commit()

        # except:
        #     print("出错了")
    except:
        pass

# except:
#     pass
