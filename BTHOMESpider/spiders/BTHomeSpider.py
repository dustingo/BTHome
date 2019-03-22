# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
import re
from ..items import BthomespiderItem
from scrapy import Request

class BthomespiderSpider(scrapy.Spider):
    name = 'BTHomeSpider'
    allowed_domains = ['www.btbtt06.com']
    start_urls = ['http://www.btbtt06.com/forum-index-fid-1.htm']
    item = BthomespiderItem()

    def parse(self, response):
        #帖子的链接正则
        regex = re.compile('http://www.btbtt06.com/thread-index-fid-1-tid-\d\d\d\d\d\.htm')
        content = response.body
        bsobj = BeautifulSoup(content,'html.parser')
        #帖子中电影详细信息
        movie_links = bsobj.find_all('a',attrs={'target':'_blank','class':'thread_icon','href':regex})
        #下一页链接正则
        next_url = bsobj.find_all('a',text="▶")
        links = []

        #取出符合规则的电影详细信息页面的url
        for i in movie_links:
            if i.attrs['href'].split('-')[5] != '12848.htm':
                #item['movie_link'] = i.attrs['href']
                links.append(i.attrs['href'])

        #将电影详细信息的url交给get_torrent函数处理
        for k in range(len(links)):
            yield Request(url=links[k],callback=self.get_torrent,dont_filter=True)

        #判断如果下一页存在，继续返回parer函数爬取信息
        if next_url[0].attrs['href']:
            yield Request(url=next_url[0].attrs['href'],callback=self.parse,dont_filter=True)

    def get_torrent(self,response):
        #电影信息页面里包含torrent链接的链接
        torrent_regex = re.compile('http:\/\/www.btbtt06.com\/attach\-dialog\-fid\-1\-aid\-\d+\-ajax\-1\.htm')
        content2 = response.body
        bsobj2 = BeautifulSoup(content2,'html.parser')
        #通过电影详细信息页面获取电影名字
        names = bsobj2.find_all('meta',attrs={'name':'keywords'})
        #获取包含torrent链接的信息
        torrent_urls = bsobj2.find_all('a',href=torrent_regex)

        for i in range(len(torrent_urls)):
            #从torrent_urls里获取url，将字段替换之后发现就是torrent的下载链接，不用再次解析链接获取
            url = torrent_urls[i].attrs['href'].replace('dialog','download')
            #放入item
            self.item['movie_link'] = url
            self.item['movie_name'] = names[0].attrs['content']
            yield self.item