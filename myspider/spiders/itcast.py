import scrapy
from ..items import MyspiderItem

class ItcastSpider(scrapy.Spider):
    name = 'itcast'
    
    def start_requests(self):
	    link='https://sz.fang.ke.com/loupan/pg{}'
	    for i in range(1,50):
		    url=link.format(i)
		    yield scrapy.Request(url=url, callback=self.parse)

    def parse(self,response):
        t_list = response.xpath('/html/body/div[6]/ul[2]/li')
        item = MyspiderItem()
        # 遍历教师节点列表
        for teacher in t_list:
            item['next_url'] = teacher.xpath('./a/@href').extract()[0] # 下一层链接

            s_url = 'https://sz.fang.ke.com'
            s_url += item['next_url']

            item['title'] = teacher.xpath('./a/@title').extract()[0] # 房地名字
            item['img_url'] = teacher.xpath('./a/img/@src').extract()[0] # 图片地址
            item['tag'] = teacher.xpath('./div/div[1]/span[1]/text()').extract()[0] # 房子在售状态
            item['tag_2'] = teacher.xpath('./div/div[1]/span[2]/text()').extract()[0] # 房子类型（住宅等、商业等、写字楼）
            item['location'] = teacher.xpath('/html/body/div[6]/ul[2]/li[1]/div/a[1]/text()[2]').extract()[0] # 所处地理位置

            # item['acreage'] = teacher.xpath('./div/a[2]/span[5]/text()').extract()[0] # 房子总面积
            item['house_money'] = teacher.xpath('./div/div[4]/div[1]/span[1]/text()').extract()[0] # 房子价格（每平方米）
            
            yield scrapy.Request(
                s_url,
                callback=self.parse_detail,
                meta={"item": item}
            )

    def parse_detail(self, response):
        item = response.meta["item"]
        
        father_nodes = response.xpath('/html/body/div[2]')
        item['alias'] = father_nodes.xpath('./div[2]/div/div[2]/text()').extract()[0] # 房子别名
        # alias_list = father_nodes.xpath('./div[2]/div/div[2]/text()').extract()
        # if len(alias_list) > 0:
        #     item['alias'] = alias_list[0]
        # else:
        #     item['alias'] = ''

        
        item['details'] = father_nodes.xpath('./div[3]/div[2]/div/div[3]/div[2]/a/@href').extract()[0] # 房子详情（三级连接）
        item['house_album'] = father_nodes.xpath('./div[3]/div[1]/div[1]/a[1]/@href').extract()[0] # 房子相册（三级连接）
        item['pre_sale_permit'] = father_nodes.xpath('./div[3]/div[1]/div[1]/a[2]/span/text()').extract()[0] # 房子预售许可证（三级连接）
        
        yield item




# # -*- coding: utf-8 -*-
# import scrapy
# from ..items import MyspiderItem

# import copy

# class ItcastSpider(scrapy.Spider):
#     # 爬虫运行时的参数
#     name = 'itcast'

#     # 检查允许爬的域名
#     allowed_domains = ['https://sz.fang.ke.com']
#     # 1.修改设置起始的url
#     start_urls = ['https://sz.fang.ke.com/loupan']
#     
#     page = 2

#     # 数据提取的方法：接收下载中间件传过来的response，定义对于网站相关的操作
#     def parse(self, response):
#         print(response.url)
#         # 翻页
#         # 获取所有的教师节点
#         t_list = response.xpath('/html/body/div[6]/ul[2]/li')
#         # print(t_list)

#         item = MyspiderItem()
#         # 遍历教师节点列表
#         for teacher in t_list:
#             # xpath方法返回的是选择器对象列表     extract()方法可以提取到selector对象中data对应的数据。
#             item['next_url'] = teacher.xpath('./a/@href').extract()[0] # 下一层链接
#             item['title'] = teacher.xpath('./a/@title').extract()[0] # 房地名字
#             item['img_url'] = teacher.xpath('./a/img/@src').extract()[0] # 图片地址
#             item['tag'] = teacher.xpath('./div/div[1]/span[1]/text()').extract()[0] # 房子在售状态
#             item['tag_2'] = teacher.xpath('./div/div[1]/span[2]/text()').extract()[0] # 房子是否为住宅
#             item['location'] = teacher.xpath('/html/body/div[6]/ul[2]/li[1]/div/a[1]/text()[2]').extract()[0] # 所处地理位置
#             item['acreage'] = teacher.xpath('./div/a[2]/span[5]/text()').extract()[0] # 房子总面积
#             item['house_money'] = teacher.xpath('./div/div[4]/div[1]/span[1]/text()').extract()[0] # 平米价格

#             yield scrapy.Request(
#                     url = self.allowed_domains[0] + item["next_url"],
#                     callback=self.detail_parse,
#                     meta={"item": copy.deepcopy(item)},
#                     dont_filter=True
#                 )
#         if self.page < 100:
#             next_url = 'https://jn.zu.ke.com/zufang/pg{}/#contentList'.format(self.page)
#             self.page += 1
#             yield scrapy.Request(next_url, callback=self.parse)
