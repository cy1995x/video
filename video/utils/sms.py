import hashlib
from datetime import datetime

import requests
import base64
import json

"""
容联云
ACCOUNT SID：8aaf0708773733a8017741b5b3bb0489
(主账户ID)
AUTH TOKEN：f41f6f79d4424fc3b71fb89a566c809b  
(账户授权令牌)
Rest URL(生产)：https://app.cloopen.com:8883
AppID(默认)：8aaf0708773733a8017741b5b490048f
"""


class YunTongXun:
    base_url = "https://app.cloopen.com:8883"

    def __init__(self, account_sid, account_token, app_id, template_id):
        self.accountSid = account_sid
        self.accountToken = account_token
        self.appId = app_id
        self.templateId = template_id

    # 构造url
    def get_request_url(self, sig):
        self.url = YunTongXun.base_url + '/2013-12-26/Accounts/%s/SMS/TemplateSMS?sig=%s' % (self.accountSid, sig)
        return self.url

    # 生成时间戳
    @staticmethod
    def get_timestamp():
        now = datetime.now()
        now_str = now.strftime('%Y%m%d%H%M%S')
        return now_str

    # 计算sig
    def get_sig(self, timestamp):
        data = self.accountSid + self.accountToken + timestamp
        hash_value = hashlib.md5(data.encode()).hexdigest().upper()
        return hash_value

    # 构造请求头
    def get_request_header(self, timestamp):
        data = self.accountSid + ":" + timestamp
        data_bs = base64.b64encode(data.encode()).decode()
        return {
            'Accept': 'application/json',
            'Content-Type': 'application/json;charset=utf-8',
            'Authorization': data_bs
        }

    # 构造请求体
    def get_request_body(self, phone, code):
        return {
            'to': phone,
            'appId': self.appId,
            'templateId': self.templateId,
            'datas': [code, '3']
        }

    # 发送请求
    def do_request(self, url, header, body):
        res = requests.post(url=url, headers=header, data=json.dumps(body))
        return res.text

    # 封装以上所有步骤
    def run(self, phone, code):
        timestamp = self.get_timestamp()
        sig = self.get_sig(timestamp)
        url = self.get_request_url(sig)
        header = self.get_request_header(timestamp)
        body = self.get_request_body(phone, code)
        result = self.do_request(url, header, body)
        return result


if __name__ == '__main__':
    a_id = '8aaf0708773733a8017741b5b3bb0489'
    a_token = 'f41f6f79d4424fc3b71fb89a566c809b'
    t_id = '1'
    ap_id = '8aaf0708773733a8017741b5b490048f'
    obj = YunTongXun(a_id, a_token, ap_id, t_id)
    res = obj.run('15700156229', '123456')
    print(res)
