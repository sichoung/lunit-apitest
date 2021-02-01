#-*- coding: utf-8 -*-
import os,sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import json
import requests
from pydicom import dcmread
from pydicom.filebase import DicomBytesIO

def get_env_var(var_name):
    tmp_value = os.environ.get(var_name)
    if tmp_value is None:
        print("There is no env variable matched - " + var_name)
    return tmp_value

def get_targetproduct():
    target_product = get_env_var('TARGET_PRODUCT')
    if target_product is None:
        os.environ['target_product'] = 'cxr3'
        return 'cxr3'
    else:
        return target_product

def dummy_set(url, version, api_id, status_code, test_type, sleep_time):
    if version == None or api_id == None or status_code == None or test_type == None: 
        raise Exception("error - TODO APITestException")
    
    headers = {'Content-Type': 'application/json'}
    payload = {
        'version': version,
        'api_id': api_id,
        'status_code': status_code,
        'test_type': test_type
        # 'sleep_time': Env4Dev.EMAILID
    }

    response = requests.post(url + "/dummy-setting", headers=headers, data=json.dumps(payload, indent=4))
    if response.status_code != 200:
        raise Exception("error - TODO APITestException")


class UrlManager():
    def __init__(self, email, password):
        self.email = email
        self.password = password
    
    def get_gcm_url(self):
        # TODO 컴포넌트와 테스트 모드에 따라 base_url을 반환해 주자
        return ''

    def get_gi_url(self):
        return ''

    def get_logviewer_url(self):
        return ''

def open_json_file(filepath):
    with open(filepath) as json_file:
        _json_body = json.load(json_file)
        json_file.close()
    return _json_body

def get_file_binary(filepath):
    with open(filepath, 'rb') as f:
        # sample = bytearray(f.read())
        sample = f.read()
        f.close()
    return sample


def get_dicom_binary(filepath):
    with open(filepath, 'rb') as f:
        raw = DicomBytesIO(f)
        ds = dcmread(raw)
        f.close()
    return ds
