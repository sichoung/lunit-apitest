#-*- coding: utf-8 -*-
import os,sys
import pytest

import os, sys, io
import requests
import json, time
from common import api_test_util as util
from common.api_constants import LogViewerConstants as url_manager


test_email = "test@lunit.io"
test_pw = "test"

def test_getloglist_basic(get_lv_baseurl,get_lv_token):
    headers = {"Authorization": "Bearer {}".format(get_lv_token(test_email, test_pw))}
    params = {
        "components": test_id, # array[string]
        "keyword": test_id,
        "limit": test_id, # integer
        "logLevel": test_id, # array
        "logTypes": test_id, # array
        "page": test_id, # integer, Default value : 0
        "startDate": test_id, # 2021-02-05T07:09:07.304Z
        "endDate": test_pw
    }
    response = requests.get(get_lv_baseurl + url_manager.getloglist_api_path, headers=headers, verify=False)
    assert 200 == response.status_code
    response_body = response.json()


def test_getloglist_search(get_lv_baseurl,get_lv_token):
    headers = {"Authorization": "Bearer {}".format(get_lv_token(test_email, test_pw))}
    params = {
        "components": test_id, # array[string]
        "keyword": test_id,
        "limit": test_id, # integer
        "logLevel": test_id, # array
        "logTypes": test_id, # array
        "page": test_id, # integer, Default value : 0
        "startDate": test_id, # 2021-02-05T07:09:07.304Z
        "endDate": test_pw
    }
    response = requests.get(get_lv_baseurl + url_manager.getloglist_api_path, headers=headers, verify=False)
    assert 200 == response.status_code
    response_body = response.json()

