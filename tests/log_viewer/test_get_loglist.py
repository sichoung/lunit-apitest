#-*- coding: utf-8 -*-
import os, sys, io
import os.path
import requests
import pytest
from datetime import datetime
from common.api_constants import LogViewerConstants as url_manager

test_email = url_manager.test_email
test_pw = url_manager.test_pw

def test_get_loglist_default_200(get_lv_baseurl, get_lv_token):
    """ 테스트 목적 : 특정 검색 조건없이 전체 조회 후 응답 json의 스키마, 디폴트값 적용 등을 확인(pagesize=100,... )
    """
    headers = {"Authorization": "Bearer {}".format(get_lv_token(test_email, test_pw))}
    response = requests.get(get_lv_baseurl + url_manager.getloglist_api_path, headers=headers, verify = False) # = get_dirpath+'/base64_lunit_cert.cer')
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
    # assert first_content.get('containerId')!= None
    assert first_content.get('createdAt')!= None
    assert first_content.get('host')!= None
    assert first_content.get('id')!= None
    assert first_content.get('log')!= None
    assert first_content.get('logLevel')!= None
    assert 'logStatus' in first_content # 현재 값 자체가 None이어서 존재 여부만 체크 
    assert first_content.get('logType')!= None
    assert first_content.get('loggedAt')!= None
    assert 'transactionId' in first_content # 현재 값 자체가 None이어서 존재 여부만 체크 
    #{
#     'component': 'BE', 
#     'createdAt': '2021-03-06T03: 44: 46.518', 
#     'host': 'test01', 
#     'id': 'Pf6jBXgBkFCJ_69qP8PO', 
#     'log': 'log: 228 Internal Server Error: /cxr-v3/predictions/e373d0a5-8aee-4404-9367-f219de0e5d8b/contour.jpg', 
#     'logLevel': 'DEBUG', 
#     'logStatus': None, 
#     'logType': 'APP', 
#     'loggedAt': '2020-09-15T05: 45: 54.905', 
#     'transactionId': 'transaction-id-test'
#   }


def test_get_loglist_search_200(get_lv_baseurl, get_lv_token):
    """ 테스트 목적 : 여러 검색 조건을 복합적으로 적용하여 조회 후 조회 결과에 반영되었는지 확인
    """
    search_component = "IS" # INFERENCE_SERVER / GATEWAY / INSIGHT_BACKEND_CXR / INSIGHT_BACKEND_MMG
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
    response = requests.get(get_lv_baseurl + url_manager.getloglist_api_path, headers=headers, params=params, verify = False)
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
        assert this_record.get('component') == "IS"
        assert "Server Error" in this_record.get('log')
        assert this_record.get('logLevel')== "DEBUG"
        assert this_record.get('logType')== "APP"

def test_get_loglist_nodata(get_lv_baseurl, get_lv_token):
    """ 테스트 목적 : 조회 결과가 없을 때 응답이 어떻게 오는지 확인
    """
    search_component = "IS" # INFERENCE_SERVER / GATEWAY / INSIGHT_BACKEND_CXR / INSIGHT_BACKEND_MMG
    search_keyword = "nodata found search string"
    search_loglevel = "ERROR" # DEBUG / ERROR / FATAL 
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
        }
    response = requests.get(get_lv_baseurl + url_manager.getloglist_api_path, headers=headers, params=params, verify = False)
    assert response.status_code == 200
    
    response_body = response.json()
    assert response_body.get("content") != None
    contents_element = response_body.get("content")
    assert len(contents_element) == 0
    assert response_body.get("totalElements") != None
    assert response_body.get("totalPages") != None
    assert response_body.get("totalElements") != None
    assert response_body.get("first") == True
    assert response_body.get("last") == True
    
# def test_get_loglist_sort(get_lv_baseurl, get_lv_token):
#     """ 테스트 목적 : 정렬 적용을 확인 - 아직 테스트 방법 파악 중
#     """
#     print("")

def test_get_loglist_paging(get_lv_baseurl, get_lv_token):
    """ 테스트 목적 : 조회 결과에 대한 페이징 처리 확인.. 
    """
    search_pagesize = 10
    search_page = 3

    headers = {"Authorization": "Bearer {}".format(get_lv_token(test_email, test_pw))}
    params = {
        'page': search_page, 
        'size': search_pagesize
        }
    response = requests.get(get_lv_baseurl + url_manager.getloglist_api_path, headers=headers, params=params, verify = False)
    assert response.status_code == 200
    
    response_body = response.json()
    assert response_body.get("content") != None
    pageable_element = response_body.get("pageable")
    assert pageable_element.get("pageSize") == search_pagesize
    assert pageable_element.get("pageNumber") == search_page

