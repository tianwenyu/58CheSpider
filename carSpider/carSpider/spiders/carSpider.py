import scrapy
from carSpider.items import CarspiderItem

baseDir = '/home/t/dataset/carRemark/'
startUrl = 'http://www.58che.com/brand.html'


class CarSpider(scrapy.Spider):
    name = 'spider'  # 爬虫名

    def __init__(self):
        self.start_urls = [startUrl]

        # 第一层解析方法

    def parse(self, response):
        # 定位到车型元素
        subclasses = response.css('body > div.fltop > div.marcenter > div > div > div.r > ul > li > dl > dt > a')
        for subclass in subclasses:
            subclass_name = subclass.xpath('text()').extract_first()  # 获取车型名称文本
            subclass_link = subclass.xpath('@href').extract_first()  # 获取车型链接
            yield scrapy.Request(url=subclass_link, callback=self.parse_car_subclass,
                                 meta={'file': subclass_name})  # 回调下一层解析方法，并把车型名称传递给该方法作为文件名

            # 第二层解析方法

    def parse_car_subclass(self, response):
        infos = response.css('#line1 > div.cars_line2.l > div.dianpings > div.d_div1.clearfix > font')  # 定位到总评分元素
        for info in infos:
            score = info.xpath('text()').extract_first()  # 获取总评分元素文本
            file = response.meta['file']  # 获取上个Request传递来的meta['file']
            self.writeScore(file, score)  # 将总评分写入文件中
            link = response.url + 'list_s1_p1.html'  # 拼接用户评论第一页链接
            yield scrapy.Request(url=link, callback=self.parse_remark,
                                 meta={'file': file})  # 回调下一层解析方法，把车型名称传递给该方法作为文件名

            # 第三层解析方法

    def parse_remark(self, response):
        # 定位到用户评论元素
        infos = response.css(
            'body > div.newbox > div > div.xgo_cars_w760.l > div.xgo_dianping_infos.mb10 > div.xgo_cars_dianping > div > dl')
        for info in infos:
            uid = info.xpath('dd[1]/strong/a/text()')[0].extract()  # 获取用户ID
            score = info.xpath('dd[1]/div/div/@style')[0].extract()  # 获取用户评分星级
            score = self.getScore(score)  # 将用户评分星级转化为5分制评分

            try:
                # 先获取是否有‘优点’元素，若有则定位‘优点’元素的下一个兄弟节点，即‘优点评语’，若无则为空
                node = info.xpath('dd[2]/div/div[contains(@class,"l redc00")]')[0]
                if node is not None:
                    merit = node.xpath('following-sibling::*[1]/text()')[0].extract()
                else:
                    merit = ''
            except:
                merit = ''

            try:
                # 先获取是否有‘缺点’元素，若有则定位‘缺点’元素的下一个兄弟节点，即‘缺点评语’，若无则为空
                node = info.xpath('dd[2]/div/div[contains(@class,"l hei666")]')[0]
                if node is not None:
                    demerit = node.xpath('following-sibling::*[1]/text()')[0].extract()
                else:
                    demerit = ''
            except:
                demerit = ''

            try:
                # 先获取是否有‘综述’元素，若有则定位‘综述’元素的下一个兄弟节点，即‘综述评语’，若无则为空
                node = info.xpath('dd[2]/div/div[contains(@class,"l")]')[0]
                if node is not None:
                    summary = node.xpath('following-sibling::*[1]/text()')[0].extract()
                else:
                    summary = ''
            except:
                summary = ''

            flower = info.xpath('dd[2]/div[contains(@class,"apply")]/a[3]/span/text()')[0].extract()  # 获取鲜花数
            brick = info.xpath('dd[2]/div[contains(@class,"apply")]/a[4]/span/text()')[0].extract()  # 获取板砖数

            # 创建Item
            item = CarspiderItem()
            item['file'] = response.meta['file']
            item['u_id'] = uid
            item['u_score'] = score
            item['u_merit'] = merit
            item['u_demerit'] = demerit
            item['u_summary'] = summary
            item['u_flower'] = flower
            item['u_brick'] = brick

            # 生成Item
            yield item

        # 获取`下一页`元素，若有则回调`parse_remark`第三层解析方法，即继续获取下一页用户评论数据
        # 定位`下一页`元素
        next_pages = response.css(
            'body > div.newbox > div > div.xgo_cars_w760.l > div.xgo_dianping_infos.mb10 > div.xgo_cars_dianping > div > div > a.next')
        for next_page in next_pages:
            # 若有`下一页`元素，则拼接`下一页`元素链接，并回调第三层解析方法，用来获取下一页用户评论数据
            if next_page is not None:
                next_page_link = next_page.xpath('@href')[0].extract()
                next_page_link = 'http://www.58che.com' + next_page_link
                file = response.meta['file']
                yield scrapy.Request(url=next_page_link, callback=self.parse_remark, meta={'file': file})


                # 将总评分写入文件

    def writeScore(self, file, score):
        with open('/home/t/dataset/carRemark/' + file + '.json', 'a+') as f:
            f.write(score + '\n')

    # 将用户评分星级转为5分制分数，类似switch功能
    def getScore(self, text):
        text = text.split(':')[1]  # 分割文本，原文本格式形如`width:100%`，分割并截取`:`后的文本
        return {
            '100%': 5,
            '80%': 4,
            '60%': 3,
            '40%': 2,
            '20%': 1,
            '0%': 0
        }.get(text)