'''
@FileName   :spider_semi.py
@Note       :半自动化爬虫
@Author     :人工智能2201 张杰 
@Log        :<2023/11/2> 半自动化爬虫, cookie失效后手动重置, 1h内成功爬取所有热门城市

'''
import requests
import time #用于sleep
import random #生成随机数，防止检测每次sleep时间相同
from selenium import webdriver
import jsonpath #解析接口返回的json数据
import json #处理json数据

HEADERS = {
    "Cookie": "lastCity=101200100; wd_guid=3023dd62-12a8-45f2-905f-c0e1a07aab94; historyState=state; _bl_uid=n3l7no4dfk4sFggIjmqjfjb4eLCq; wt2=DnW8QqNIffH4RCML-PPJKeuocA-8aHji6rSR_NoBybaz6V3Oa1cvNniSFXjvvDkeP_HG8nqwMNcwc3nuQPWnoRQ~~; wbg=0; Hm_lvt_194df3105ad7148dcf2b98a91b5e727a=1699102387,1699143078,1699153045,1699166625; __g=-; __c=1699244648; __l=l=%2Fwww.zhipin.com%2Fweb%2Fgeek%2Fjob%3Fquery%3DAI%26city%3D100010000&r=&g=&s=3&friend_source=0&s=3&friend_source=0; __a=61957306.1698845011.1699166607.1699244648.205.16.3.15; geek_zp_token=V1R9gjGeL02l9qVtRvxhQaLS625DvRwyo~; __zp_stoken__=2d9feaUp2a1dQVD8hKEgkM11TeHlSfHZbKVtnNElpdSZ3el0EWyoCaTs2L04lSmNlF3t0cQhddDpuIntkTSJWGwJpREhvQW9KFjUFK3AuJVBVHDAHHCkYQEdNWF4hGgMuVUJGDgxbC0d4bCE%3D",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0"
}

#首页url处理反爬
INDEX_URL = 'https://www.zhipin.com/'

#所有城市信息
CITY_SITE_URL = 'https://www.zhipin.com/wapi/zpgeek/common/data/city/site.json' #url
DATA_CITY_SITE = 'data/city.json'  #保存结果path

#待分析数据信息
BASE_URL = 'https://www.zhipin.com/wapi/zpgeek/search/joblist.json?scene=1&query=AI&city={city}&experience=&payType=&partTime=&degree=&industry=&scale=&stage=&position=&jobType=&salary=&multiBusinessDistrict=&multiSubway=&page={page}&pageSize=30' #url
DATA_CITY_JOBS = 'data/semi/data.csv' #结果保存path


def get_cities()->list:
    '''
    爬取所有城市代码信息
    选取热门城市
    :return: list 热门城市 
    '''
    print('start get city_site data')
    # 保存所有城市对应json数据到city_urls.json中
    try:
        json_response = requests.get(url=CITY_SITE_URL,headers=HEADERS).text
        with open(DATA_CITY_SITE,'w',encoding='utf-8')as f:
            f.write(json_response)
            print('success write city.json')
    except:
        print('获取城市数据失败，直接读取city.json')
    city_site = json.load(open(DATA_CITY_SITE,'r',encoding='utf-8'))

    #选取热门城市
    cities_list = jsonpath.jsonpath(city_site, '$.zpData.hotCitySites')
    return cities_list


def crawl(url,headers)->list:
    '''
    爬取url并解析，返回job数据列表
    :param url:url
    :param headers: 更新cookie后的header (待实现)
    :return: list
    '''
    response = requests.get(url=url,headers=headers)
    job_json = response.json()

    print('start crawling {url}'.format(url=url))

    #设置随机等待时间，降低爬取频率
    interval = random.randint(1,5)
    time.sleep(5+interval)

    #被反爬检测会返回 37 错误码，需要退出重置cookie
    if job_json['code'] == 37:
        print('行为受限，需要重置cookie')
        raise

    job_list = job_json['zpData']['jobList'] #成功爬取
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
    print('success crawl\n')
    return result


def get_job_details(urls, city_code):
    '''
    爬取指定城市所有url，并将该城市数据保存 (DATA_CITY_JOBS{city_code}.json)
    :param urls: 城市所有页面url
    :param city_code: 城市代码信息
    :return: None
    '''
    result = []
    with open(DATA_CITY_JOBS,'a',encoding='utf-8')as f:

        headers = HEADERS

        for url in urls:
            #捕获由crawl()抛出的异常，处理失效cookie
            try:
                data = crawl(url=url,headers=headers)
                result=result+data
            except:
                #需要手动改cookie，半自动化
                headers['Cookie'] = input('请输入新的cookie:')
                data = crawl(url=url,headers=headers)
                result=result+data

        print('program success!')
        json.dump(result,f,indent=4,ensure_ascii=False) #若不加ensure_ascii=false 汉字部分保存的是转义字符


def rotate_urls_crawl():
    '''
    循环爬取每个城市
    :return: None
    '''
    #获取所需城市
    code_list = get_cities() 

    #循环每个城市爬取
    urls = []
    for city in code_list[0]:
        print('爬取城市信息： ',end='');print(city)
        for i in range(1,11):
            url = BASE_URL.format(city = city['code'],page=i)
            urls.append(url)
        get_job_details(urls,city['code'])
        urls.clear()
        print('成功爬取城市： ',end='');print(city)


if __name__ == '__main__':
    rotate_urls_crawl()
