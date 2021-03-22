#-*- coding: utf-8 -*-
import os, sys, io
import requests
import pytest
import pydicom
import json, time
from common import api_test_util as util
from common.db_manager import BEDBManager

# integration = pytest.mark.integration

BE_UPLOAD_APIPATH = "/cxr-v3/dcm/"
BE_PREDICT_APIPATH = "/cxr-v3/models/latest/predict/"
BE_REPORT_APIPATH = "/cxr-v3/predictions/{predict_uuid}/report"

# @integration
def test_intg_001(get_be_baseurl, get_dirpath, get_be_apikey):
    """ upload, predict, report flow testing with thresould 0.25 """
    test_threshold_value = 0.25

    # 1) upload
    headers = {"Authorization": "Bearer "+get_be_apikey}
    values = {"file": ("normal.dcm", open(get_dirpath+"/be/normal.dcm", "rb"))}
    response = requests.post(get_be_baseurl + BE_UPLOAD_APIPATH, files=values, headers=headers)
    assert 201 == response.status_code
    response_body = response.json()
    assert "cxr-v3" == response_body["app"]
    assert "uuid" in response_body
    dicom_uuid = response_body["uuid"]

    # 2) predict
    headers = {"Content-Type": "application/json", "Authorization": "Bearer "+get_be_apikey}
    payload = {
        "case": [
            {
                "dicom": dicom_uuid,
                "view_name": "frontal"
            }
        ],
        "threshold": test_threshold_value,
        "filtering": False
    }
    response = requests.post(get_be_baseurl + BE_PREDICT_APIPATH, data=json.dumps(payload,indent=4), headers=headers)
    assert 200 == response.status_code, "Failed to predict!! - "+response.text
    response_body = response.json()
    assert "uuid" in response_body
    predict_uuid = response_body.get("uuid")
    assert "inference_model" in response_body
    assert "case" in response_body
    first_case = response_body.get("case")[0]
    assert "dicom" in first_case
    assert "view_name" in first_case
    assert test_threshold_value == response_body.get("threshold")
    assert False == response_body.get("filtering")

    # 3) report
    headers = {"Authorization": "Bearer "+get_be_apikey}
    params = {"lesion_names":"atelectasis,calcification,cardiomegaly,consolidation,fibrosis,mediastinal_widening,nodule,pleural_effusion,pneumoperitoneum,pneumothorax"}
    response = requests.get(get_be_baseurl + BE_REPORT_APIPATH.format(predict_uuid = predict_uuid), params = params, headers=headers)

    assert 200 == response.status_code
    response_body = response.json()
    assert "report" in response_body
    report_info = response_body.get("report")
    assert "nodule" in report_info
    assert "pneumoperitoneum" in report_info
    assert "atelectasis" in report_info
    assert "calcification" in report_info
    assert "mediastinal_widening" in report_info
    assert "fibrosis" in report_info
    assert "consolidation" in report_info
    assert "pneumothorax" in report_info
    assert "pleural_effusion" in report_info
    assert "cardiomegaly" in report_info

@pytest.mark.skip(reason="This chages DB info. it is risky. Do not run")
def test_intg_002(get_be_baseurl, get_dirpath, get_be_apikey):
    """ 동적으로 더미서버 IS 연동 변경 테스트. upload 후 predict할 때 IS에 임의의 에러가 나도록 한후 BE의 동작 확인   """
    test_threshold_value = 0.25

    # 강제로 개인 VM으로 BE 지정 
    # get_be_baseurl = "http://10.220.150.115:8000"
    # get_apikey = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiI4YzNiZDk5Yi0wMzhlLTQ5ZGQtODZkNi02ZjFiYjRlNDAxMzEiLCJpc3MiOiJMdW5pdCIsImlhdCI6MTYxMjQwNDQ1OCwiZXhwIjoxNjIwMTgwNDU4LCJuYmYiOjE2MTI0MDQ0NTgsImF1ZCI6Imh0dHBzOi8vaW5zaWdodC5sdW5pdC5pbyIsImRhdGEiOnsiY291bnRyeV9pZCI6MSwiY291bnRyeV9uYW1lIjoiQWZnaGFuaXN0YW4ifX0.VqoOpdPWDAa8FdJ4pdUuqnTf-PK6cprgBi5lANxgD4Q"
    
    # 1) upload
    headers = {"Authorization": "Bearer "+get_be_apikey}
    values = {"file": ("normal.dcm", open(get_dirpath+"/be/normal.dcm", "rb"))}
    response = requests.post(get_be_baseurl + BE_UPLOAD_APIPATH, files=values, headers=headers)
    assert 201 == response.status_code
    response_body = response.json()
    assert "cxr-v3" == response_body["app"]
    assert "uuid" in response_body
    dicom_uuid = response_body["uuid"]

    util.dummy_is_cxr3_set("cxr3_result_is_predict", 400, "notfound", 1)
    be_db_manager = BEDBManager("10.120.0.11","5433", "lunit", "lunitinsight", "insight_backend")
    currentinfo_list = be_db_manager.get_cxr3_info()
    current_host = currentinfo_list[1]
    current_port = currentinfo_list[2]
    be_db_manager.update_cxr3_info("10.220.150.115", "7711")
    
    util.dummy_is_cxr3_reset()

    # 2) predict
    headers = {"Content-Type": "application/json", "Authorization": "Bearer "+get_be_apikey}
    payload = {
        "case": [
            {
                "dicom": dicom_uuid,
                "view_name": "frontal"
            }
        ],
        "threshold": test_threshold_value,
        "filtering": False
    }
    response = requests.post(get_be_baseurl + BE_PREDICT_APIPATH, data=json.dumps(payload,indent=4), headers=headers)

    be_db_manager.update_cxr3_info(current_host, current_port)

    assert 200 == response.status_code, "Failed to predict!! - "+response.text
    


