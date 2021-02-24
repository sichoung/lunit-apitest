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

    #### LOGS ####
    getloglist_api_path = "/api/v1/logs"
    logupload_api_path ="​/api​/v1​/logs"

    #### ACCOUNT ####
    test_email = "test@lunit.io"
    test_pw = "test"
    test_name = "apitest user"


# class BackendConstants():

# class InferenceServerConstants():


