# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
class CarspiderItem(scrapy.Item):
    file=scrapy.Field() #文件名
    car=scrapy.Field() #车型
    score=scrapy.Field() #总评分
    u_id=scrapy.Field() #用户ID
    u_score=scrapy.Field() #用户评分
    u_merit=scrapy.Field() #用户评论优点
    u_demerit=scrapy.Field() #用户评论缺点
    u_summary=scrapy.Field() #用户评论综述
    u_flower=scrapy.Field() #用户评论鲜花数
    u_brick=scrapy.Field() #用户评论板砖数