#!/usr/bin/env python
# -*- coding: cp936 -*-

import json
import requests
from common.data_processing import data_processing


class function():
    def post(self,url,data):
        db=data_processing()
        data1=db.encrypt(data)#加密
        header={"Content-Type":"application/json"}
        re=requests.post(url,data=data1,headers=header)
        response=re.text
        dict=json.loads(response)#将unicode转为字典
        result=db.decrypt(dict)       #解密
        print(result)


#data={"params": "Ly+WfsOYZTosk8qQUHYyHIoDk4lpuHW8mTAsFtwNLJFZqio1ceZVtdbR3APsFsV2nVpqI+Bxa7qX\r\nR8ZAmzKDmtpdRkc4ZyDBCxtV8OUMMyXH0q/etILFdVHpXU6s3j8krleAjzlmY1rSiiQ9GL5jL/C1\r\nR2rsEcIKC7YdgqMh0S8=\r\n"}
url = "http://yzjtest.uicredit.cn/yzj-inner-api/innerApi/payment/getOverdueOrderInfo"
data={
    "params":{
           "orderId":"20180207101404206137254"
     }
}
f=function()
f.post(url,data)
