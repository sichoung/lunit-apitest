#-*- coding: utf-8 -*-
import os, sys, io
import requests
import pytest
import pydicom
import json, time
from common import api_test_util as util
from common.exceptions import APITestException

this_api_path = '/cxr-v3/predictions/{predict_uuid}/report'

def test_report_basic(get_be_baseurl, get_apikey, get_case_uuid):
    case_uuid = get_case_uuid
    headers = {"Authorization": "Bearer "+get_apikey}
    params = {"lesion_names":"atelectasis,calcification,cardiomegaly,consolidation,fibrosis,mediastinal_widening,nodule,pleural_effusion,pneumoperitoneum,pneumothorax"}
    response = requests.get(get_be_baseurl + this_api_path.format(predict_uuid = case_uuid), params = params, headers=headers)

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


def test_report_notexistuuid(get_be_baseurl, get_apikey):
    case_uuid = "notexistuuiddddddddddddddd"
    print(case_uuid)
    headers = {"Authorization": "Bearer "+get_apikey}
    params = {"lesion_names":"atelectasis,calcification,cardiomegaly,consolidation,fibrosis,mediastinal_widening,nodule,pleural_effusion,pneumoperitoneum,pneumothorax"}
    response = requests.get(get_be_baseurl + this_api_path.format(predict_uuid = case_uuid), params = params, headers=headers)

    assert 404 == response.status_code
    assert '<h1>Not Found</h1><p>The requested resource was not found on this server.</p>' == response.text


def test_report_nolesionname(get_be_baseurl, get_apikey, get_case_uuid):
    """ checking the result when no lesion_names requested(default behavior) """
    case_uuid = get_case_uuid
    headers = {"Authorization": "Bearer "+get_apikey}
    # params = {"lesion_names":"atelectasis,calcification,cardiomegaly,consolidation,fibrosis,mediastinal_widening,nodule,pleural_effusion,pneumoperitoneum,pneumothorax"}
    response = requests.get(get_be_baseurl + this_api_path.format(predict_uuid = case_uuid), headers=headers)

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

def test_report_invalidlesionname(get_be_baseurl, get_apikey, get_case_uuid):
    """ when wrong lesion_names requested. """
    case_uuid = get_case_uuid
    print(case_uuid)
    headers = {"Authorization": "Bearer "+get_apikey}
    params = {"lesion_names":"atelectasis,wrongname"}
    response = requests.get(get_be_baseurl + this_api_path.format(predict_uuid = case_uuid), params = params, headers=headers)

    assert 400 == response.status_code

    response_body = response.json()
    assert "message" in response_body
    assert "code" in response_body
    assert "insight_error_code" in response_body
    assert "is not a valid choice." in response_body.get("message")
    assert "400.50.ISTBE.004" == response_body.get("insight_error_code")
