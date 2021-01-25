#-*- coding: utf-8 -*-
import os, sys, io
import os.path
import requests
import pytest

this_api_path = '/gcm/product-type'
cxr_base_url = ''
mmg_base_url = ''

def test_cxr3_getproducttype_200ok(get_gcm_cxr3_baseurl):
    response = requests.get(get_gcm_cxr3_baseurl + this_api_path)
    assert 200 == response.status_code

    print("response text is " + response.text)
    response_body = response.json()
    assert (response_body["product_type"])
    # TODO: cxr3 반환여부는 요청 대상에 따라 다르므로 assert 제거 예정
    assert "cxr3" == response_body["product_type"]

def test_mmg_getproducttype_200ok(get_gcm_mmg_baseurl):
    response = requests.get(get_gcm_mmg_baseurl + this_api_path)
    assert 200 == response.status_code

    print("response text is " + response.text)
    response_body = response.json()
    assert (response_body["product_type"])
    # TODO: cxr3 반환여부는 요청 대상에 따라 다르므로 assert 제거 예정
    assert "cxr3" == response_body["product_type"]
