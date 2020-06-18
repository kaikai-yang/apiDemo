#!/usr/bin/env python
# -*- coding:utf-8 -*-

# update : 2017-5-11
# description : update sdzx bandwith by api

import urllib2
import json
import argparse
import os
import time
import datetime
import requests

TOKEN_FILE = "/usr/local/api/token.txt"
UPDATE_TOKEN_MINITE = 5
SDZX_USER = ""
SDZX_PASSWD = ""


def get_token(filename):
    f_token = open(filename, 'r')
    # just a line
    data_token = f_token.read().strip()
    f_token.close()
    return data_token


def update_file_token(filename, token):
    f_token = open(filename, 'w')
    # read
    f_token.seek(0)
    f_token.truncate()
    f_token.write(token)
    f_token.close()
    return True


def is_five_minites(filename, minutes):
    mtime = os.path.getmtime(filename)
    modify_time = datetime.datetime.fromtimestamp(mtime)
    now_time = datetime.datetime.strptime(
        str(datetime.datetime.now()), '%Y-%m-%d %H:%M:%S.%f')
    return now_time - modify_time < datetime.timedelta(minutes=minutes)


def send_warning(S=0):
    if S == 0:
        pass
    else:
        global WARNINGSTATUS
        WARNINGSTATUS = 1
    return WARNINGSTATUS


def get_tokenid():
    def wrapped_tokenid(retry_run_count):
        try:
            if is_five_minites(TOKEN_FILE, UPDATE_TOKEN_MINITE):
                token = get_token(TOKEN_FILE)
                print 'get token from file and token = ' + token
                return token

            else:
                url = "http://api2.capitalonline.net/gic/v1/get_token/"
                print url
                send_headers = {
                    "username": SDZX_USER,
                    "password": SDZX_PASSWD,
                }
                req = urllib2.Request(url, headers=send_headers)
                response = urllib2.urlopen(req)
                tokeninfo = response.read()
                tokenid = json.loads(tokeninfo).get('Access-Token')
                if tokenid == None:
                    raise Exception("Access-Token is None")
                print tokenid
                update_file_token(TOKEN_FILE, tokenid)
                return tokenid
        except (Exception) as e:
            if retry_run_count < 5:
                status = "get_tokenid ERROR%s" % (retry_run_count)
                # time.sleep(10)
                retry_run_count += 1
                wrapped_tokenid(retry_run_count)
            else:
                raise Exception(e)
    retry_run_count = 0
    return wrapped_tokenid(retry_run_count)


def get_last_bandwidth(query_type, query_url):
    def wrapped_last_value(retry_run_count):
        tokenid = get_tokenid()
        try:
            send_headers = {
                "token": tokenid,
                "Content-Type": "application/json"
            }
            req = urllib2.Request(query_url, headers=send_headers)
            response = urllib2.urlopen(req)
            list = json.loads(response.read()).get('data')[0]['net']
            for i in xrange(len(list)):
                if query_type == "gpn":
                    if list[i]['type'] == 'gic':
                        last_value = list[i]['qos']
                        break
                else:
                    if list[i]['type'] == 'public':
                        last_value = list[i]['qos']
                        break
            if last_value == None:
                raise Exception("last_value is None")
            else:
                return last_value
        except (Exception) as e:
            if retry_run_count < 5:
                status = "get_last_value ERROR%s" % (retry_run_count)
                # time.sleep(10)
                retry_run_count += 1
                wrapped_last_value(retry_run_count)
            else:
                raise Exception(e)
    retry_run_count = 0
    return wrapped_last_value(retry_run_count)

