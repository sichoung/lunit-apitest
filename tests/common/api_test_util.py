#-*- coding: utf-8 -*-
import os,sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


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
