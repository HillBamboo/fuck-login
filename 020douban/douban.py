#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Required
- requests (必须)
- bs4 (必选)
- pillow (可选)
Info
- author : "shjunlee"
- email  : "shjunlee@foxmail.com"
- date   : "2017.8.30"

- HILLBAMBOO 重构于2018.4.9
'''

from urllib.request import urlretrieve
from os import remove
try:
    import cookielib
except:
    import http.cookiejar as cookielib

import requests
from bs4 import BeautifulSoup
try:
    from PIL import Image
except:
    pass


class DoubanLogin(object):

    def __init__(self):
        self.session = requests.session()
        self.session.cookies = cookielib.LWPCookieJar(filename='douban_cookies')
        self.headers = {
            'Host': 'www.douban.com',
            'Referer': 'https://www.douban.com/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:55.0) Gecko/20100101 Firefox/55.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate, br'
        }
        self.login_url = "https://www.douban.com/login"
        self.post_url = "https://accounts.douban.com/login"
        self.auth_url = "https://www.douban.com/accounts/"
        self.datas = {
            'source': 'index_nav',
            'remember': 'on'
        }
        # self.usr = usr
        # self.pwd = pwd

    def save_cookie(self):
        self.session.cookies.save()

    def load_cookie(self):
        try:
            self.session.cookies.load()
        except:
            print('cookie未能加载成功')

    def login(self):
        if self.is_login():
            print('登陆成功')
        else:
            usr = input('请输入用户名：\n>>> ')
            pwd = input('请输入密码：\n>>> ')
            self.datas['form_email'] = usr
            self.datas['form_password'] = pwd
            captcha, captcha_id = self.get_captcha()
            # 增加表数据
            self.datas['captcha-solution'] = captcha
            self.datas['captcha-id'] = captcha_id
            login_page = self.session.post(self.login_url, data=self.datas, headers=self.headers)
            page = login_page.text
            soup = BeautifulSoup(page, "html.parser")
            result = soup.findAll('div', attrs={'class': 'title'})

            # 进入豆瓣登陆后页面，打印热门内容
            for item in result:
                print(item.find('a').get_text())

            # 保存 cookies 到文件，下次可以使用 cookie 直接登录，不需要输入账号和密码
            self.save_cookie()

    def is_login(self):
        '''
        通过查看用户个人账户信息来判断是否已经登录
        '''
        self.load_cookie()
        login_code = self.session.get(self.auth_url, headers=self.headers,
                                 allow_redirects=False).status_code
        if login_code == 200:
            return True
        else:
            return False

    # TODO: 并不是每一次登录都需要输入验证码的，多次登录失败才需要输
    def get_captcha(self):
        '''
        获取验证码及其ID
        '''
        r = requests.post(self.post_url, data=self.datas, headers=self.headers)
        page = r.text
        soup = BeautifulSoup(page, "html.parser")
        # 利用bs4获得验证码图片地址
        img_src = soup.find('img', {'id': 'captcha_image'}).get('src')
        urlretrieve(img_src, 'captcha.jpg')
        try:
            im = Image.open('captcha.jpg')
            im.show()
            im.close()
        except:
            print('到本地目录打开captcha.jpg获取验证码')
        finally:
            captcha = input('please input the captcha:')
            remove('captcha.jpg')
        captcha_id = soup.find(
            'input', {'type': 'hidden', 'name': 'captcha-id'}).get('value')
        return captcha, captcha_id

if __name__ == '__main__':
    db = DoubanLogin()
    db.login()
