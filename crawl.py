import requests
from pyquery import PyQuery as pq
import time
import datetime
import pandas as pd
from urllib.parse import quote


class Spider(object):
    def __init__(self,file):
        self.keywords = []
        self.headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"}
        self.base_url = 'https://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=1&rsv_idx=1&tn=baidu&wd={}'
        self.length = 0
        self.l = []
        self.file = file
        self.output_file = 'result.csv'
        
        
    def get_keywords(self):
        df = pd.read_csv(self.file,encoding='gbk')
        kwd = df['关键词']
        self.keywords = list(kwd.map(lambda x:'江苏'+x))
        self.length = len(self.keywords)
        
        
    def get_response(self,key):
        
        print('正在获取{}页面'.format(key))
        n_key = quote(key)
        url =  self.base_url.format(n_key)
        try:   
            res = requests.get(url,headers=self.headers)
            return res.text
        except Exception as e:
            print('----该页发生异常{}----'.format(e))
            time.sleep(60)
            return self.get_response(key)
    
    def parse_response(self,key):
        res = self.get_response(key)
        print('正在解析{}页面'.format(key))
        doc = pq(res)
        items = doc('div#content_left').children().items()
        c = 0
        result = pd.DataFrame()
        all_key = []
        all_host = []
        all_time = []
        all_title =  []
        all_red_title = []
        all_content = []
        all_red_content = []
        all_rank = []
        for item in items:
            c += 1
            process = item.find('a>span').text().split(' ')
            try:
                host = process[0]
            except Exception as e:
                host = ''
            host = host.encode('gbk','ignore').decode('gbk','ignore')
            if  '广告' in process:
                all_host.append(host)
                time = datetime.datetime.now().strftime('%Y/%m/%d %H:%M')
                all_time.append(time)
                title = item.find('h3 > a').text()
                title = title.encode('gbk','ignore').decode('gbk','ignore')
                all_title.append(title)
                red_title = item.find('h3>a>em').text()
                red_title = red_title.encode('gbk','ignore').decode('gbk','ignore')
                all_red_title.append(red_title)
                content = item.find('div.c-abstract').text()
                content =content.encode('gbk','ignore').decode('gbk','ignore')
                all_content.append(content)
                red_content = item.find('div.c-abstract>div>div>div>font').text()
                red_content = red_content.encode('gbk','ignore').decode('gbk','ignore')
                all_red_content.append(red_content)
                all_key.append(key)
            else:
                all_host.append(host)
                time = datetime.datetime.now().strftime('%Y/%m/%d %H:%M')
                all_time.append(time)
                title = item.find('h3 > a').text()
                title = title.encode('gbk','ignore').decode('gbk','ignore')
                all_title.append(title)
                red_title = item.find('h3>a>em').text()
                red_title = red_title.encode('gbk','ignore').decode('gbk','ignore')
                all_red_title.append(red_title)
                content = item.find('div.c-abstract').text()
                content = content.encode('gbk','ignore').decode('gbk','ignore')
                all_content.append(content)
                red_content = item.find('div.c-abstract>em').text()
                red_content = red_content.encode('gbk','ignore').decode('gbk','ignore')
                all_red_content.append(red_content)
                all_key.append(key)
                
            all_rank.append(c)
        result['抓取时间'] = all_time
        result['搜索词'] = all_key        
        result['创意标题'] = all_title
        result['标题飘红'] = all_red_title
        result['创意描述'] = all_content
        result['描述飘红'] = all_red_content
        result['广告主'] = all_host
        result['排名'] = all_rank
        print(result)
        return result
    
    def run(self):
        self.get_keywords()
        for key in self.keywords:
            res = self.parse_response(key)
            self.l.append(res)
        result = pd.concat(self.l,ignore_index=True)
        result.to_csv(self.output_file,encoding='gbk',index=False)
        
        
if __name__ == "__main__":
    file = 'kwd.csv'
    sp = Spider(file)
    sp.run()
    
