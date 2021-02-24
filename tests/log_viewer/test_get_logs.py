#-*- coding: utf-8 -*-
import os, sys, io
import os.path
import requests
import pytest
from common.api_constants import LogViewerConstants as url_manager

user_token = None
base_url = None

test_email = url_manager.test_email
test_pw = url_manager.test_pw

def test_get_logs_default_200(lv_api_url, get_lv_token, get_dirpath):
    headers = {"Authorization": "Bearer {}".format(get_lv_token(test_email, test_pw))}
    response = requests.get(lv_api_url + url_manager.getloglist_api_path, headers=headers, verify = False) # = get_dirpath+'/base64_lunit_cert.cer')
    assert response.status_code == 200
    response_body = response.json()
    assert response_body.get("content") != None
    assert response_body.get("empty") != None
    assert response_body.get("first") != None   
    assert response_body.get("first") == True # 디폴트 조회이므로 first는 무조건 True   
    assert response_body.get("last") != None
    assert response_body.get("number") != None
    assert response_body.get("numberOfElements") != None
    assert response_body.get("pageable") != None
    
    pageable_element = response_body.get("pageable")
    assert pageable_element.get("offset") != None
    assert pageable_element.get("pageNumber") != None
    assert pageable_element.get("pageSize") != None
    assert pageable_element.get("pageSize") ==100   # 디폴트 사이즈는 100 
    assert pageable_element.get("paged") != None
    assert pageable_element.get("paged") == True
    assert pageable_element.get("sort") != None
    #   'sort': {
    #       'empty': False, 
    #       'sorted': True, 
    #       'unsorted': False}, 
    assert pageable_element.get("unpaged") != None
    assert "size" in response_body   # 값 자체가 None인 경우가 있어서 element 존재 여부만 체크 
    assert response_body.get("size") == 100  # 현재는 로그가 많아서 한 페이지당 갯수 100 에 따라 첫페이지 100개 size 값.
    assert response_body.get("totalElements") != None
    assert response_body.get("totalPages") != None
    
    contents_element = response_body.get("content")
    assert len(contents_element) > 0
    first_content = contents_element[0]
    assert first_content.get('component')!= None
    assert first_content.get('containerId')!= None
    assert first_content.get('createdAt')!= None
    assert first_content.get('host')!= None
    assert first_content.get('id')!= None
    assert first_content.get('log')!= None
    assert first_content.get('logLevel')!= None
    assert 'logStatus' in first_content # 현재 값 자체가 None이어서 존재 여부만 체크 
    assert first_content.get('logType')!= None
    assert first_content.get('loggedAt')!= None
    assert first_content.get('objectKey')!= None
    assert 'transactionId' in first_content # 현재 값 자체가 None이어서 존재 여부만 체크 
    assert first_content.get('updatedAt')!= None

def test_get_logs_search(lv_api_url, get_lv_token, get_dirpath):
    search_component = "INFERENCE_SERVER" # INFERENCE_SERVER / GATEWAY / INSIGHT_BACKEND_CXR / INSIGHT_BACKEND_MMG
    search_keyword = "Server Error"
    search_loglevel = "DEBUG" # DEBUG / ERROR / FATAL 
    search_logtype = "APP"
    search_pagesize = 10

    headers = {"Authorization": "Bearer {}".format(get_lv_token(test_email, test_pw))}
    params = {
        'components': search_component, 
        'keyword': search_keyword, 
        'logLevels': search_loglevel, 
        'logTypes': search_logtype, 
        'page': 0, 
        'size': search_pagesize, 
        'sort': 'loggedAt'
        } # '2020-09-15T05:45:54.905'
    # components, startDate, endDate, 
    # keyword, logLevels, logStatus, logTypes, page, size, sort
    response = requests.get(lv_api_url + url_manager.getloglist_api_path, headers=headers, params=params, verify = False)
    assert response.status_code == 200
    
    response_body = response.json()
    assert response_body.get("content") != None
    pageable_element = response_body.get("pageable")
    assert pageable_element.get("pageSize") == search_pagesize
    assert pageable_element.get("pageNumber") == 0
    assert response_body.get("size") == search_pagesize # 결과 데이터가 10건 미만이면 실패할 수 있음 
    assert pageable_element.get("sort") != None
    #   'sort': {
    #       'empty': False, 
    #       'sorted': True, 
    #       'unsorted': False}, 
    
    contents_element = response_body.get("content")
    assert len(contents_element) > 0    # 결과 데이터가 없으면 실패할 수 있음 
    for this_record in contents_element:
        ##### 조회된 모든 데이터에 대해 검색 조건 반영됐는지 for 문 돌면서 확인 
        assert this_record.get('component') == "INFERENCE_SERVER"
        assert "Server Error" in this_record.get('log')
        assert this_record.get('logLevel')== "DEBUG"
        assert this_record.get('logType')== "APP"


