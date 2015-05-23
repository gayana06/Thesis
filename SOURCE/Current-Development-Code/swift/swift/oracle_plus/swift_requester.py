__author__ = 'Gayana'

import swiftclient
from swift.oracle_plus.utility import log_oracle_plus
from swift.oracle_plus.config import CURRENT_IP
import sys
import traceback

class  SwiftRequester():
    user = 'test1:tester1'
    key = 'testing1'
    conn = swiftclient.Connection(
            user=user,
            key=key,
            authurl='http://'+str(CURRENT_IP)+':8085/auth/v1.0',
    )

    def resend_write(self,object_path,value):
        try:
            split=object_path.split("/")
            print(split)
            container=split[3]
            obj_name=split[4]
            log_oracle_plus("resend_write container = "+container+" Name = "+obj_name )
            #log_oracle_plus("New Content = "+value)
            self.resend_put(container,obj_name,value)
        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
            error=''.join('!! ' + line for line in lines)
            log_oracle_plus(error)

    def print_request_details(self,object_path,request):
        try:
            split=object_path.split("/")
            print(split)
            container=split[3]
            obj_name=split[4]
            log_oracle_plus("Container = "+container+" Name = "+obj_name )
            log_oracle_plus("Content"+str(request.environ['wsgi.input']))
            #content=request.environ['wsgi.input'].read()
            content="Test content"
            self.resend_put(container,obj_name,content)
        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
            error=''.join('!! ' + line for line in lines)
            log_oracle_plus(error)
        return  1

    def resend_put(self,container_name,obj_name,val):
        self.conn.put_object(container_name, obj_name,contents=val ,content_type=None)
        log_oracle_plus("Resent put successfully")

swiftrequester=SwiftRequester()

def get_swift_requester():
    return swiftrequester



