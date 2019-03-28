from bs4 import BeautifulSoup
from sqlalchemy import String,Column,Integer,create_engine
from sqlalchemy.ext import declarative
from sqlalchemy.orm import Session
import time,os,crawl_begin,SQL_DATA

id1_page='1'    #1号传感器当前页数
id3_page='1'    #3号传感器当前页数
session=crawl_begin.login_to_logined() #获取登录成功后的session

id1_final_headers = {   #url不变，只是页码改变
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36',
            'Referer':'http://www.klha.net/History.do?method=findIotHistoryByCondition&gatewayId=600&sensorName=1'
}

id3_final_headers = {   #url不变，只是页码改变
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36',
            'Referer':'http://www.klha.net/History.do?method=findIotHistoryByCondition&gatewayId=600&sensorName=3'
}

def database_create():   #创建excel表格，用于存储数据
    SQL_DATA.init()

#通过登录成功获取的session，直接进入最终的数据网页地址，通过改变页码变量，来获取数据
def id1_get_final_data():
    global page
    database_create()
    id1_sensorId='1'    #编号为1的传感器
    startTime=''
    endTime=''
    gateway='查找'    #可以没有
    id1_curr=id1_page       #指定跳转的页码，即可获取相应的数值，此时为第一页
    textfield=''
    id1_final_data={
        'sensorId':id1_sensorId,
        'startTime':startTime,
        'endTime':endTime,
        #'gateway':gateway,
        'curr':id1_curr,
        'textfield':textfield
    }
    return id1_final_data

def id3_get_final_data():
    global page
    database_create()
    id3_sensorId='3'    #编号为1的传感器
    startTime=''
    endTime=''
    gateway='查找'    #可以没有
    id3_curr=id3_page       #指定跳转的页码，即可获取相应的数值，此时为第一页
    textfield=''
    id3_final_data={
        'sensorId':id3_sensorId,
        'startTime':startTime,
        'endTime':endTime,
        #'gateway':gateway,
        'curr':id3_curr,
        'textfield':textfield
    }
    return id3_final_data

def id1_final_process(final_data):
    global session
    url_28_id1='http://www.klha.net/History.do?method=findIotHistoryByCondition&gatewayId=600&sensorName=1'
    id1_final_response=session.post(url_28_id1,data=final_data,headers=id1_final_headers)
    id1_final_html=id1_final_response.text
    #print(final_response.url)
    return id1_final_html

def id3_final_process(final_data):
    global session
    url_28_id3 = 'http://www.klha.net/History.do?method=findIotHistoryByCondition&gatewayId=600&sensorName=3'
    id3_final_response = session.post(url_28_id3, data=final_data, headers=id3_final_headers)
    id3_final_html = id3_final_response.text
    #print(final_response.url)
    return id3_final_html

def get_spec_data():    #获取指定的数据，即一行温度、湿度等信息
    id1_final_data = id1_get_final_data()
    id1_final_html = id1_final_process(id1_final_data)
    id3_final_data = id3_get_final_data()
    id3_final_html = id3_final_process(id3_final_data)
    # print(id1_final_html)
    # print(id3_final_html)
    id1_data_bs=BeautifulSoup(id1_final_html,'html.parser')    #对指定的最后信息页面进行解析
    id1_data_list=id1_data_bs.select("div[class='STYLE2 STYLE1']")
    id3_data_bs = BeautifulSoup(id3_final_html, 'html.parser')  # 对指定的最后信息页面进行解析
    id3_data_list = id3_data_bs.select("div[class='STYLE2 STYLE1']")
    id1_pure_data_list=[]
    id3_pure_data_list = []
    # print(id1_data_list)
    # print(id3_data_list)
    for data in id1_data_list:
        id1_pure_data_list.append(data.get_text().replace('\t','').replace('\r','').replace('\n',''))
    id1_pure_data_list.pop(0)
    id1_pure_data_list.pop(0)
    id1_pure_data_list.pop(0)
    id1_pure_data_list.pop(0)
    id1_pure_data_list.pop(0)
    id1_pure_data_list.pop(0)
    id1_pure_data_list.pop(0)
    id1_pure_data_list.pop(0)
    id1_pure_data_list.pop(0)
    id1_pure_data_list.pop(0)
    # print(id1_pure_data_list)
    id1_split_pure_data_list = [id1_pure_data_list[i:i + 7] for i in range(0, len(id1_pure_data_list), 7)]  # 此时数据为二维数组，每行数据为一列表，列表的元素为每行数据的列表
    id1_split_pure_data_list.pop(0)
    # print(id1_split_pure_data_list)
    for data in id3_data_list:
        id3_pure_data_list.append(data.get_text().replace('\t','').replace('\r','').replace('\n',''))
    id3_pure_data_list.pop(0)
    id3_pure_data_list.pop(0)
    id3_pure_data_list.pop(0)
    id3_pure_data_list.pop(0)
    id3_pure_data_list.pop(0)
    id3_pure_data_list.pop(0)
    id3_pure_data_list.pop(0)
    id3_pure_data_list.pop(0)
    id3_pure_data_list.pop(0)
    id3_pure_data_list.pop(0)
    # print(id3_pure_data_list)
    id3_split_pure_data_list=[id3_pure_data_list[i:i + 2] for i in range(0, len(id3_pure_data_list), 2)]    #此时数据为二维数组，每行数据为一列表，列表的元素为每行数据的列表
    id3_split_pure_data_list.pop(0)
    # print(id3_split_pure_data_list)
    id1_id3_pure_data_list=id1_split_pure_data_list+id3_split_pure_data_list
    return id1_id3_pure_data_list

def add_to_sql(id1_id3_pure_data_list):
    session=SQL_DATA.Session()
    # print(id1_id3_pure_data_list)
    for num in range(len(id1_id3_pure_data_list)):
        id1_id3_data_time=id1_id3_pure_data_list[num][0]
        id1_id3_co2 = id1_id3_pure_data_list[num+20][1]
        id1_id3_air_temp = id1_id3_pure_data_list[num][1]
        id1_id3_air_humidity = id1_id3_pure_data_list[num][2]
        id1_id3_illuminate = id1_id3_pure_data_list[num][3]
        id1_id3_soil_temp = id1_id3_pure_data_list[num][4]
        id1_id3_soil_humidity = id1_id3_pure_data_list[num][5]

        to_sql_data_row=SQL_DATA.Crawl_data(date_time=id1_id3_data_time,co2=id1_id3_co2,air_temp=id1_id3_air_temp,
                                            air_humidity=id1_id3_air_humidity,illuminate=id1_id3_illuminate,
                                            soil_temp=id1_id3_soil_temp,soil_humidity=id1_id3_soil_humidity)
        session.add(to_sql_data_row)
        session.commit()
        session.close()
        if num ==19:
            break

if __name__ == '__main__':
    while True:
        id1_id3_pure_data_list=get_spec_data()
        time.sleep(1)
        if len(id1_id3_pure_data_list)==40:
            print(id1_id3_pure_data_list)
            print(len(id1_id3_pure_data_list))
            add_to_sql(id1_id3_pure_data_list)
            id1_page = str(int(id1_page) + 1)
            id3_page = str(int(id3_page) + 1)
            id1_id3_pure_data_list = []
            print(id1_id3_pure_data_list)
        else:
            time.sleep(1800)
            continue