def test_get_logs_sort(lv_api_url, get_lv_token, get_dirpath):
    print("")

def test_get_logs_paging(lv_api_url, get_lv_token, get_dirpath):
    search_pagesize = 10
    search_page = 3

    headers = {"Authorization": "Bearer {}".format(get_lv_token(test_email, test_pw))}
    params = {
        'page': search_page, 
        'size': search_pagesize
        }
    response = requests.get(lv_api_url + url_manager.getloglist_api_path, headers=headers, params=params, verify = False)
    assert response.status_code == 200
    
    response_body = response.json()
    assert response_body.get("content") != None
    pageable_element = response_body.get("pageable")
    assert pageable_element.get("pageSize") == search_pagesize
    assert pageable_element.get("pageNumber") == search_page


def test_get_logs_search_capitalkeyword(lv_api_url, get_lv_token, get_dirpath):
    search_keyword = "SERVER ERROR" # find 'Server Error' log text with 'SERVER ERROR' uppercase keyword

    search_component = "INFERENCE_SERVER" # INFERENCE_SERVER / GATEWAY / INSIGHT_BACKEND_CXR / INSIGHT_BACKEND_MMG
    search_loglevel = "DEBUG" # DEBUG / ERROR / FATAL 
    search_logtype = "APP"

    headers = {"Authorization": "Bearer {}".format(get_lv_token(test_email, test_pw))}
    params = {
        'components': search_component, 
        'keyword': search_keyword, 
        'logLevels': search_loglevel, 
        'logTypes': search_logtype, 
        'page': 0
        }
    response = requests.get(lv_api_url + url_manager.getloglist_api_path, headers=headers, params=params, verify = False)
    assert response.status_code == 200
    
    response_body = response.json()
    assert response_body.get("content") != None
    contents_element = response_body.get("content")
    assert len(contents_element) > 0    # 결과 데이터가 없으면 실패할 수 있음 
    for this_record in contents_element:
        ##### 조회된 모든 데이터에 대해 검색 조건 반영됐는지 for 문 돌면서 확인 
        assert "Server Error" in this_record.get('log')

def test_get_logs_daterangesearch(lv_api_url, get_lv_token, get_dirpath):
    print("")

# def test_add_log_200(lv_api_url, get_lv_token, get_dirpath):
#     headers = {'Content-Type': 'multipart/form-data; boundary=----WebKitFormBoundaryY4ruG5YEGEX3yU47', "Authorization": "Bearer {}".format(get_lv_token(test_email, test_pw))}
#     # Body
#     with open(get_dirpath+'/sample_log.log', 'rb') as f:
#         sample = bytearray(f.read())
#         f.close()
    
#     payload = {
#         "containerId ": "pytest_automation",
#         # "file" : (io.BytesIO(b"abcdef"), 'test.dcm'),
#         "file" : (sample, 'test.dcm'),
#         "host" : "http://10.220.150.115"
#     }

#     response = requests.post(lv_api_url + url_manager.getloglist_api_path, data=payload, headers = headers, verify = False) # =get_dirpath+'/base64_lunit_cert.cer')
#     # data=json.dumps(payload, indent=4)
#     print(response.text)
#     assert response.status_code == 200
#     response_body = response.json()
#     assert "" == response_body["message"]


# def test_get_log_200(lv_api_url, get_lv_token, lv_tokener):
#     headers = {"Authorization": "Bearer {}".format(get_lv_token(test_email, test_pw))}
#     temp_id = "temp_id"
#     response = requests.get(lv_api_url + url_manager.getloglist_api_path+"/"+temp_id, headers = headers, verify = False)
#     assert response.status_code == 200
#     response_body = response.json()
#     assert "" == response_body["message"]



