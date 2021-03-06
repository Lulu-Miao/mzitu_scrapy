# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy import Request
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
import re


class MzituScrapyPipeline(ImagesPipeline):

    def file_path(self, request, response=None, info=None):
        """
        :param request: 每一个图片下载管道请求
        :param response:
        :param info:
        :param strip :清洗Windows系统的文件夹非法字符，避免无法创建目录
        :return: 每套图的分类目录
        """
        item = request.meta['item']
        folder = item['name']
        folder_strip = strip(folder)
        # image_guid = request.url.split('/')[-1]
        splits = request.url.split('/')
        if re.match('^\d{2}.*', splits[-1]):
            image_guid = splits[-3] + '-' + splits[-2] + '-' + splits[-1][:2] + '-' + splits[-1][2:]
        else:
            image_guid = splits[-3] + '-' + splits[-2] + '-' + splits[-1]
        filename = u'full/{0}/{1}'.format(folder_strip, image_guid)
        # print("pipelines.file_path:" + filename)
        return filename

    def get_media_requests(self, item, info):
        for img_url in item['image_urls']:
            referer = item['url']
            # print("pipelines.get_media_requests: yield Request" + referer)
            yield Request(img_url, meta={'item': item,
                                         'referer': referer})


    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        return item

    # def process_item(self, item, spider):
    #     return item

def strip(path):
    """
    :param path: 需要清洗的文件夹名字
    :return: 清洗掉Windows系统非法文件夹名字的字符串
    """
    path = re.sub(r'[？\\*|“<>:/]', '', str(path))
    return path

