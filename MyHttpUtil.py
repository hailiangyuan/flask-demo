#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/05/06 15:12
# @Author  : faker
# @Site    :  http 工具类
# @File    : MyHttpUtil.py
# @Software: PyCharm
import requests
import json

corn_list_url = "http://47.92.23.82:9993/phoenix/livePreview/0_ZL4/all/all/all"
corn_add_url = "http://yunweicai.com"
corn_delete_url = "http://yunweicai.com"
test_corn = [{"imei": 0, "corn": "test1Corn"}, {"imei": 1, "corn": "test2Corn"}]


class MyUtil(object):

    @staticmethod
    def corn_list():
        # list = requests.get(corn_list_url)
        # result_json = list.text
        # data = json.loads(result_json)
        # return data["data"][0]
        return test_corn

    @staticmethod
    def corn_find(imei):
        print("查询imei:"+str(imei))
        size = len(test_corn)
        if imei < size:
            print("index:"+str(imei))
            return test_corn[imei]
        # list = requests.get(corn_list_url)
        # result_json = list.text
        # data = json.loads(result_json)
        # return data["data"][0]
        print("下标越界！返回第一个")
        return test_corn[0]

    @staticmethod
    def corn_add(imei, corn):
        print("imei:" + str(imei))
        print("corn:" + str(corn))
        # 发送post请求，带json串
        json_data = {"imei": imei, "corn": corn}
        size = len(test_corn)
        test_corn.insert(size, json_data)
        print("增加之后的cornList:" + str(len(test_corn)))
        # r11 = requests.post(corn_add_url, json=json_data)
        return True

    @staticmethod
    def corn_delete(imei):
        test_corn.pop(imei)
        # 发送post请求，带json串
        # json_data = {"imei": imei}
        # r11 = requests.post(corn_delete_url, json=json_data)

        # // todo 记得修改
        return True

    @staticmethod
    def corn_updete(imei, corn):
        json_data = {"imei": imei, "corn": corn}
        test_corn.remove(test_corn[imei])
        test_corn.append(json_data)
        # 发送post请求，带json串
        # json_data = {"imei": imei}
        # r11 = requests.post(corn_delete_url, json=json_data)

        # // todo 记得修改
        return True


