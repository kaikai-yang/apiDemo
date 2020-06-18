#!/usr/bin/python
# -*- coding:utf-8 -*-

# update : 2019-10-21
# description : call phone to alert user

import time
import sys,json,os
from qcloudsms_py import SmsMultiSender
from qcloudsms_py.httpclient import HTTPError

LOGGING_FILE = '/tmp/qcloudsms.log'

## tengxun
APP_ID = 
APP_KEY = 
TEMP_ID = 45176
PLAY_TIMES = 2

def send_sms(appid, appkey, template_id,  phone_numbers, sms_content):
    msender = SmsMultiSender(appid, appkey)
    params = [sms_content]
    try:
      result = msender.send_with_param(86, phone_numbers,
          template_id, params, extend="", ext="")
    except HTTPError as e:
      print(e)
    except Exception as e:
      print(e)
    print(result)

if __name__ == "__main__":
    phone_list = [
        "123123123", # 管理员
    ]
    sms_content = "故障数>100"
    send_sms(APP_ID, APP_KEY, TEMP_ID, phone_list, sms_content)
