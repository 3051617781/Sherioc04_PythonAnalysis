'''
@FileName  :spider.py
@Author    :人工智能2201 张杰 0122210880325
@Time      :2023/11/3
'''
import requests
import time
import random
# from selenium import webdriver
# from lxml import etree

import json
import jsonpath

HEADERS = {
    "Cookie": "lastCity=101200100; wd_guid=3023dd62-12a8-45f2-905f-c0e1a07aab94; historyState=state; _bl_uid=n3l7no4dfk4sFggIjmqjfjb4eLCq; wt2=DnW8QqNIffH4RCML-PPJKeuocA-8aHji6rSR_NoBybaz6V3Oa1cvNniSFXjvvDkeP_HG8nqwMNcwc3nuQPWnoRQ~~; wbg=0; Hm_lvt_194df3105ad7148dcf2b98a91b5e727a=1698931210,1698936230,1699019569,1699092949; __g=-; __c=1699096276; __l=l=%2Fwww.zhipin.com%2Fweb%2Fgeek%2Fjob%3Fquery%3DAI%26city%3D100010000%26page%3D2&r=&g=&s=3&friend_source=0&s=3&friend_source=0; __a=61957306.1698845011.1699092947.1699096276.69.10.7.69; __zp_stoken__=5935eZ2YRV115VBYjX3gkAHxeU3cxXVgmb0hbDTUyZwtzW293Lk0%2BYxI2EW0hHyFWNnZffyQ2QzUTLW1dKgwsTFIRGQZhIE5EOjglEgw1WRRCERtZPjY%2BSG5NZGddGBEddE9tACA8N01RbB0%3D",

    "Referer":"https://www.zhipin.com/web/geek/job",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0"
}
#获取并生成url
CITY_SITE_URL = 'https://www.zhipin.com/wapi/zpgeek/common/data/city/site.json'
DATA_CITY_SITE = 'data/city.json'
DATA_CITY_URLS = 'data/city_urls.json.'
#待分析数据信息url
BASE_URL = 'https://www.zhipin.com/wapi/zpgeek/search/joblist.json?scene=1&query=AI&city={city}&experience=&payType=&partTime=&degree=&industry=&scale=&stage=&position=&jobType=&salary=&multiBusinessDistrict=&multiSubway=&page={page}&pageSize=30'
#待分析数据
DATA_CITY_JOBS = 'data/city_jobs.json'


def get_city_urls()->list:
    '''
    通过CITY_SITE_URL爬取城市数据并保存到 DATA_CITY_SITE
    提取热门城市并生成url，保存url到 DATA_CITY_URLS
    '''
    print('start get city_json')
    # 保存所有城市对应json数据，已经保存在city_urls.json中
    # json_response = requests.get(url=CITY_SITE_URL,headers=HEADERS).text
    # with open(DATA_CITY_SITE,'w',encoding='utf-8')as f:
    #     f.write(json_response)
    #     print('success write in')
    city_site = json.load(open(DATA_CITY_SITE,'r',encoding='utf-8'))

    #生成热门城市url并写入文件
    code_list = jsonpath.jsonpath(city_site, '$.zpData.hotCitySites')
    urls = []
    for city in code_list[0]:
        for i in range(1,11):
            url = BASE_URL.format(city = city['code'],page=i)
            urls.append(url)
    print('start write city_urls')
    with open(DATA_CITY_URLS,'w')as f:
        json.dump(urls,f,indent=4)
    return urls


def crawl(url)->list:
    '''
    爬取一页（指定城市、指定页）并解析，返回该页job数据列表
    :param url:每个url
    :return: list
    '''
    response = requests.get(url=url,headers=HEADERS)
    job_json = response.json()

    print('start crawling {url}'.format(url=url))

    interval = random.randint(1,5)
    time.sleep(5+interval)

    job_list = job_json['zpData']['jobList']
    result = []
    for i in job_list:
        data = {
            "jobName":i['jobName'],
            "salaryDesc":i['salaryDesc'],
            "jobLabels":i['jobLabels'],
            "skills":i['skills'],
            "jobExperience":i['jobExperience'],
            "jobDegree":i['jobDegree'],
            "cityName":i['cityName'],
            "areaDistrict":i['areaDistrict'],
            "brandIndustry":i['brandIndustry'],
            "welfareList":i['welfareList'],

        }
        result.append(data)
    print('success crawl')
    return result

def get_job_details():
    '''
    使用每个url爬取数据，并将最终job数据保存到 DATA_CITY_JOBS 中
    :return: None
    '''
    urls = get_city_urls()
    result = []
    with open(DATA_CITY_JOBS,'w',encoding='utf-8')as f:
        for url in urls:
            #可能出现异常
            try:
                data = crawl(url)
                result=result+data
            except:
                print('cookie failed')
                break

        print('program success!')
        json.dump(result,f,indent=4,ensure_ascii=False) #若不加ensure_ascii=false 汉字部分保存的是转义字符


if __name__ == '__main__':
    # browser = webdriver.Edge()
    # browser.get('https://www.zhipin.com/web/geek/job?')
    # cookie = browser.get_cookies()
    # cookie_str = ''

    # print(cookie)
    get_job_details()
