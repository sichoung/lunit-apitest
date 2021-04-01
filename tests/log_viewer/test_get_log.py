#-*- coding: utf-8 -*-
import os, sys, io
import os.path
import requests
import pytest
from datetime import datetime
from common.exceptions import APITestException
from common.api_constants import LogViewerConstants as url_manager

test_email = url_manager.test_email
test_pw = url_manager.test_pw

# @pytest.fixture(scope='module')
# def upload_logfile(get_lv_baseurl, get_lv_token, get_dirpath):
#     time_stamp = datetime.now().strftime("%d%m%Y_%H%M%S")
#     headers = {"Authorization": "Bearer {}".format(get_lv_token(test_email, test_pw))}
#     payload = {
#         "host" : "10.120.0.11:91",
#         "containerId" : "qe_test",
#         "file" : ("daily{}.log".format(time_stamp), open(get_dirpath + "/log_viewer/test_resource/gw_logviewertest_dailylog.log", "rb")),
#     }

#     response = requests.post(get_lv_baseurl + url_manager.getloglist_api_path, files=payload, headers = headers, verify = False) # = get_dirpath+'/base64_lunit_cert.cer')
#     if response.status_code != 201:
#         raise APITestException("Failed to upload log file - status code is not 201 "+ response.status_code)
#     response_body = response.json()
#     return response_body.get('objectKey')

@pytest.fixture(scope='session')
def get_log_idlist(get_lv_baseurl, get_lv_token):
    search_pagesize = 3 # 가장 위에 3건만 조회
    headers = {"Authorization": "Bearer {}".format(get_lv_token(test_email, test_pw))}
    params = {
        'size': search_pagesize
        }
    response = requests.get(get_lv_baseurl + url_manager.getloglist_api_path, headers=headers, params=params, verify = False)
    if response.status_code != 200:
        raise APITestException("Failed to list search - "+response.status_code)
    response_body = response.json()
    contents_element = response_body.get("content")
    result_list = []
    for this_record in contents_element:
        result_list.append(this_record.get('id'))
    if len(result_list) >0 :
        return result_list
    else:
        raise APITestException("Not found any data")


def test_getlog_basic(get_lv_baseurl, get_lv_token, get_log_idlist):
    """ 테스트 목적 : 로그파일 업로드 & 조회 
    """
    headers = {"Authorization": "Bearer {}".format(get_lv_token(test_email, test_pw))}

    response = requests.get(get_lv_baseurl + url_manager.getloglist_api_path + "/"+ get_log_idlist[0], headers = headers, verify = False) # = get_dirpath+'/base64_lunit_cert.cer')
    # 'https://log-collector-server-dev.lunit.io/api/v1/logs602efa5c67bd0a718525ca85'
    assert 200 == response.status_code
    # '{"id":"602efa5c67bd0a718525ca85",
    # "transactionId":null,
    # "log":"[GW] [DEBUG] 2020-09-15 05:45:54,905 log:228 Internal Server Error: /cxr-v3/predictions/e373d0a5-8aee-4404-9367-f219de0e5d8b/contour.jpg",
    # "loggedAt":"2020-09-15T05:45:54.905",
    # "objectKey":"/tmp/tempLog/host_test_1.container_id_test_1.INFERENCE_SERVER.daily.log.2020-10-16-test.log",
    # "host":"host_test_1",
    # "component":"INFERENCE_SERVER",
    # "containerId":"container_id_test_1",
    # "logLevel":"DEBUG",
    # "logType":"APP",
    # "logStatus":null,
    # "updatedAt":"2021-02-18T23:38:04.384",
    # "createdAt":"2021-02-18T23:38:04.384"}'
    response_body = response.json()
    assert 'id' in response_body
    assert response_body.get('id') == get_log_idlist[0]
    assert 'transactionId' in response_body
    assert 'log' in response_body
    assert 'loggedAt' in response_body
    assert 'host' in response_body
    assert 'component' in response_body
    # assert 'containerId' in response_body
    assert 'logLevel' in response_body
    assert 'logType' in response_body
    assert 'logStatus' in response_body

def test_getlog_notexistid(get_lv_baseurl, get_lv_token):
    """ 테스트 목적 : 없는 로그 아이디
    """
    headers = {"Authorization": "Bearer {}".format(get_lv_token(test_email, test_pw))}

    response = requests.get(get_lv_baseurl + url_manager.getloglist_api_path + "/nononononono", headers = headers, verify = False) # = get_dirpath+'/base64_lunit_cert.cer')
    # 'https://log-collector-server-dev.lunit.io/api/v1/logs602efa5c67bd0a718525ca85'
    # assert 404 == response.status_code
    assert 400 == response.status_code
    response_body = response.json()
    assert response_body.get('code') == "400.0001.003"
    assert response_body.get('message') == "Not found log."


def test_getlog_tolongid(get_lv_baseurl, get_lv_token):
    """ 테스트 목적 : 너무 긴 값의 로그 아이디
    """
    headers = {"Authorization": "Bearer {}".format(get_lv_token(test_email, test_pw))}

    response = requests.get(get_lv_baseurl + url_manager.getloglist_api_path + "/nononononono_nononononono_nononononono_nononononono_nononononono", headers = headers, verify = False) # = get_dirpath+'/base64_lunit_cert.cer')
    # 'https://log-collector-server-dev.lunit.io/api/v1/logs602efa5c67bd0a718525ca85'
    # assert 404 == response.status_code
    assert 400 == response.status_code
    response_body = response.json()
    # '{"code":"400.0001.003","message":"Not found log."}'
    assert response_body.get('code') == "400.0001.003"
    assert response_body.get('message') == "Not found log."

    







