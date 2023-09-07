import scrapy
from ..items import MyspiderItem

class ItcastSpider(scrapy.Spider):
    name = 'itcast'
    s_url = 'https://sz.fang.ke.com' # 开始url

    def start_requests(self): # 翻页爬取
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

            url = self.s_url
            url += item['next_url']

            item['title'] = teacher.xpath('./a/@title').extract()[0] # 房地名字
            item['img_url'] = teacher.xpath('./a/img/@src').extract()[0] # 图片地址
            item['tag'] = teacher.xpath('./div/div[1]/span[1]/text()').extract()[0] # 房子在售状态
            item['tag_2'] = teacher.xpath('./div/div[1]/span[2]/text()').extract()[0] # 房子类型（住宅等、商业等、写字楼）
            item['location'] = teacher.xpath('/html/body/div[6]/ul[2]/li[1]/div/a[1]/text()[2]').extract()[0] # 所处地理位置

            # item['acreage'] = teacher.xpath('./div/a[2]/span[5]/text()').extract()[0] # 房子总面积
            item['house_money'] = teacher.xpath('./div/div[4]/div[1]/span[1]/text()').extract()[0] # 房子价格（每平方米）
            
            yield scrapy.Request(
                url,
                callback=self.parse_detail,
                meta={"item": item}
            )


    def parse_detail(self, response): # 二级连接
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
        

        url = self.s_url
        url += item['house_album']

        yield scrapy.Request(
            url,
            callback=self.parse_detail_next,
            meta={"item": item}
        )


    
    def parse_detail_next(self, response): # 三级连接
        item = response.meta["item"]

        father_nodes = response.xpath('/html/body/div[2]/div[1]/div') # 所有图片的父级
        
        div_count = len(response.xpath('/html/body/div[2]/div[1]/div/div')) # 获取div节点数量
       
        for i in range(1, div_count+1):
            house_img_nodes = father_nodes.xpath('./div[{i}]/ul'.format(i)) # 图片的父级
            house_img_nodes.xpath()


        # item['house_album'] = father_nodes.xpath('./div[1]/ul') # 所有效果的父级
        # item['house_album'] = father_nodes.xpath('./div[2]/ul') # 所有样板间的父级
        # item['house_album'] = father_nodes.xpath('./div[3]/ul') # 所有区位图的父级
        # item['house_album'] = father_nodes.xpath('./div[4]/ul') # 所有项目现场的父级
        # item['house_album'] = father_nodes.xpath('./div[5]/ul') # 所有预售许可证的父级
        # item['house_album'] = father_nodes.xpath('./div[6]/ul') # 所有开发商营业执照的父级