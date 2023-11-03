'''
@FileName  :spider.py
@Author    :人工智能2201 张杰 0122210880325
@Time      :2023/11/3
'''
import requests
from bs4 import BeautifulSoup
import re
import time
import urllib.request

from lxml import etree

import json
import jsonpath

HEADERS = {
    "Cookie": "historyState=state; wd_guid=697d23d1-3842-48be-bc2d-92c1539e82bd; _bl_uid=yClgjogIgCnhyFmbOzn90wha7z5s; wt2=DNVKmWbB9AvmKPAq6n8ihroTPwKtwtAld8l3rwz3id_DQcRlYMW6MYnxd4vrE5aUsEq345bHEw_y8GgW0QdfuFA~~; wbg=0; Hm_lvt_194df3105ad7148dcf2b98a91b5e727a=1698887306,1698908507,1698927636; __a=80638911.1698887306.1698908504.1698927635.21.3.13.21; __zp_stoken__=e8dbeKXcFRkYzUUdiOyd9TQIjLi5jFVBHQQYAbHAydScLDTNpMDNjKFciPmIOdn0YQS5SMWBxZklNR0M8aHZxBEZJbTJ%2BVhICIFx%2Fc0l7Jl0sSQhZF24iMTNBeSlURgNNAxdgTmAORUByBkY%3D; __zp_sname__=f53019a5; __zp_sseed__=CzYPiBBv8XJiGwyso/lWvDGWxBANieTfHBEeAhjy4eY=; __zp_sts__=1698980307568",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36 SLBrowser/8.0.1.4031 SLBChan/105"
}
CITY_URL = 'https://www.zhipin.com/wapi/zpgeek/common/data/city/site.json'
CITY_JSON = '../data/city.json'
BASE_URL = 'https://www.zhipin.com/wapi/zpgeek/search/joblist.json?scene=1&query=AI&city={city}&experience=&payType=&partTime=&degree=&industry=&scale=&stage=&position=&jobType=&salary=&multiBusinessDistrict=&multiSubway=&page={page}&pageSize=30'
CSV_PATH = '../data/city.csv'

def request_gen():
    request = urllib.request.Request(url = CITY_URL, headers=HEADERS)
    return request


def get_city_code_list()->list:
    '''
    保存并解析城市json数据，提取城市代号
    :return: list:city_code_list
    '''
    print('start get city_json')
    # 返回城市对应json数据
    json_response = urllib.request.urlopen(request_gen()).read().decode('utf-8')
    print(json_response)
    #保存json数据
    with open(CITY_JSON,'w',encoding='utf-8')as f:
        f.write(json_response)
    print('success get city_json')
    # obj = json.load(CITY_JSON)
    
    # code_list = jsonpath.jsonpath(obj, '')
    # return code_list
    

#设置Headers处理反爬


#爬取每页AI岗位信息
# url_list = [BASEURL.format(page = page) for page in range(1,11)] #1-10页url
# # for url in url_list:
# url = url_list[0]
# data = requests.get(url=url, headers = HEADERS).content.decode('utf-8') #发送请求，获取每页响应数据
# print(data)
# #使用beautifulsoup提取数据
# soup = BeautifulSoup(data, 'lxml')
# job_card_wrappers = soup.find_all('div',attrs={"class":"job-card-wrapper"}) #提取出job_card_wrapper
# print(job_card_wrappers)
# time.sleep(1)

if __name__ == '__main__':
    city_code_list = get_city_code_list()
    # print(city_code_list)
    # for item in city_code_list:
    #     print(item)
