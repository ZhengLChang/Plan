import gevent
from gevent import pool, monkey
monkey.patch_all()
gevent_pool = pool.Pool(50)
import requests
import time
import json
import traceback
import re
import subprocess
import home_info 


class HomeList(object):
    def __init__(self):
        pass


    def GetHomeList(self):
        url = "https://dg.ke.com/ershoufang/$$INDEX$$rs%E9%95%BF%E5%AE%89%E8%8A%B1%E5%9B%AD/"

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
        home_list = list()
        for index_str in ["", "pg2", "pg3"]:
            replace_url = url.replace("$$INDEX$$", index_str)
            res = requests.get(url=replace_url, headers=headers)
            if res.status_code == 200:
                #with open("changan_" + index_str + ".txt", "w") as f:
                #    f.write(res.text.split("东莞二手房")[1])
                home_list1 = re.findall(r'https://dg.ke.com/ershoufang/\d{3,}.html', res.text.split("东莞二手房")[1])
                home_list = home_list + home_list1

        return set(home_list)



if __name__ == "__main__":
    obj = HomeList()
    home_set = obj.GetHomeList()
    #home_set = set(re.findall(r'https://dg.ke.com/ershoufang/\d{3,}.html', res_str))
    home_info_obj = home_info.HomeInfo()

    home_less_80_list = list()
    home_less_80_and_south_list = list()
    home_other_list = list()

    store_list = list()
    tasks = [gevent_pool.spawn(home_info_obj.GetHomeDesc, store_list, home_url) for home_url in home_set]
    gevent.wait(tasks)

    area_list = list()
    for home_info_dict in store_list:
        if home_info_dict["建筑面积"].startswith("7") or home_info_dict["建筑面积"].startswith("8") or home_info_dict["建筑面积"].startswith("6"):
            home_less_80_list.append(home_info_dict)
            area_list.append(home_info_dict["建筑面积"])
            if "南" in home_info_dict["房屋朝向"]:
                home_less_80_and_south_list.append(home_less_80_and_south_list)
        else:
            home_other_list.append(home_info_dict)
    print(area_list)
    print(f"< 80 个数: {len(home_less_80_list)}")
    print(f"< 80 且朝南个数: {len(home_less_80_and_south_list)}")
    print(f"> 80 个数: {len(home_other_list)}")
    '''
    for home_url in home_set:
        home_info_dict = home_info_obj.GetHomeDesc(home_url)
        if home_info_dict["建筑面积"].startswith("7"):
            home_less_80_list.append(home_info_dict)
        else:
            home_other_list.append(home_info_dict)
        
    print(f"< 80:{len(home_less_80_list)}")
    '''




