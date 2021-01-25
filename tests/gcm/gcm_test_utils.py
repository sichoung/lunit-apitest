
#-*- coding: utf-8 -*-
import requests
import json

def get_gcm_token(url, api_path, email_id, passwd):
    headers = {'Content-Type': 'application/json'}
    payload = {'email': email_id, 'password': passwd}
    response = requests.post(url + api_path, headers=headers,
                            data=json.dumps(payload, indent=4))
    if response.status_code == 200:
        response_body = response.json()
        return str(response_body["key"])
    else:
        return None