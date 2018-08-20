#!/usr/bin/python
# -*- coding:UTF-8 -*-
# @Time     : 17:31
# @Author   :RNone

import os
import json

class data_processing():
    def encrypt(self,data):
        '''加密数据'''
        data1=json.dumps(data).replace(' ', '').replace('\"', '\\\"')  # 字典转化JSON，并将转换后的空格符去除
        #print("encrypt:",self.__data_processing(1,data1).split('======>')[1])
        #print(self.__data_processing(1,data1))
        return self.__data_processing(1,data1).split('======>')[1]
    def decrypt(self,data):
        '''解密数据'''
        data1 = json.dumps(data).replace(' ', '').replace('\"', '\\\"')
        #print("decrypt:", self.__data_processing(2, data1).split('======>')[1])

        return self.__data_processing(2,data1).split('======>')[1]
    def __data_processing(self,mode,data):
        '''
        数据处理
        :param mode: 处理模式，1为加密，2为解密
        :param data: 需要处理的原始数据
        :return: 处理后的数据
        '''
        result = os.popen('java -jar RSA.jar %s %s'%(mode,data))
        dataOut = result.read()
        return dataOut

if __name__ == '__main__':
    dp = data_processing()  #实例化数据处理对象
    #加密数据
    #data = {"params":"2f46ec886b4e028ec14e7e1985dbb5"}  #需要加密的数据样本
    data={
 "params":{
          "orderId":"8888888888888888",
          "installNums":[1,2,3],
           "page":{
                   "page":1,
                   "rows":10
           }
 }
}
    dataOut = dp.encrypt(data)  #调用加密函数，dataOut就是加密后的数据
    print(dataOut)
    #解密数据
    #解密样本数据
    #data1 = {"message": "查询成功！","code": "0000","info": "vfDMa7jNd0MFTVcqo7hQVLKRWarx2JgtoJ9omtU1vWvosH3oknNQoyGPggAb9W/quSfjimR1X1pFxHO2aBq2JevrNonR4iQhMDEfalce9T2ndTPG1BRHA5+P0ndlt09/kIkOKQM9sl2fAT4/Rtk2r/WJSgYH3B1ZL5mBRSxMQEs="}
    #dataOut = dp.decrypt(data1)  #调用解密函数，dataOut就是解密后的数据
    #print(dataOut)
