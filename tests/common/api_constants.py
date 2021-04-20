import os,sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class LogViewerConstants():
    #### USERS ####
    signup_api_path = "/users/signup"
    login_api_path = "/users/login"
    chgpw_api_path = "/users/change-password"
    refreshtkn_api_path = "/users/refresh"
    verifytkn_api_path = "/users/verify"

    #### COMMON ####
    getcomponent_api_path = "/api/v1/commons/components"
    getloglevel_api_path = "/api/v1/commons/log-level"
    getlogtype_api_path = "/api/v1/commons/log-types"
    getlogstatus_api_path = "/api/v1/commons/log-status"
    getservicehost_api_path = "/api/v1/hosts"

    gethealthcheck_api_path = "/health"
    getserverinfo_api_path = "/configurations"

    #### LOGS ####
    getloglist_api_path = "/api/v1/logs"
    logupload_api_path ="​/api​/v1​/logs"
    logdownload_api_path = "/api/v1/logs/download"

    #### ACCOUNT ####
    test_email = "qe_test2@lunit.io"
    test_pw = "1q2w3e4r%t"
    test_name = "apitest user"
#     test_name = "apitest user"
# test_email = "qe_test@lunit.io"
# test_pw = "1q2w3e4r%t"


class BEConstants():
    getcomponent_api_path = "/api/v1/commons/components"
    getloglevel_api_path = "/api/v1/commons/log-level"
    getlogtype_api_path = "/api/v1/commons/log-types"
    getlogstatus_api_path = "/api/v1/commons/log-status"
# class InferenceServerConstants():


