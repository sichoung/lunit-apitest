#-*- coding: utf-8 -*-
import os,sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import json
import requests
from common.exceptions import APITestException

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


def dummy_be_set(api_id, status_code, test_type, sleep_time):
    if sleep_time == None:
        sleep_time = 0
    return dummy_set('http://10.220.150.115:7720', None, api_id, status_code, test_type, sleep_time)

def dummy_is_cxr3_set(api_id, status_code, test_type, sleep_time):
    if sleep_time == None:
        sleep_time = 0
    return dummy_set('http://10.220.150.115:7711', None, api_id, status_code, test_type, sleep_time)

def dummy_set(url, version, api_id, status_code, test_type, sleep_time):
    if api_id == None or status_code == None or test_type == None: 
        raise APITestException("error - required var is missing(version, api_id, status_code, test_type)")
    
    headers = {'Content-Type': 'application/json'}
    payload = {
        'version': version,
        'api_id': api_id,
        'status_code': status_code,
        'test_type': test_type,
        'sleep_time': sleep_time
    }

    response = requests.post(url + "/dummy-setting", headers=headers, data=json.dumps(payload, indent=4))
    if response.status_code != 200:
        raise APITestException("Failed to set dummy-server - {}".format(response.text))
    return True

def dummy_is_cxr3_reset():
    return dummy_reset('http://10.220.150.115:7711')

def dummy_reset(url):
    # try:
    response = requests.get(url + "/dummy-reset")
    if response.status_code != 200:
        raise APITestException("Failed to set dummy-server - {}".format(response.text))
    # except Exception:
    #     raise APITestException("Failed to set dummy-server")
    return True

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

# def get_dicom_binary(filepath):
#     with open(filepath, 'rb') as f:
#         raw = DicomBytesIO(f)
#         ds = dcmread(raw)
#         f.close()
#     return ds

class UrlManager():
    """ 원래는 현재 테스트 대상 url을 동적으로 반환하기 위해 만듬"""
    DUMMY_BE_URL = "http://10.220.150.115:7720"
    DUMMY_GW_URL = "http://10.220.150.115:7730"
    DUMMY_ISCXR3_URL = "http://10.220.150.115:7711"
    DUMMY_ISCXR2_URL = "http://10.220.150.115:7712"
    DUMMY_ISCXR1_URL = "http://10.220.150.115:7713"
    DUMMY_ISMMG_URL = "http://10.220.150.115:7714"
    
    test_mode = "dummy"

    # def __init__(self, test_mode):
    #     self.test_mode = test_mode
    
    def set_testmode(self, test_mode):
        self.test_mode = test_mode

    def get_gcm_url(self):
        # TODO 컴포넌트와 테스트 모드에 따라 base_url을 반환해 주자
        return ''

    def get_gi_url(self):
        return ''

    def get_logviewer_url(self):
        return ''

# class BEAPIInfo():


# class GWAPIInfo():

# class ISAPIInfo():

