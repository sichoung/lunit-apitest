#-*- coding: utf-8 -*-
import os, sys, io
import os.path
import requests
import pytest
import json
from datetime import datetime
from common.exceptions import APITestException
from common.api_constants import LogViewerConstants as url_manager

test_email = url_manager.test_email
test_pw = url_manager.test_pw

@pytest.fixture(scope='session')
def get_logfile_idlist(get_lv_baseurl, get_lv_token):
    search_pagesize = 3
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
    return result_list


def test_logdownload_basic(get_lv_baseurl, get_lv_token, get_logfile_idlist):
    """ 테스트 목적 : 최근 3건의 id 조회 후 다운로드 기본 테스트
    """
    headers = {"Content-Type": "application/json", "Authorization": "Bearer {}".format(get_lv_token(test_email, test_pw))}
    payload = {
        "ids": get_logfile_idlist
    }
    response = requests.post(get_lv_baseurl + url_manager.logdownload_api_path, headers=headers, data=json.dumps(payload,indent=4), verify = False)
    assert response.status_code == 200
    assert '' != response.text
    # csv 형태의 컨텐츠 반환 
    # '"id","transactionId","log","loggedAt","objectKey","host","component","containerId","logLevel","logType","logStatus","updatedAt","createdAt"\n
    # "602efa5c67bd0a718525ca85","","[GW] [DEBUG] 2020-09-15 05:45:54,905 log:228 Internal Server Error: /cxr-v3/predictions/e373d0a5-8aee-4404-9367-f219de0e5d8b/contour.jpg","2020-09-15T05:45:54.905","/tmp/tempLog/host_test_1.container_id_test_1.INFERENCE_SERVER.daily.log.2020-10-16-test.log","host_test_1","INFERENCE_SERVER","container_id_test_1","DEBUG","APP","","2021-02-18T23:38:04.384","2021-02-18T23:38:04.384"\n"602efa5c67bd0a718525ca86","","[BE] [DEBUG] 2020-09-15 05:45:54,905 log:228 Internal Server Error: /cxr-v3/predictions/e373d0a5-8aee-4404-9367-f219de0e5d8b/contour.jpg","2020-09-15T05:45:54.905","/tmp/tempLog/host_test_1.container_id_test_1.INFERENCE_SERVER.daily.log.2020-10-16-test.log","host_test_1","INFERENCE_SERVER","container_id_test_1","DEBUG","APP","","2021-02-18T23:38:04.384","2021-02-18T23:38:04.384"\n"602efa5c67bd0a718525ca87","","[BE] [FATAL] 2020-09-15 05:45:54,905 log:228 Internal Server Error: /cxr-v3/predictions/e373d0a5-8aee-4404-9367-f219de0e5d8b/contour.jpg","2020-09-15T05:45:54.905","/tmp/tempLog/host_test_1.container_id_test_1.INFERENCE_SERVER.daily.log.2020-10-16-test.log","host_test_1","INFERENCE_SERVER","container_id_test_1","FATAL","APP","","2021-02-18T23:38:04.384","2021-02-18T23:38:04.384"\n'

def test_logdownload_notexistlogid(get_lv_baseurl, get_lv_token):
    """ 테스트 목적 : 유효하지 않은 3건의 id 값에 대해 다운로드 테스트 - 200ok, 컬럼 헤더값만 반환
    """
    headers = {"Content-Type": "application/json", "Authorization": "Bearer {}".format(get_lv_token(test_email, test_pw))}

    invalid_id_list = ['nononono','wrong','inval']
    payload = {
        "ids": invalid_id_list
    }
    response = requests.post(get_lv_baseurl + url_manager.logdownload_api_path, headers=headers, data=json.dumps(payload,indent=4), verify = False)
    assert response.status_code == 200
    # 데이터 없는 경우 헤더 데이터만 반환
    assert '"id","transactionId","log","loggedAt","objectKey","host","component","containerId","logLevel","logType","logStatus","updatedAt","createdAt"\n' == response.text
    
def test_logdownload_notexistlogid2(get_lv_baseurl, get_lv_token, get_logfile_idlist):
    """ 테스트 목적 : 3건의 id 중 가운데 하나의 id 값이 없는 값일때 다운로드 테스트 - 200ok, 유효한 2건의 데이터 반환
    """
    headers = {"Content-Type": "application/json", "Authorization": "Bearer {}".format(get_lv_token(test_email, test_pw))}
    id_list = get_logfile_idlist
    id_list[1] = 'wrongid'
    payload = {
        "ids": id_list
    }
    response = requests.post(get_lv_baseurl + url_manager.logdownload_api_path, headers=headers, data=json.dumps(payload,indent=4), verify = False)
    assert response.status_code == 200
    # '"id","transactionId","log","loggedAt","objectKey","host","component","containerId","logLevel","logType","logStatus","updatedAt","createdAt"\n
    # "602efa5c67bd0a718525ca85","","[GW] [DEBUG] 2020-09-15 05:45:54,905 log:228 Internal Server Error: /cxr-v3/predictions/e373d0a5-8aee-4404-9367-f219de0e5d8b/contour.jpg",
    # "2020-09-15T05:45:54.905","/tmp/tempLog/host_test_1.container_id_test_1.INFERENCE_SERVER.daily.log.2020-10-16-test.log","host_test_1","INFERENCE_SERVER","container_id_test_1","DEBUG","APP","","2021-02-18T23:38:04.384","2021-02-18T23:38:04.384"\n
    # 
    # "602efa5c67bd0a718525ca86","","[BE] [DEBUG] 2020-09-15 05:45:54,905 log:228 Internal Server Error: /cxr-v3/predictions/e373d0a5-8aee-4404-9367-f219de0e5d8b/contour.jpg",
    # "2020-09-15T05:45:54.905","/tmp/tempLog/host_test_1.container_id_test_1.INFERENCE_SERVER.daily.log.2020-10-16-test.log",
    # "host_test_1","INFERENCE_SERVER","container_id_test_1","DEBUG","APP","","2021-02-18T23:38:04.384","2021-02-18T23:38:04.384"\n'
    assert '' != response.text

