# -*- coding: utf-8 -*-
import re
import scrapy
from scrapy.spiders import Spider
from zufang.items import ZufangItem
from Util.bs4 import bs4_str


class AnjukexianzufangSpider(Spider):
    name = 'anjuke'
    # allowed_domains = ['bj.zu.anjuke.com']
    page = 1
    url = 'https://bj.zu.anjuke.com/fangyuan/p'
    start_urls = [url + str(page) + '/']

    def parse(self, response):
        regions = response.xpath('//div[@class="city-list"]/dl')
        for info in regions:
            for node in info.xpath("./dd/a"):
                item = ZufangItem()
                item['region'] = info.xpath("./dt/text()").extract()[0]
                item['city'] = node.xpath('./text()').extract()[0]
                city_url = node.xpath('./@href').extract()[0]
                yield scrapy.Request(city_url, meta={"meta_1": item}, callback=self.parse_city)

    def parse_city(self, response):
        item = response.meta['meta_1']
        detial_links = response.xpath("//div[@class='zu-itemmod']/@link").extract()
        for detial_link in detial_links:
            yield scrapy.Request(detial_link, callback=self.parse_item, meta={'meta_2': item})
        if self.page < 50:
            self.page += 1
            yield scrapy.Request(self.url + str(self.page) + '/', callback=self.parse)

    def parse_item(self, response):
        item = response.meta['meta_2']
        # 房子详情的链接
        item['home_url'] = response.url
        # 标题
        if response.xpath('//h3[@class="house-title"]/div/text()').extract():
            item['name'] = response.xpath('//h3[@class="house-title"]/div/text()').extract()[0]
        # 租房类型
        if response.xpath('//li[@class="title-label-item rent"]/text()').extract():
            item['rental_type'] = response.xpath('//li[@class="title-label-item rent"]/text()').extract()[0]
        # 交通
        if response.xpath('//li[@class="title-label-item subway"]/text()').extract():
            item['traffic'] = response.xpath('//li[@class="title-label-item subway"]/text()').extract()[0]
        # 室内图
        if response.xpath('//div[@id="room_pic_wrap"]//img/@src').extract():
            item['indoor_map'] = "|".join(response.xpath('//div[@id="room_pic_wrap"]//img/@src').extract())
        # 户型图
        if response.xpath('//div[@id="hx_pic_wrap"]//img/@src').extract():
            item['house_plan'] = "|".join(response.xpath('//div[@id="hx_pic_wrap"]//img/@src').extract())
        for k, v in self.house_info(response).items():
            item[k] = v
        # 设施
        if response.xpath('//ul[@class="house-info-peitao cf"]//div/text()').extract():
            item['facility'] = "|".join(response.xpath('//ul[@class="house-info-peitao cf"]//div/text()').extract())
        # 房源概况
        item['listing'] = self.listing(response)
        # 来源
        item['source'] = '安居客'
        yield item

    def listing(self, response):
        infos = response.xpath('//div[@class="auto-general"]/b/text()').extract()
        return " ".join(infos)

    def house_info(self, response):
        house_info = {}
        house_infos = response.xpath('//ul[@class="house-info-zufang cf"]')
        if house_infos:
            # 房费每月/元
            if house_infos.xpath('./li[1]/span[@class="price"]//b/text()').extract() and house_infos.xpath('./li[1]/span[@class="price"]/text()').extract():
                house_info['rent'] = "%s%s" % (
                    bs4_str(house_infos.xpath('./li[1]/span[@class="price"]//b/text()').extract()[0], response.body.decode("utf-8")),
                    house_infos.xpath('./li[1]/span[@class="price"]/text()').extract()[0])
            # 户型
            house_types = []
            for item in house_infos.xpath('./li[2]/span[@class="info"]//b/text()').extract():
                house_types.append(bs4_str(item, response.body.decode("utf-8")))
            if house_types:
                house_info['house_type'] = "%s室%s厅%s卫" % (house_types[0], house_types[1], house_types[2])
            else:
                house_info['house_type'] = ''

            # 面积
            if house_infos.xpath('./li[3]/span[@class="info"]//b/text()').extract():
                house_info['area'] = bs4_str(house_infos.xpath('./li[3]/span[@class="info"]//b/text()').extract()[0],
                                             response.body.decode("utf-8"))
            # 房子朝向
            if house_infos.xpath('./li[4]/span[@class="info"]/text()').extract():
                house_info['orientation'] = house_infos.xpath('./li[4]/span[@class="info"]/text()').extract()[0]
            # 楼层
            if house_infos.xpath('./li[5]/span[@class="info"]/text()').extract():
                house_info['floor'] = house_infos.xpath('./li[5]/span[@class="info"]/text()').extract()[0]
            # 装修情况
            if house_infos.xpath('./li[6]/span[@class="info"]/text()').extract():
                house_info['decoration'] = house_infos.xpath('./li[6]/span[@class="info"]/text()').extract()[0]
            # 房屋类型
            if house_infos.xpath('./li[7]/span[@class="info"]/text()').extract():
                house_info['property_type'] = house_infos.xpath('./li[7]/span[@class="info"]/text()').extract()[0]
            # 小区名
            if house_infos.xpath('./li[8]/a[1]/text()').extract():
                house_info['community_name'] = house_infos.xpath('./li[8]/a[1]/text()').extract()[0]
            # 要求
            if house_infos.xpath('./li[9]/span[@class="info"]/text()').extract():
                house_info['claim'] = house_infos.xpath('./li[9]/span[@class="info"]/text()').extract()[0]
        return house_info
