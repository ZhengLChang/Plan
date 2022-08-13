import requests
import time
import json
import traceback
import matplotlib.pyplot as plt
import re
import subprocess


class HomeInfo(object):
    s = requests.Session()
    def __init__(self):
        pass


    def GetHomeDesc(self, store_list, url):
        headers = {
            "Host": "dg.ke.com",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:94.0) Gecko/20100101 Firefox/94.0",
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
            "Accept-Encoding": "gzip, deflate, br",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "X-Requested-With": "XMLHttpRequest",
            "Origin": "https://m.fang.com",
            "Connection": "keep-alive",
            "Referer": "https://m.fang.com/xiaoqu/weekreport/dg/2819457622.html",
            "Cookie": "csrfToken=bQcGC0zngCOHBwjAJA_Xr1ZG; global_wapandm_cookie=4tdaj1pvtx2jyw4n5e085goi52yl3fdj4ut; unique_wapandm_cookie=U_4tdaj1pvtx2jyw4n5e085goi52yl3fdj4ut*3; g_sourcepage=esf_xqhqzb%5Exq_wap",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "TE": "trailers",
        }
        res_dict = {
            "建筑面积": "",
            "房屋朝向": "",
            "所在楼层": ""
        }
        res = self.s.get(url=url, headers=headers)
        if res.status_code == 200:
            res_dict["建筑面积"] = re.findall(r"建筑面积</span>([^<]*)", res.text)[0]
            res_dict["房屋朝向"] = re.findall(r"房屋朝向</span>([^<]*)", res.text)[0]
            res_dict["所在楼层"] = re.findall(r"所在楼层</span>([^<]*)", res.text)[0]

        store_list.append(res_dict)
        
if __name__ == "__main__":
    home_info_obj = HomeInfo()
    home_info_obj.GetHomeDesc("https://dg.ke.com/ershoufang/105108510511.html")

