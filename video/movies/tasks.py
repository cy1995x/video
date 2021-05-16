"""
电影数据获取
"""

import random
import re
import time

import pymysql
import redis
import requests
from fake_useragent import UserAgent
from lxml import etree
from selenium import webdriver

from video.celery import app


class MovieSpider:
    def __init__(self):
        self.url = 'https://maoyan.com/'
        self.db = pymysql.connect(host='127.0.0.1', port=3306, user='root',
                                  password='123456', database='video', charset='utf8')
        self.cur = self.db.cursor()
        self.r = redis.Redis(host='localhost', port=6379)
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('--headless')
        self.driver = webdriver.Chrome(options=self.options)

    def get_incr_url(self):
        self.driver.get(self.url)
        self.driver.find_element_by_link_text('榜单').click()
        self.driver.find_element_by_link_text('TOP100榜').click()
        # 等待加载(无需切换句柄！)
        time.sleep(2)

    def get_page_data(self):
        dd_list = self.driver.find_elements_by_xpath('//*[@id="app"]/div/div/div/dl/dd')
        for dd in dd_list:
            rank, title, actor, release_time, score = dd.text.split('\n')
            actor = actor.split('：')[1].replace(',', '/')
            release_time = release_time.split('：')[1].split('(')[0]
            if len(release_time) == 4:
                release_time += '-01-01'
            if len(release_time) == 7:
                release_time += '-01'
            res = [rank, title, actor, release_time, score]
            print(res)
            # 持久化储存
            self.save_data_by_mysql(res)

    def save_data_by_mysql(self, data):
        sql = 'insert into top100_movies values (%s,%s,%s,%s,%s,7)'
        self.cur.execute(sql, data)

    def close_mysql(self):
        self.cur.close()
        self.db.close()

    def get_all_data(self):
        self.get_incr_url()
        while True:
            self.get_page_data()
            self.db.commit()
            try:
                self.driver.find_element_by_link_text('下一页').click()
                time.sleep(random.randint(1, 2))
            except Exception as e:
                print('爬取完成！', e)
                self.close_mysql()
                self.driver.quit()
                break


# if __name__ == '__main__':
#     spider = MovieSpider()
#     spider.get_all_data()


class PosterSpider:
    def __init__(self):
        self.url = 'https://maoyan.com/'
        self.db = pymysql.connect(host='127.0.0.1', port=3306, user='root',
                                  password='123456', database='video', charset='utf8')
        self.cur = self.db.cursor()
        # self.r = redis.Redis(host='localhost', port=6379)
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('--headless')
        self.driver = webdriver.Chrome(options=self.options)

    def get_incr_url(self):
        self.driver.get(self.url)
        self.driver.find_element_by_link_text('榜单').click()
        self.driver.find_element_by_link_text('TOP100榜').click()
        # 等待加载(无需切换句柄！)
        time.sleep(2)

    def get_page_data(self):
        dd_list = self.driver.find_elements_by_xpath('//*[@id="app"]/div/div/div[1]/dl/dd')
        for i in range(500, 2000, 200):
            self.driver.execute_script(f'var q=document.documentElement.scrollTop={i}')
            time.sleep(1)
        for dd in dd_list:
            img = dd.find_element_by_xpath('./a/img[2]')
            poster = img.get_attribute('src')
            title = img.get_attribute('alt')
            print((title, poster))
            # 持久化存储
            resp = self.get_picture_data(poster)
            self.save_by_file((title, resp))
            self.save_by_mysql(title)

    def save_by_mysql(self, title):
        sql = 'update top100_movies set poster = %s where title = %s'
        self.cur.execute(sql, ['posters/' + title + '.jpg', title])

    def get_picture_data(self, poster):
        resp = requests.get(url=poster, headers={'User-Agent': UserAgent().random}).content
        return resp

    def save_by_file(self, data):
        with open('../media/posters/' + data[0] + '.jpg', 'wb') as f:
            f.write(data[1])

    def close_mysql(self):
        self.cur.close()
        self.db.close()

    def get_all_data(self):
        self.get_incr_url()
        while True:
            self.get_page_data()
            self.db.commit()
            try:
                self.driver.find_element_by_link_text('下一页').click()
                time.sleep(random.randint(1, 2))
            except Exception as e:
                print('爬取完成！', e)
                self.close_mysql()
                self.driver.quit()
                break


# if __name__ == '__main__':
#     spider = PosterSpider()
#     spider.get_all_data()

