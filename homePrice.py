import requests
import time
import json
import mail
import traceback
import matplotlib.pyplot as plt
import re
import subprocess


class homePrice(object):
    def __init__(this):
        pass
    def GetRecentPrice(this):
        url = "https://m.fang.com/fangjia/zhoushiXiaoquAjax/"

        headers = {
            "Host": "m.fang.com",
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

        post_data = {"searchtype":"2",
            "timetype":"3",
            "cityname":"%E4%B8%9C%E8%8E%9E",
            "newcode":"2819457622",
            "comarea":"%E4%B9%8C%E6%B2%99",
            "district":"%E9%95%BF%E5%AE%89",
            "FANG_CSRF":"bQcGC0zngCOHBwjAJA_Xr1ZG",
        }
        res = requests.post(url=url, headers=headers, data=post_data)
        if res.status_code == 200:
            try:
                res_dic = json.loads(res.text)
                return True, res_dic
            except Exception as err:
                return False, traceback.format_exc()
    def GetNowStat(this):
        headers = {
            "Host": "dg.ke.com",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:94.0) Gecko/20100101 Firefox/94.0",
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
            "Accept-Encoding": "gzip, deflate, br",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "X-Requested-With": "XMLHttpRequest",
            "Connection": "keep-alive",
            "Referer": "https://dg.ke.com/",
            "Cookie": "lianjia_uuid=2388fddb-00f3-48c2-827c-07117621d48d; lianjia_ssid=0ab009d1-bcfa-4609-a9ad-ad241af408dd; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22178781c4d71aee-0b152bb523d5ba-33697709-1024000-178781c4d72a23%22%2C%22%24device_id%22%3A%22178781c4d71aee-0b152bb523d5ba-33697709-1024000-178781c4d72a23%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_utm_source%22%3A%22baidu%22%2C%22%24latest_utm_medium%22%3A%22pinzhuan%22%2C%22%24latest_utm_campaign%22%3A%22wyguangzhou%22%2C%22%24latest_utm_content%22%3A%22biaotimiaoshu%22%2C%22%24latest_utm_term%22%3A%22biaoti%22%7D%7D; select_city=441900; Hm_lvt_9152f8221cb6243a53c83b956842be8a=1653487230; Hm_lpvt_9152f8221cb6243a53c83b956842be8a=1653487230; srcid=eyJ0Ijoie1wiZGF0YVwiOlwiNDlmZjVjYWNlNmQ5YTFjMWVkZGJlMjVkODE1N2NlZDUxMjk2YmRkMjgwNjc5YTEwYmE1YTdlYmU1NjI4M2IyYTc5MzE5MWZiNTIyZTA5ZGQyM2FiNWVjZmRiZWFlMzkwY2NkNzJjYzljNDE5YTQ1ZWE4ZTAzZDRhMzMzMTI3MTA0M2MwM2NkZDgzNDEzZTk2MjYyMjBhZGZlOThiYjZmMDJlMGIzYmE0ODg5MzFlMmY1OTFkYzZkNzY0MDBkODBhZjUwNzQ3M2IwMGFlNWU4OTliMDU1YTM1OTMyZjBlNzJjOWRiOWVmZjZjOTE3MzE1ZDIzMDQyNTg4NzBiODJkM1wiLFwia2V5X2lkXCI6XCIxXCIsXCJzaWduXCI6XCJmY2QwOGM0NlwifSIsInIiOiJodHRwczovL2RnLmtlLmNvbS8iLCJvcyI6IndlYiIsInYiOiIwLjEifQ==",
            "sec-ch-ua": '" Not A;Brand";v="99", "Chromium";v="101", "Google Chrome";v="101"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"macOS"',
        }
        try:
            res = requests.get("https://dg.ke.com/xiaoqu/rs%E9%95%BF%E5%AE%89%E8%8A%B1%E5%9B%AD/", headers=headers)
            if res.status_code == 200:
                totalSellCount = [m.strip() for m in re.findall(r'(.*totalSellCount.*)', res.text)]
                totalPrice = [m.strip() for m in re.findall(r'(.*totalPrice.*)', res.text)]

                return True, totalSellCount + totalPrice
        except Exception as err:
            return False, [traceback.format_exc()]
     
    def GetPricePicture(this, priceDict, priceName):
        try:
            subprocess.getoutput(f"rm -rf {priceName}")
            month_row = [] 
            price_line = []
            max_price = (0, 0)
            min_price = (10000000, 100000000)
            buy_price = (0, 0)
            for dat in priceDict["data"]["fangjianewcode"]:
                price = dat["price"]
                month = dat["month"]
                if price > max_price[1]:
                    max_price = (month, price)
                if price < min_price[1]:
                    min_price = (month, price)
                if month == '2020.06':
                    buy_price = (month, price)
                month_row.append(month)
                price_line.append(price)

            plt.plot(month_row, price_line, linestyle="-")
            plt.text(month_row[-1], price_line[-1], f"{price_line[-1]}");

            if max_price[0] != 0:
                plt.text(max_price[0], max_price[1], f"{max_price[0]}, {max_price[1]}");

            if min_price[0] != 0 and max_price[0] != min_price[0]:
                plt.text(min_price[0], min_price[1], f"{min_price[0]}, {min_price[1]}");

            if buy_price[0] != 0:
                print(f"buy {buy_price[0]}, {buy_price[1]}")
                plt.text(buy_price[0], buy_price[1], f"buy {buy_price[0]}, {buy_price[1]}");

            #plt.axis([month_row[0], month_row[-1]])
            plt.xticks(month_row)
            plt.savefig(f"{priceName}")
            return True, [f"{price}"]
        except Exception as err:
            return False, [traceback.format_exc()]

    def DumpMail(this):
        retCode, priceDict = this.GetRecentPrice()
        retCode, nowStatArr = this.GetNowStat()
        retCode, priceMsg = this.GetPricePicture(priceDict, "1.jpg")
        if retCode:
            mail.sentemailPic('Home Msg', nowStatArr + priceMsg,  ["1.jpg"])
        else:
            mail.sentemail('Home Msg', nowStatArr + priceMsg)



if __name__ ==  "__main__":
    homeObj = homePrice()
    homeObj.DumpMail()
    '''
    print(homeObj.GetRecentPrice())
    print(homeObj.GetNowStat())
    '''


