#-*- coding: utf-8 -*-
import os,sys
import pytest
import os, sys, io
import requests
import json, time
from datetime import datetime
from common import api_test_util as util
from common.api_constants import LogViewerConstants as APIInfo

test_id = "test"
test_pw = "test"

# [BE/IS/GW][2.5.0][Level][TimeStamp][TransactionID]   result_code : Success / Fail / Fail Retry

def test_uploadlog_basic(get_lv_baseurl,get_lv_token,get_dirpath):
    get_lv_token = get_lv_token(test_id, test_pw)
    time_stamp = datetime.now().strftime("%d%m%Y_%H%M%S")
    # headers = {"Content-Type": "multipart/form-data", "Authorization": "Bearer {}".format(get_lv_token)}
    headers = {"Authorization": "Bearer {}".format(get_lv_token)}
    payload = {
        "host" : "10.120.0.11:91",
        "containerId" : "qe_test",
        "file" : ("daily{}.log".format(time_stamp), open(get_dirpath + "/log_viewer/test_resource/gw_logviewertest_dailylog.log", "rb")),
    }
    response = requests.post(get_lv_baseurl + "/api/v1/logs", files=payload, headers=headers, verify=False) #data=payload, 
    print(response.text)
    assert 201 == response.status_code
    response_body = response.json()
    assert "objectKey" in response_body
    #'{"objectKey":"2021/02/05/GATEWAY/10.120.0.11:91.qe_test.GATEWAY.daily05022021_185522.log"}'

