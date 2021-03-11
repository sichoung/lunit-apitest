#-*- coding: utf-8 -*-
import os, sys, io
import requests
import pytest
import pydicom
import json, time
from common import api_test_util as util
from common.db_manager import BEDBManager

test_host = '10.220.150.115'
test_port = '5433'
test_id = 'lunit'
test_pw = 'lunitinsight'
test_dbname = 'insight_backend'


def test_getcxr3_info():
    dbmanager = BEDBManager(test_host,test_port,test_id,test_pw,test_dbname)
    result_list = dbmanager.get_cxr3_info()
    assert result_list != None
    assert len(result_list) == 5
    # assert result_list[0] == 5
    # assert result_list[1] == 
    # assert result_list[2] == 
    assert result_list[3] == "cxr-v3"
    assert result_list[4] == "latest"


def test_getmmg_info():
    dbmanager = BEDBManager(test_host,test_port,test_id,test_pw,test_dbname)
    result_list = dbmanager.get_mmg_info()
    assert result_list != None
    assert len(result_list) == 5
    # assert result_list[0] == 5
    # assert result_list[1] == 
    # assert cxr3_result_listinfo_list[2] == 
    assert result_list[3] == "mmg"
    assert result_list[4] == "latest"


def test_updagtecxr3_info():
    before_host = None
    before_port = None 
    to_change_host = "10.10.10.10"
    to_change_port = 7777

    dbmanager = BEDBManager(test_host,test_port,test_id,test_pw,test_dbname)
    # 이전값 조회
    result_list = dbmanager.get_cxr3_info()
    assert result_list != None
    assert len(result_list) == 5
    before_host = result_list[1]
    before_port = result_list[2]

    # 값 수정
    dbmanager.update_cxr3_info(to_change_host, to_change_port)
    
    # 변경된 값 확인
    result_list = dbmanager.get_cxr3_info()
    assert result_list != None
    assert len(result_list) == 5
    assert to_change_host == result_list[1]
    assert to_change_port == result_list[2]

    # 다시 원복
    dbmanager.update_cxr3_info(before_host, before_port)

    # 원복 확인
    result_list = dbmanager.get_cxr3_info()
    assert result_list != None
    assert len(result_list) == 5
    assert before_host == result_list[1]
    assert before_port == result_list[2]

def test_updagtemmg_info():
    before_host = None
    before_port = None 
    to_change_host = "10.10.10.10"
    to_change_port = 7777

    dbmanager = BEDBManager(test_host,test_port,test_id,test_pw,test_dbname)
    # 이전값 조회
    result_list = dbmanager.get_mmg_info()
    assert result_list != None
    assert len(result_list) == 5
    before_host = result_list[1]
    before_port = result_list[2]

    # 값 수정
    dbmanager.update_mmg_info(to_change_host, to_change_port)
    
    # 변경된 값 확인
    result_list = dbmanager.get_mmg_info()
    assert result_list != None
    assert len(result_list) == 5
    assert to_change_host == result_list[1]
    assert to_change_port == result_list[2]

    # 다시 원복
    dbmanager.update_mmg_info(before_host, before_port)

    # 원복 확인
    result_list = dbmanager.get_mmg_info()
    assert result_list != None
    assert len(result_list) == 5
    assert before_host == result_list[1]
    assert before_port == result_list[2]

