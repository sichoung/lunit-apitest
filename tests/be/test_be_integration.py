#-*- coding: utf-8 -*-
import os, sys, io
import requests
import pytest
import pydicom
import json, time
from common import api_test_util as util

integration = pytest.mark.integration

BE_UPLOAD_APIPATH = "/cxr-v3/dcm/"
BE_PREDICT_APIPATH = "/cxr-v3/models/latest/predict/"
BE_REPORT_APIPATH = "/cxr-v3/predictions/{predict_uuid}/report"

#@integration
def test_intg_001(get_be_baseurl, get_dirpath, get_apikey):
    """ upload, predict, report flow testing with thresould 0.25 """
    test_threshold_value = 0.25

    # 1) upload
    headers = {"Authorization": "Bearer "+get_apikey}
    values = {"file": ("normal.dcm", open(get_dirpath+"/be/normal.dcm", "rb"))}
    response = requests.post(get_be_baseurl + BE_UPLOAD_APIPATH, files=values, headers=headers)
    assert 201 == response.status_code
    response_body = response.json()
    assert "cxr-v3" == response_body["app"]
    assert "uuid" in response_body
    dicom_uuid = response_body["uuid"]

    # 2) predict
    headers = {"Content-Type": "application/json", "Authorization": "Bearer "+get_apikey}
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
    headers = {"Authorization": "Bearer "+get_apikey}
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

def test_intg_002(get_be_baseurl, get_dirpath, get_apikey):
    """ upload, predict, report flow testing with thresould 0.25 """
    print("not yet implemented.")


