# -*- coding: utf-8 -*-

import json
import scrapy
from scrapy import FormRequest,Request

from wenshu.items import WenshuItem
class CourtSpider(scrapy.Spider):
    name = "court"
    area_url = 'http://wenshu.court.gov.cn/List/TreeContent'
    court_url = 'http://wenshu.court.gov.cn/List/CourtTreeContent'
    content_url = 'http://wenshu.court.gov.cn/List/ListContent'
    def start_requests(self):
        """获取省一级地区"""

        formdata = {
            'Param':'全文检索:诈骗',
        }
        yield FormRequest(url=self.area_url,
                          formdata=formdata,
                          dont_filter=True,
                          callback=self.parse)



    def parse(self, response):
        """解析省级地名"""
        try:
            data = json.loads(response.body)
            areaName_list = [item['Key'] for item in data[3]['Child']]
            for areaName in areaName_list:
                formdata = {
                    'Param':'全文检索:诈骗,法院地域:%s'%(areaName)
                }
                yield FormRequest(url=self.court_url,
                                  formdata=formdata,
                                  meta={'areaName':areaName},
                                  dont_filter=True,
                                  callback=self.parse_second)
        except:
            print '获取省级域名内容失败，请检查！'

    def parse_second(self,response):
        """解析一级法院"""
        try:
            pass
            data = json.loads(response.body)
            first_court_list = [item['Key'] for item in data[0]['Child']]
            areaName = response.meta.get('areaName')
            for first_court in first_court_list:
                formdata = {
                    'Param':'全文检索:诈骗,法院地域:%s,中级法院:%s'%(areaName,first_court)
                }
                yield FormRequest(url=self.court_url,
                                  formdata=formdata,
                                  meta={'areaName':areaName,
                                        'first_court':first_court,
                                        },
                                  dont_filter=True,
                                  callback=self.parse_third,
                                  )
        except:
            pass

    def parse_third(self,response):
        """获取基层法院列表"""
        try:
            data = json.loads(response.body)
            areaName = response.meta.get('areaName')
            first_court = response.meta.get('first_court')
            second_court_list = [item['Key'] for item in data[0]['Child']]
            for second_court in second_court_list:
                formdata = {
                    'Param':'全文检索:诈骗,法院地域:%s,中级法院:%s,基层法院:%s'%(areaName,first_court,second_court),
                    'Index':'1',
                    'Page':'20',
                    'Order':'法院层级',
                    'Direction':'asc',
                }
                yield FormRequest(url=self.content_url,
                                  formdata=formdata,
                                  meta={'areaName':areaName,
                                        'first_court':first_court,
                                        'second_court':second_court,
                                        },
                                  dont_filter=True,
                                  callback=self.parse_list,
                                  )
        except:
            pass


    def parse_list(self,response):
        """解析列表项"""
        try:
            data = json.loads(response.body)
            total = data[0]['Count'] # 总记录
            for i in range(1,len(data)):
                id = data[i]['文书ID']
                url = 'http://wenshu.court.gov.cn/content/content?DocID=%s'%(id)
                yield Request(url=url,
                              meta={'case':data[i],
                                    'areaName':response.meta.get('areaName'),
                                    'first_court':response.meta.get('first_court'),
                                    'second_court':response.meta.get('second_court'),
                                    },
                              dont_filter=True,
                              callback=self.parse_detail,
                              )
            # 获取下一页


        except:
            print '解析列表项失败，请管理员检查！'

    def parse_detail(self,response):
        """解析"""
        item = WenshuItem()
        content = response.xpath('//div[@id="DivContent"]').extract_first()
        case = response.meta.get('case')
        item['content'] = content
        item['title'] = case.get('案件名称')
        item['date'] = case.get('裁判日期')
        item['document_code'] = case.get('案号')
        item['court'] = case.get('法院名称')
        item['type'] = case.get('案件类型')
        item['areaName'] = response.meta.get('areaName')
        item['first_court'] = response.meta.get('first_court')
        item['url'] = response.url
        item['source_crawl'] = 'wenshu.court.gov.cn'
        yield item









