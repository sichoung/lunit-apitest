#-*- coding: utf-8 -*-
import os, sys, io
import requests
import pytest
import pydicom
import json, time
from common import api_test_util as util

this_api_path = '/cxr-v3/dcm/'

# Accept-Language: en

# def test_upload_200ok(get_be_baseurl, get_dirpath, get_apikey):
#     # 400 bad request가 나서 아래 방법으로 전송해야 함 
#     headers = {"Authorization": "Bearer "+get_apikey,
#                "Content-Type": "multipart/form-data"}
#     values = {
#         "file": ("normal.dcm", util.get_file_binary(get_dirpath+"/be/normal.dcm"))
#     }
#     response = requests.post(get_be_baseurl + this_api_path, data=values, headers=headers)
#     print(response.text)
#     assert 201 == response.status_code
#     response_body = response.json()
#     print("")

def test_uploaddicom_201ok(get_be_baseurl, get_dirpath, get_apikey):
    headers = {"Authorization": "Bearer "+get_apikey}

    values = {
        "file": ("normal.dcm", open(get_dirpath+"/be/normal.dcm", "rb"))
    }
    # response = requests.post(get_be_baseurl + this_api_path, data={"file": open(get_dirpath+"/be/normal.dcm", "rb")}  , headers=headers)
    response = requests.post(get_be_baseurl + this_api_path, files=values, headers=headers)

    assert 201 == response.status_code

    response_body = response.json()
    assert "cxr-v3" == response_body["app"]
    assert "uuid" in response_body
    save_uuid = response_body["uuid"]
    assert "file" in response_body
    assert True == response_body.get("valid")
    assert "width" in response_body
    assert "height" in response_body
    assert "created_at" in response_body
    print(f"generated_uuid = {save_uuid}")


def test_uploaddicom_wrongapikey(get_be_baseurl, get_dirpath, get_apikey):
    headers = {"Authorization": "Bearer {}".format("invalid_value_key")}
    values = {
        "file": ("normal.dcm", open(get_dirpath+"/be/normal.dcm", "rb"))
    }

    response = requests.post(get_be_baseurl + this_api_path, files=values, headers=headers)

    print(response.text)
    assert 401 == response.status_code
    response_body = response.json()
    assert "message" in response_body
    assert "code" in response_body
    assert "insight_error_code" in response_body
    assert "API Key Error: Token has been corrupted, thus undecodable." == response_body.get("message")
    assert "401.50.ISTBE.999" == response_body.get("insight_error_code")

def test_uploaddicom_invalidapikey(get_be_baseurl, get_dirpath, get_apikey):
    headers = {"Authorization": "Bearer "+"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiJiYWI4NzVkYS03ZWUxLTRmYzYtOTNiOC1mZWIxZDIwY2E5NzUiLCJpc3MiOiJMdW5pdCIsImlhdCI6MTYwNjExMjc4MCwiZXhwIjoxNjEzODg4NzgwLCJuYmYiOjE2MDYxMTI3ODAsImF1ZCI6Imh0dHBzOi8vaW5zaWdodC5sdW5pdC5pbyIsImRhdGEiOnsiY291bnRyeV9pZCI6MSwiY291bnRyeV9uYW1lIjoiQWZnaGFuaXN0YW4ifX0.XEmOg5ZBZiHyzhcZJRuu12J-_VxyGfbvVPWygee23qc"}
    values = {
        "file": ("normal.dcm", open(get_dirpath+"/be/normal.dcm", "rb"))
    }

    response = requests.post(get_be_baseurl + this_api_path, files=values, headers=headers)

    print(response.text)
    assert 401 == response.status_code
    response_body = response.json()
    assert "message" in response_body
    assert "code" in response_body
    assert "insight_error_code" in response_body
    assert "This api key is not registered." == response_body.get("message")
    assert "401.50.ISTBE.999" == response_body.get("insight_error_code")


def test_uploaddicom_nofile(get_be_baseurl, get_dirpath, get_apikey):
    headers = {"Authorization": "Bearer "+get_apikey}
    values = {
        "file": None
    }

    response = requests.post(get_be_baseurl + this_api_path, files=values, headers=headers)

    assert 400 == response.status_code
    response_body = response.json()
    assert "code" in response_body
    assert "file: No file was submitted." == response_body.get("message")
    assert "400.50.ISTBE.004" == response_body.get("insight_error_code")
    # '{"message":"file: No file was submitted.","code":400,"insight_error_code":"400.50.ISTBE.004"}'

def test_uploaddicom_nodicomfile(get_be_baseurl, get_dirpath, get_apikey):
    headers = {"Authorization": "Bearer "+get_apikey}
    values = {
        "file": ("nodcm.dcm", (io.BytesIO(b"thisisnotdicomfile")))
    }
    response = requests.post(get_be_baseurl + this_api_path, files=values, headers=headers)
    assert 415 == response.status_code
    response_body = response.json()
    assert "code" in response_body
    assert "Unable to pre-load DICOM" == response_body.get("message")
    assert "415.50.ISTBE.001" == response_body.get("insight_error_code")

@pytest.mark.skip(reason="no difference, not refering to lanaguage when uploading")
def test_uploaddicom_notsupportlanguage(get_be_baseurl, get_dirpath, get_apikey):
    headers = {"Authorization": "Bearer "+get_apikey, "Accept-Language":"kr"}
    values = {
        "file": ("normal.dcm", open(get_dirpath+"/be/normal.dcm", "rb"))
    }
    response = requests.post(get_be_baseurl + this_api_path, files=values, headers=headers)

    assert 201 == response.status_code