def test_get_loglist_search_capitalkeyword(get_lv_baseurl, get_lv_token):
    """ 테스트 목적 : Server Error 텍스트에 대해 키워드 검색 대문자 SERVER ERROR로 검색이 되는지 확인 
    """
    search_uppercase_keyword = "SERVER ERROR" # find 'Server Error' log text with 'SERVER ERROR' uppercase keyword

    search_component = "IS" # INFERENCE_SERVER / GATEWAY / INSIGHT_BACKEND_CXR / INSIGHT_BACKEND_MMG
    search_loglevel = "DEBUG" # DEBUG / ERROR / FATAL 
    search_logtype = "APP"

    headers = {"Authorization": "Bearer {}".format(get_lv_token(test_email, test_pw))}
    params = {
        'components': search_component, 
        'keyword': search_uppercase_keyword, 
        'logLevels': search_loglevel, 
        'logTypes': search_logtype, 
        'page': 0
        }
    response = requests.get(get_lv_baseurl + url_manager.getloglist_api_path, headers=headers, params=params, verify = False)
    assert response.status_code == 200
    
    response_body = response.json()
    assert response_body.get("content") != None
    contents_element = response_body.get("content")
    assert len(contents_element) > 0    # 결과 데이터가 없으면 실패할 수 있음 
    for this_record in contents_element:
        assert "Server Error" in this_record.get('log')

# @pytest.mark.skip(reason="not yet find valid date format")
def test_get_loglist_daterangesearch(get_lv_baseurl, get_lv_token):
    """ 테스트 목적 : 날짜 범위로 검색 
    """
    search_startdate = "2020-09-15 05:45" # '2020-09-15T05:45:54.905'
    search_enddate = "2020-09-15 05:45"
    search_keyword = "error"

    headers = {"Authorization": "Bearer {}".format(get_lv_token(test_email, test_pw))}
    params = {
        # startDate, endDate, 
        'startDate': search_startdate, 
        'endDate': search_enddate,
        'keyword': search_keyword, 
        'page': 0
        }
    response = requests.get(get_lv_baseurl + url_manager.getloglist_api_path, headers=headers, params=params, verify = False)
    assert response.status_code == 200
    
    response_body = response.json()
    assert response_body.get("content") != None
    contents_element = response_body.get("content")
    assert len(contents_element) > 0    # 결과 데이터가 없으면 실패할 수 있음 
    for this_record in contents_element:
        assert "rror" in this_record.get('log')

def test_get_loglist_switcheddaterange(get_lv_baseurl, get_lv_token):
    """ 테스트 목적 : 날짜 범위 앞뒤 선후관계가 바뀐 상태로 검색 요청
    """
    search_startdate = "2020-09-16 05:45" # '2020-09-15T05:45:54.905'
    search_enddate = "2020-09-14 05:45"
    search_keyword = "rror"
    
    headers = {"Authorization": "Bearer {}".format(get_lv_token(test_email, test_pw))}
    params = {
        # startDate, endDate, 
        'startDate': search_startdate, 
        'endDate': search_enddate,
        'keyword': search_keyword, 
        'page': 0
        }
    response = requests.get(get_lv_baseurl + url_manager.getloglist_api_path, headers=headers, params=params, verify = False)
    assert response.status_code == 200
    
    response_body = response.json()
    assert response_body.get("content") != None
    contents_element = response_body.get("content")
    assert len(contents_element) > 0    # 결과 데이터가 없으면 실패할 수 있음 
    for this_record in contents_element:
        assert "rror" in this_record.get('log')

def test_get_loglist_invalid_dateformat(get_lv_baseurl, get_lv_token):
    """ 테스트 목적 : invalid format - 날짜 형태에 2020-09-15T 입력했을 때 응답 확인
    """
    search_startdate = "2020-09-15" # '2020-09-15 05:45'
    search_enddate = "2020-09-15"

    headers = {"Authorization": "Bearer {}".format(get_lv_token(test_email, test_pw))}
    params = {
        # startDate, endDate, 
        'startDate': search_startdate, 
        'endDate': search_enddate,
        'page': 0
        }
    response = requests.get(get_lv_baseurl + url_manager.getloglist_api_path, headers=headers, params=params, verify = False)
    assert response.status_code == 400 # failing. 500 returning
    response_body = response.json()
    assert response_body.get("code") == "500.0001.0005"
    assert response_body.get("message") == "Text '2020-09-15T' could not be parsed at index 10"

