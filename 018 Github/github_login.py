#!/usr/bin/env python
# encoding: utf-8

"""
__author__: wuxiaoshen
__software__: PyCharm
__project__:scrapyone
__file__: github_login
__time__: 2017/4/16 23:20
"""
import requests
from bs4 import BeautifulSoup
try:
    import cookielib
except:
    import http.cookiejar as cookielib


class GithubLogin(object):

    def __init__(self):
        self.headers = {
            'Referer': 'https://github.com/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
            'Host': 'github.com',
            'Upgrade-Insecure-Requests': '1'
        }
        self.login_url ='https://github.com/login'
        self.post_url = 'https://github.com/session'
        self.logined_url = 'https://github.com/settings/profile'

        self.session = requests.session()
        self.session.cookies = cookielib.LWPCookieJar(filename='github_cookie')

    def load_cookie(self):
        try:
            self.session.cookies.load(ignore_discard=True)
            return True
        except:
            print('cookie 载入不成功')
            return False

    def get_token(self):
        response = self.session.get(self.login_url, headers=self.headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'lxml')
            result = soup.select('#login > form > input[name="authenticity_token"]')
            return result[0].get('value')
        else:
            print('failed')

    def login(self):
        if self.is_login():
            print('登录成功！')
        else:
            email = input('请输入邮箱地址：\n>>> ')
            pwd = input('请输入密码：\n>>> ')

            post_data = {
                'commit': 'Sign in',
                'utf8': '✓',
                'authenticity_token': self.get_token(),
                'login': email,
                'password': pwd
            }
            response = self.session.post(self.post_url, data=post_data, headers=self.headers)

            if response.status_code == 200:
                print('登录成功')

            self.session.cookies.save()

    def is_login(self):
        if not self.load_cookie():
            return False
        else:
            response = self.session.get(self.logined_url, headers=self.headers, allow_redirects=False)
            if response.status_code == 200:
                # soup = BeautifulSoup(response.text, 'lxml')
                # result = soup.select('#profile_10396980 > div')
                # print(result[0].text)
                return True
            else:
                return False


if __name__ == "__main__":
    Github = GithubLogin()
    Github.login()
