#-*- coding: utf-8 -*-
import os, sys, io
import requests
import pytest
import pydicom
import json, time
from common import api_test_util as util
from common.exceptions import APITestException
# import test_be_uploaddicom as test_upload

this_api_path = '/cxr-v3/models/latest/predict/'

@pytest.fixture(scope="module")
def get_dicom_uuid(get_be_baseurl, get_apikey, get_dirpath):
    upload_api_path = '/cxr-v3/dcm/'
    headers = {"Authorization": "Bearer "+get_apikey}
    values = {
        "file": ("normal.dcm", open(get_dirpath+"/be/normal.dcm", "rb"))
    }
    response = requests.post(get_be_baseurl + upload_api_path, files=values, headers=headers)
    if 201 != response.status_code:
        raise APITestException("Failed to upload dicom file and get uuid - {}".format(response.text))
    else:
        yield response.json()["uuid"]


def test_predict_200ok(get_be_baseurl, get_apikey, get_dicom_uuid):
    test_uuid = get_dicom_uuid
    headers = {"Content-Type": "application/json", "Authorization": "Bearer "+get_apikey}
    payload = {
        "case": [
            {
                "dicom": test_uuid,
                "view_name": "frontal"
            }
        ],
        "threshold": 0.15,
        "filtering": False
    }
    response = requests.post(get_be_baseurl + this_api_path, data=json.dumps(payload,indent=4), headers=headers)

    assert 200 == response.status_code

    response_body = response.json()
    # assert test_uuid == response_body.get("uuid") ?? 다른 uuid가 반환됨
    assert "inference_model" in response_body
    child_inference_model = response_body.get("inference_model")
    assert "tag" in child_inference_model
    assert "description" in child_inference_model
    assert "supported_features" in child_inference_model
    assert "case" in response_body
    first_case = response_body.get("case")[0]
    assert "dicom" in first_case
    assert "view_name" in first_case

    assert 0.15 == response_body.get("threshold")
    assert False == response_body.get("filtering")

    assert "status" in response_body
    assert "SUCCESS" == response_body.get("status")
    assert "status_code" in response_body
    assert "200.40.ISTIS.000" == response_body.get("status_code")
    assert "wait_time" in response_body
    assert "init_time" in response_body
    assert "prediction_time" in response_body
    assert "created_at" in response_body
    # '{"uuid":"35bfa433-d1c1-42c6-a19a-caeda4b10765",
    # "inference_model":{"tag":"3.6.0.1","description":"",
    # "supported_features":[]},
    # "case":[{"dicom":"a362bf4e-3bc7-447d-bb78-0f1db194cb6a",
    # "view_name":"frontal"}],
    # "threshold":0.15,
    # "filtering":false,
    # "wait_time":1.956839,
    # "init_time":null,
    # "prediction_time":1.74308,
    # "status":"SUCCESS",
    # "status_code":"200.40.ISTIS.000",
    # "created_at":"2021-02-01T16:55:29.321352+09:00"}'

def test_predict_dupuuid(get_be_baseurl, get_apikey, get_dicom_uuid):
    """ 동일 uuid에 대해 2번 분석 시도 """
    print("")


def test_predict_wrongjsonbody(get_be_baseurl, get_apikey, get_dicom_uuid):

    # assert 401 == response.status_code
    # response_body = response.json()
    # assert "message" in response_body
    # assert "code" in response_body
    # assert "insight_error_code" in response_body
    # assert "API Key Error: Token has been corrupted, thus undecodable." == response_body.get("message")
    # assert "401.50.ISTBE.999" == response_body.get("insight_error_code")

def test_predict_filteringon(get_be_baseurl, get_apikey, get_dicom_uuid):
    print("")


def test_predict_invalidapikey(get_be_baseurl, get_apikey, get_dicom_uuid):
    print("")


def test_predict_invalidapikey(get_be_baseurl, get_apikey, get_dicom_uuid):
    print("")