def test_get_loglist_wrongcomponenttype(get_lv_baseurl, get_lv_token):
    """ 테스트 목적 : invalid_COMPONENT
    """
    wrong_component = "invalid_COMPONENT"

    search_keyword = "Server Error"
    search_loglevel = "DEBUG" # DEBUG / ERROR / FATAL 
    search_logtype = "APP"
    search_pagesize = 10

    headers = {"Authorization": "Bearer {}".format(get_lv_token(test_email, test_pw))}
    params = {
        'components': wrong_component, 
        'keyword': search_keyword, 
        'logLevels': search_loglevel, 
        'logTypes': search_logtype, 
        'page': 0, 
        'size': search_pagesize, 
        'sort': 'loggedAt'
        }
    response = requests.get(get_lv_baseurl + url_manager.getloglist_api_path, headers=headers, params=params, verify = False)
    assert response.status_code == 400
    response_body = response.json()
    assert response_body.get("code") == "500.0001.0005"
    assert response_body.get("message") == "Failed to convert value of type 'java.lang.String' to required type 'java.util.List'; nested exception is org.springframework.core.convert.ConversionFailedException: Failed to convert from type [java.lang.String] to type [io.lunit.log.collector.server.code.Component] for value 'invalid_COMPONENT'; nested exception is java.lang.IllegalArgumentException: No enum constant io.lunit.log.collector.server.code.Component.invalid_COMPONENT"

def test_get_loglist_wrongloglevel(get_lv_baseurl, get_lv_token):
    """ 테스트 목적 : 잘못된 값 - 로그레벨에 대한 응답 확인
    """
    search_component = "IS" # INFERENCE_SERVER / GATEWAY / INSIGHT_BACKEND_CXR / INSIGHT_BACKEND_MMG
    search_keyword = "Server Error"
    # search_loglevel = "DEBUG" # DEBUG / ERROR / FATAL 
    wrong_loglevel = "invaliddddd" # DEBUG / ERROR / FATAL 
    search_logtype = "APP"
    search_pagesize = 10

    headers = {"Authorization": "Bearer {}".format(get_lv_token(test_email, test_pw))}
    params = {
        'components': search_component, 
        'keyword': search_keyword, 
        'logLevels': wrong_loglevel, 
        'logTypes': search_logtype, 
        'page': 0, 
        'size': search_pagesize, 
        'sort': 'loggedAt'
        } # '2020-09-15T05:45:54.905'
    # components, startDate, endDate, 
    # keyword, logLevels, logStatus, logTypes, page, size, sort
    response = requests.get(get_lv_baseurl + url_manager.getloglist_api_path, headers=headers, params=params, verify = False)
    assert response.status_code == 400
    response_body = response.json()
    assert response_body.get("code") == "500.0001.0005"
    assert response_body.get("message") == "Failed to convert value of type 'java.lang.String' to required type 'java.util.List'; nested exception is org.springframework.core.convert.ConversionFailedException: Failed to convert from type [java.lang.String] to type [io.lunit.log.collector.server.code.LogLevel] for value 'invaliddddd'; nested exception is java.lang.IllegalArgumentException: No enum constant io.lunit.log.collector.server.code.LogLevel.invaliddddd"

def test_get_loglist_wronglogtype(get_lv_baseurl, get_lv_token):
    """ 테스트 목적 : 잘못된 값 - 로그타입에 대한 응답 확인
    """
    search_component = "IS" # INFERENCE_SERVER / GATEWAY / INSIGHT_BACKEND_CXR / INSIGHT_BACKEND_MMG
    search_keyword = "Server Error"
    search_loglevel = "DEBUG" # DEBUG / ERROR / FATAL 
    # search_logtype = "APP"
    wrong_logtype = "INVAL"
    search_pagesize = 10

    headers = {"Authorization": "Bearer {}".format(get_lv_token(test_email, test_pw))}
    params = {
        'components': search_component, 
        'keyword': search_keyword, 
        'logLevels': search_loglevel, 
        'logTypes': wrong_logtype, 
        'page': 0, 
        'size': search_pagesize, 
        'sort': 'loggedAt'
        } # '2020-09-15T05:45:54.905'
    # components, startDate, endDate, 
    # keyword, logLevels, logStatus, logTypes, page, size, sort
    response = requests.get(get_lv_baseurl + url_manager.getloglist_api_path, headers=headers, params=params, verify = False)
    assert response.status_code == 400
    response_body = response.json()
    assert response_body.get("code") == "500.0001.0005"
    assert response_body.get("message") == "Failed to convert value of type 'java.lang.String' to required type 'java.util.List'; nested exception is org.springframework.core.convert.ConversionFailedException: Failed to convert from type [java.lang.String] to type [io.lunit.log.collector.server.code.LogType] for value 'INVAL'; nested exception is java.lang.IllegalArgumentException: No enum constant io.lunit.log.collector.server.code.LogType.INVAL"

def test_get_loglist_notauth(get_lv_baseurl):
    """ 테스트 목적 : 인증토큰 없이 로그 조회 시도 
    """
    # headers = {"Authorization": "Bearer {}".format(get_lv_token(test_email, test_pw))}
    response = requests.get(get_lv_baseurl + url_manager.getloglist_api_path, verify = False) # = get_dirpath+'/base64_lunit_cert.cer')
    assert response.status_code == 401
    assert response.text == ''  # 401일때 응답 바디가 없음 
    # response_body = response.json()


