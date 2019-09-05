# -*- coding: utf-8 -*-
import re
import scrapy
from scrapy.spiders import Spider
from zufang.items import DouBanItem
from Util.bs4 import bs4_str
from urllib import parse
import json


class DouBanSpider(Spider):
    name = 'douban'
    # allowed_domains = ['bj.zu.anjuke.com']
    page = 0
    title = "热门"
    url_title = parse.quote(title)
    url = 'https://movie.douban.com/j/search_subjects?type=movie&tag='
    url_1 = '&sort=rank&page_limit=20&page_start='
    start_urls = [
        'https://movie.douban.com/explore#!type=movie&tag=%E7%83%AD%E9%97%A8&sort=recommend&page_limit=20&page_start=0']
    formdata = {'ck': '',
                'name': '18829042139',
                'password': 'aywan0327',
                'remember': 'false',
                'ticket': ''
                }  # 'redir': 'https://movie.douban.com/explore#!type=movie&tag=%E7%83%AD%E9%97%A8&sort=recommend&page_limit=20&page_start=0'}

    def start_requests(self):
        return [scrapy.Request(url='https://accounts.douban.com/passport/login',
                               meta={'cookiejar': 1}, callback=self.parse_login)]

    def parse_login(self, response):
        captcha = response.xpath("//img[@id='captcha_image']/@src").extract()
        print(captcha)
        cookie = response.meta['cookiejar']
        yield scrapy.FormRequest(method='POST', url="https://accounts.douban.com/j/mobile/login/basic",
                                 meta={'cookiejar': cookie}, formdata=self.formdata,
                                 callback=self.parse_success)

    def parse_success(self, response):
        yield scrapy.Request(url='https://movie.douban.com/subject/27010768/?tag=%E7%83%AD%E9%97%A8&amp;amp;amp;from=gaia',
                             meta={'cookiejar': response.meta['cookiejar']},
                             callback=self.parse)

    def parse(self, response):
        cookie = response.meta['cookiejar']
        title_links = '热门  最新  经典  可播放  豆瓣高分  冷门佳片  华语  欧美  韩国  日本  动作 喜剧  爱情  科幻  悬疑  恐怖  治愈'.split()
        for title in title_links:
            self.page = 0
            self.url_title = parse.quote(title)
            self.start_urls = self.url + self.url_title + self.url_1 + str(self.page)
            yield scrapy.Request(url=self.start_urls, callback=self.parse_page,
                                 meta={'url_title': self.url_title, 'title': title,
                                       'cookiejar': cookie})

    def parse_page(self, response):
        if self.page <= 300:
            self.url_title = response.meta['url_title']
            title = response.meta['title']
            self.start_urls = self.url + self.url_title + self.url_1 + str(self.page)
            self.page += 20
            yield scrapy.Request(url=self.start_urls, callback=self.parse_item,
                                 meta={'title': title, 'cookiejar': response.meta['cookiejar']})

    def parse_item(self, response):
        title = response.meta['title']
        data_info = json.loads(response.body)
        for film_info in data_info['subjects']:
            url = film_info.get('url')
            if url:
                yield scrapy.Request(url, callback=self.parse_detail,
                                     meta={'title': title, 'cookiejar': response.meta['cookiejar']})

    def parse_detail(self, response):
        item = DouBanItem()
        item['title'] = response.meta['title']
        # 电影名
        if response.xpath("//div[@id='content']/h1/span[1]/text()").extract():
            item['film_name'] = response.xpath("//div[@id='content']/h1/span[1]/text()").extract()[0]
        # 上映年份年份
        if response.xpath("//div[@id='content']/h1/span[2]/text()").extract():
            item['time_year'] = re.search("(\d+)",
                                          response.xpath("//div[@id='content']/h1/span[2]/text()").extract()[0]).group(
                1)
        # 导演
        if response.xpath('//div[@id="info"]/span[1]/span[2]/a/text()').extract():
            item['director'] = response.xpath('//div[@id="info"]/span[1]/span[2]/a/text()').extract()[0]
        # 编剧
        if response.xpath('//div[@id="info"]/span[2]/span[2]/a/text()').extract():
            item['screenwriter'] = ",".join(response.xpath('//div[@id="info"]/span[2]/span[2]/a/text()').extract())
        # 演员
        if response.xpath('//div[@id="info"]/span[3]/span[2]//a/text()').extract():
            item['actors'] = ",".join(response.xpath('//div[@id="info"]/span[3]/span[2]//a/text()').extract())
        span_nodes = response.xpath('//div[@id="info"]/span')
        span_counts = len(span_nodes)
        type_start_count = 0
        type_end_count = 0
        time_start_count = 0
        time_end_count = 0
        for idx, span_node in enumerate(span_nodes):
            if "类型" in span_node.xpath('./text()').extract()[0]:
                type_start_count = idx + 1
            elif '制片国家/地区:' == span_node.xpath('./text()').extract()[0]:
                type_end_count = idx
            elif '上映日期:' == span_node.xpath('./text()').extract()[0]:
                time_start_count = idx + 1
            elif '片长:' == span_node.xpath('./text()').extract()[0]:
                time_end_count = idx
        # 电影类型
        film_types = []
        for node in span_nodes[type_start_count:type_end_count]:
            film_types.append(node.xpath('./text()').extract()[0])
        item['film_type'] = ",".join(film_types)
        info = ['', '', '']
        if response.xpath('//div[@id="info"]/text()').extract():
            info = [item for item in response.xpath('//div[@id="info"]/text()').extract() if
                    (item.strip() and not item.strip().startswith(r'/'))]
        if len(info) < 3:
            info.append('')
        # 拍摄国家
        item['shooting_country'] = info[0]
        # 电影语言
        item['film_language'] = info[1]
        # 上映时间
        release_times = []
        for node in span_nodes[time_start_count:time_end_count]:
            release_times.append(node.xpath('./text()').extract()[0])
        item['release_time'] = ",".join(release_times)
        # 时长
        if span_nodes[-3].xpath('./text()').extract():
            item['time_length'] = span_nodes[-3].xpath('./text()').extract()[0]
        # 别名
        item['another_name'] = info[2]
        # 电影链接
        if response.xpath('//div[@id="info"]/a/@href').extract():
            item['film_link'] = response.xpath('//div[@id="info"]/a/@href').extract()[0]

        # 评分
        if response.xpath('//div[@id="interest_sectl"]//strong/text()').extract():
            item['score'] = response.xpath('//div[@id="interest_sectl"]//strong/text()').extract()[0]
        # 评分人数
        if response.xpath('//div[@id="interest_sectl"]//div[@class="rating_sum"]/a/span/text()').extract():
            item['score_number'] = response.xpath(
                '//div[@id="interest_sectl"]//div[@class="rating_sum"]/a/span/text()').extract()[0]

        scores = response.xpath('//div[@id="interest_sectl"]//span[@class="rating_per"]/text()').extract()
        if scores:
            # 5星评分
            item['five_score_rate'] = scores[0]
            # 4星评分
            item['four_score_rate'] = scores[1]
            # 3星评分
            item['three_score_rate'] = scores[2]
            # 2星评分
            item['two_score_rate'] = scores[3]
            # 1星评分
            item['one_score_rate'] = scores[4]

        # 电影简介
        if response.xpath('//div[@class="related-info"]//div[@class="indent"]/span/text()').extract():
            item['film_bref'] = ''.join([item.strip() for item in response.xpath(
                '//div[@class="related-info"]//div[@class="indent"]/span/text()').extract()])

        # 电影封面
        if response.xpath('//div[@id="mainpic"]/a/img/@src').extract():
            item['film_img'] = response.xpath('//div[@id="mainpic"]/a/img/@src').extract()[0]
        item['source'] = '豆瓣'
        yield item
