# -*- coding: utf-8 -*-
import psycopg2
import traceback

class BEDBManager():
    """ 
    """
    target_host = None # "10.220.150.115"
    target_port =  None # "5433"
    user_id =  None # "lunit"
    user_pw =  None # "lunitinsight"
    db_name =  None # "insight_backend"

    def __init__(self, host, port, db_id, db_pw, db_name):
        self.target_host = host
        self.target_port = port
        self.user_id = db_id
        self.user_pw = db_pw
        self.db_name = db_name
        self.conn = self.__connect()

    def teardown(self):
        if self.conn:
            self.conn.close()
            self.conn = None

    def __connect(self):
        return psycopg2.connect(host=self.target_host, port=self.target_port, dbname=self.db_name,
                                user=self.user_id, password=self.user_pw)

    

    def update_cxr3_info(self, host, port):
        self.__update_db_info(host,port, 'cxr-v3')

    def update_mmg_info(self, host, port):
        self.__update_db_info(host,port, 'mmg')

    def __update_db_info(self, host, port, product):
        """ DB key 값으로 할까.. cxr-v3 값으로 할까... """
        query_string = "UPDATE insight_inferenceserver SET host ='{}' , port ={} WHERE inference_model_id = (select a.id FROM insight_inferencemodel a, insight_app b WHERE a.app_id = b.id and b.name = '{}');".format(host, port, product)
        try:
            if not self.conn:
                self.conn = self.__connect()
            cur = self.conn.cursor()
            cur.execute(query_string)
            self.conn.commit()
        except Exception:
            msg = traceback.format_exc()
            msg += '\n\n Query: \n' + query_string
            print(msg)
            return -1
        finally:
            cur.close()
        return 1 # Not Found

    def __get_db_info(self, product):
        query_string = "SELECT a.id, a.host, a.port, c.name, b.tag FROM insight_inferenceserver a, insight_inferencemodel b, insight_app c where a.inference_model_id = b.id and b.app_id = c.id and c.name = '{}';".format(product)
        if not self.conn:
            self.conn = self.__connect()
        cur = self.conn.cursor()
        try:
            cur.execute(query_string)
            result = cur.fetchall()
            if(len(result) == 1):
                return result[0]
                # db_key = record[0]
                #     app_name = record[3] 
                #     app_tag = record[4] 
                #     is_host = record[1] 
                #     is_port = record[2]
            else:
                raise Exception("query result is not 1 but -"+len(result))
                # return None
        except Exception:
            msg = traceback.format_exc()
            msg += '\n\n Query: \n' + query_string
            print(msg)
        finally:
            cur.close()
        return None # Not Found

    def get_cxr3_info(self):
        """ will return is cxr-v3 server info as list type - (db_key, host, port, app_name, tag) (eg.(1, 10.10.10.10, 7777, cxr-v3, latest))
        """
        return self.__get_db_info('cxr-v3')

    def get_mmg_info(self):
        """ will return is mmg server info as list type - (db_key, host, port, app_name, tag) (eg.(1, 10.10.10.10, 7777, mmg, latest))
        """
        return self.__get_db_info('mmg')


# if __name__ == '__main__':
#     get_inference_server_info()