# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import codecs

baseDir = '/home/t/dataset/carRemark/'
class CarspiderPipeline(object):
    def process_item(self, item, spider):
        print(item['file'])
        with codecs.open(baseDir+item['file']+'.json','a+',encoding='utf-8') as f:
            line=json.dumps(dict(item),ensure_ascii=False)+'\n'
            f.write(line)

        return item
