# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ZufangItem(scrapy.Item):
    # define the fields for your item here like:
    # 房子详情的链接
    home_url = scrapy.Field()
    # 标题
    name = scrapy.Field()
    # 租房类型
    rental_type = scrapy.Field()
    # 交通
    traffic = scrapy.Field()
    # 室内图
    indoor_map = scrapy.Field()
    # 户型图
    house_plan = scrapy.Field()
    # 房费每月/元
    rent = scrapy.Field()
    # 户型
    house_type = scrapy.Field()
    # 面积
    area = scrapy.Field()
    # 房子朝向
    orientation = scrapy.Field()
    # 楼层
    floor = scrapy.Field()
    # 装修情况
    decoration = scrapy.Field()
    # 房屋类型
    property_type = scrapy.Field()
    # 小区名
    community_name = scrapy.Field()
    # 要求
    claim = scrapy.Field()
    # 设施
    facility = scrapy.Field()
    # 房源概况
    listing = scrapy.Field()
    # 来源
    source = scrapy.Field()
    # 地区
    city = scrapy.Field()
    # 区域
    region = scrapy.Field()


class DouBanItem(scrapy.Item):
    title = scrapy.Field()
    # 电影名
    film_name = scrapy.Field()
    # 上映年份年份
    time_year = scrapy.Field()
    # 导演
    director = scrapy.Field()
    # 编剧
    screenwriter = scrapy.Field()
    # 演员
    actors = scrapy.Field()
    # 电影类型
    film_type = scrapy.Field()
    # 拍摄国家
    shooting_country = scrapy.Field()
    # 电影语言
    film_language = scrapy.Field()
    # 上映时间
    release_time = scrapy.Field()
    # 时长
    time_length = scrapy.Field()
    # 别名
    another_name = scrapy.Field()

    # 电影链接
    film_link = scrapy.Field()

    #来源
    source = scrapy.Field()

    # 评分
    score = scrapy.Field()
    # 评分人数
    score_number = scrapy.Field()
    # 5星评分
    five_score_rate = scrapy.Field()
    # 4星评分
    four_score_rate = scrapy.Field()
    # 3星评分
    three_score_rate = scrapy.Field()
    # 2星评分
    two_score_rate = scrapy.Field()
    # 1星评分
    one_score_rate = scrapy.Field()

    # 电影简介
    film_bref = scrapy.Field()

    # 电影封面
    film_img = scrapy.Field()