class MovieDetailSpider:
    def __init__(self):
        self.url = 'https://maoyan.com/'
        self.db = pymysql.connect(host='127.0.0.1', port=3306, user='root',
                                  password='123456', database='video', charset='utf8')
        self.cur = self.db.cursor()
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('--headless')
        self.driver = webdriver.Chrome()

    def get_incr_url(self):
        self.driver.get(self.url)
        self.driver.find_element_by_link_text('榜单').click()
        self.driver.find_element_by_link_text('TOP100榜').click()
        # 等待加载(无需切换句柄！)
        time.sleep(2)

    def get_page_data(self):
        dd_list = self.driver.find_elements_by_xpath('//*[@id="app"]/div/div/div[1]/dl/dd')
        for dd in dd_list:
            detail_url = dd.find_element_by_xpath('./a').get_attribute('href')
            html = self.get_html(detail_url)
            time.sleep(2)
            res = self.parser_data_by_xpath(html)
            # 持久化储存
            self.save_by_mysql(res)

    def save_by_mysql(self, res):
        sql = 'insert into movies_detail (release_area,film_length,`desc`,movie_id) values (%s,%s,%s,%s)'
        self.cur.execute(sql, res)

    def get_html(self, url):
        headers = {'User-Agent': UserAgent().random}
        html = requests.get(url=url, headers=headers).text
        return html

    def parser_data_by_xpath(self, html):
        e_obj = etree.HTML(html)
        title = e_obj.xpath('/html/body/div[3]/div/div[2]/div[1]/h1/text()')[0]
        movie_id = self.get_movie_id(title)
        a_list = e_obj.xpath('.//div[@class="movie-brief-container"]/ul/li[1]/a')
        classification = []
        for a in a_list:
            text = a.xpath('./text()')[0].strip()
            classification.append(text)
        area_length_list = e_obj.xpath('.//div[@class="movie-brief-container"]/ul/li[2]/text()')
        area_length = area_length_list[0] if area_length_list else ''
        desc_list = e_obj.xpath('//*[@id="app"]/div/div[1]/div/div[3]/div[1]/div[1]/div[2]/span/text()')
        desc = desc_list[0] if desc_list else None
        area_length = re.sub(r'\s', '', area_length).split('/')
        res = [area_length[0], area_length[1], desc, movie_id]
        print(res)
        return res

    def get_movie_id(self, title):
        sql = 'select `rank` from movies where title = %s'
        self.cur.execute(sql, title)
        movie_id = self.cur.fetchone()[0]
        return movie_id

    def close_mysql(self):
        self.cur.close()
        self.db.close()

    def get_all_data(self):
        self.get_incr_url()
        while True:
            self.get_page_data()
            self.db.commit()
            try:
                self.driver.find_element_by_link_text('下一页').click()
                time.sleep(random.randint(1, 2))
            except Exception as e:
                print('爬取完成！', e)
                self.close_mysql()
                self.driver.quit()
                break


# if __name__ == '__main__':
#     MovieDetailSpider().get_all_data()

class MovieClassificationSpider:
    def __init__(self):
        self.url = 'https://maoyan.com/'
        self.db = pymysql.connect(host='127.0.0.1', port=3306, user='root',
                                  password='123456', database='video', charset='utf8')
        self.cur = self.db.cursor()
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('--headless')
        self.driver = webdriver.Chrome()

    def get_incr_url(self):
        self.driver.get(self.url)
        self.driver.find_element_by_link_text('榜单').click()
        self.driver.find_element_by_link_text('TOP100榜').click()

        # 等待加载(无需切换句柄！)
        time.sleep(2)

    def get_page_data(self):
        dd_list = self.driver.find_elements_by_xpath('//*[@id="app"]/div/div/div[1]/dl/dd')
        for dd in dd_list:
            detail_url = dd.find_element_by_xpath('./a').get_attribute('href')
            html = self.get_html(detail_url)
            time.sleep(2)
            res = self.parser_data_by_xpath(html)
            # 持久化储存
            # self.save_by_mysql(res)

    def save_by_mysql(self, res):
        sql = 'insert into movies_detail (release_area,film_length,`desc`,movie_id) values (%s,%s,%s,%s)'
        self.cur.execute(sql, res)

    def get_html(self, url):
        headers = {'User-Agent': UserAgent().random}
        html = requests.get(url=url, headers=headers).text
        return html

    def parser_data_by_xpath(self, html):
        e_obj = etree.HTML(html)
        title = e_obj.xpath('/html/body/div[3]/div/div[2]/div[1]/h1/text()')[0]
        movie_id = self.get_movie_id(title)
        a_list = e_obj.xpath('.//div[@class="movie-brief-container"]/ul/li[1]/a')
        classification = []
        for a in a_list:
            text = a.xpath('./text()')[0].strip()
            classification.append(text)
        res = [movie_id, title, classification]
        print(res)
        return res

    def get_movie_id(self, title):
        sql = 'select `rank` from movies where title = %s'
        self.cur.execute(sql, title)
        a = self.cur.fetchone()
        if not a:
            return None
        else:
            movie_id = a[0]
            return movie_id

    def close_mysql(self):
        self.cur.close()
        self.db.close()

    def get_all_data(self):
        self.get_incr_url()
        while True:
            self.get_page_data()
            # self.db.commit()
            try:
                self.driver.find_element_by_link_text('下一页').click()
                time.sleep(random.randint(1, 2))
            except Exception as e:
                print('爬取完成！', e)
                # self.close_mysql()
                self.driver.quit()
                break


if __name__ == '__main__':
    MovieClassificationSpider().get_all_data()
