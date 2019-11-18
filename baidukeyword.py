import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import datetime
from pyquery import PyQuery as pq
from selenium.webdriver.common.keys import Keys
from urllib.parse import quote
import pandas as  pd
def load_data(file):
    data=pd.read_csv(file,encoding='gbk')
    return data
def process(data):
    keywords=data['关键词']
    nk=keywords.map(lambda x: '江苏'+x)
    return nk
def search(key):
    n_key=quote(key)
    url=base_url.format(n_key)
    try:
        browser.get(url)
    except TimeoutException:
        return search(key)
def next_page():
    button=wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div#page>a.n')))
    button.send_keys(Keys.ENTER)
    time.sleep(2)
def parse_page(key):
    c=0
    result=pd.DataFrame()
    all_key=[]
    all_host=[]
    all_time=[]
    all_title=[]
    all_red_title=[]
    all_content=[]
    all_red_content=[]
    all_rank=[]
    html=browser.page_source
    doc=pq(html)
    items=doc('div#content_left').children().items()
    for item in items:
        
        c+=1
        all_rank.append(c)
        a=item.find('a>span').text()
        process_a=a.split(' ')
        
        try:
            host=process_a[0]
        except Exception:
            host=''
        host=host.encode('gbk','ignore').decode('gbk','ignore')
        all_host.append(host)
        time = datetime.datetime.now().strftime('%Y/%m/%d %H:%M')
        all_time.append(time)
        title=item.find('h3 > a').text()
        title=title.encode('gbk','ignore').decode('gbk','ignore')
        all_title.append(title)
        red_title=item.find('h3>a>em').text()
        red_title=red_title.encode('gbk','ignore').decode('gbk','ignore')
        all_red_title.append(red_title)
        content=item.find('div.c-abstract').text()
        content=content.encode('gbk','ignore').decode('gbk','ignore')
        all_content.append(content)
        red_content=item.find('div.c-abstract>em').text()
        red_content=red_content.encode('gbk','ignore').decode('gbk','ignore')
        all_red_content.append(red_content)
        all_key.append(key)
        
    result['抓取时间']=all_time
    result['搜索词']=all_key        
    result['创意标题']=all_title
    result['标题飘红']=all_red_title
    result['创意描述']=all_content
    result['描述飘红']=all_red_content
    result['广告主']=all_host
    result['排名']=all_rank
    print(result)
    return result
def save(outputfile,result_list):
    result=pd.concat(result_list,ignore_index=True)
    result.to_csv(outputfile,index=False,encoding='gbk')


if __name__ == "__main__":
    browser=webdriver.Chrome()
    wait=WebDriverWait(browser, 10)
    base_url='https://www.baidu.com/s?wd={}'
    file='鲜花礼品.csv'
    outputfile='result.csv'
    data=load_data(file)
    nk=process(data)
    length=len(nk)
    l=[]
    for i in range(400,500):
        key=nk[i]
        search(key)
        r=parse_page(key)
        l.append(r)
    save(outputfile,l)




