# -*- coding: utf-8 -*-

from time import sleep
import json
import scrapy


from scrapy import FormRequest,Request

class CaseSpider(scrapy.Spider):
    name = "case"
    post_url = 'http://wenshu.court.gov.cn/List/ListContent'

    def start_requests(self):
        """重写请求入口函数"""
        formdata = {
            'Param':'案件类型:刑事案件,全文检索:诈骗,文书类型:判决书',
            'index':'1',
            'Page':'5',
            'Order':'法院层级',
            'Direction':'asc',
        }
        yield FormRequest(url=self.post_url,
                          formdata=formdata,
                          meta={'dont_cache':True,
                                'formdata':formdata},
                          callback=self.parse,
                          dont_filter=True,
                          )

    def parse(self, response):
        """解析接口数据"""
        if 'remind' in response.body:
            print '访问过于频繁，服务器拒绝访问！'
            sleep(10)
        else:
            data = json.loads()
            for item in data:
                print item,