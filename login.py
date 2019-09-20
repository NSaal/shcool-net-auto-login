# Login schoolnet automatically
# Author : Guo
# Contact : guoqr1997@163.com
import os
import subprocess
import time

import requests

url = 'http://202.204.48.66/'
pingdress = 'www.4399.com'  # The web to test net connection


def login():
    my_headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
        'Connection': 'keep-alive',
    }
    my_data = {
        'DDDDD': 'your id here',
        'upass': 'your password here',
        # 'v6ip': '', # Not necessary if you dont use ipv6
        '0MKKey': '123456789',
    }
    a = requests.post(url, data=my_data, headers=my_headers)

def main():
    state = subprocess.getstatusoutput('ping -w 500 -n 2 %s' % pingdress)
    if state[0]:
        login()
        print('login sucess')
    else:
        print('already login')
    os.system("pause")


if __name__ == '__main__':
    main()
