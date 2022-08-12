import requests
import time
import json
import mail
import traceback
import matplotlib.pyplot as plt
import subprocess
import lianjia


subprocess.getoutput("rm -rf 1.jpg")
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
changanhuaStat = lianjia.GetChanganStat()
res = requests.post(url=url, headers=headers, data=post_data)
if res.status_code == 200:
    try:
        res_dic = json.loads(res.text)
        month_row = [] 
        price_line = []
        max_price = (0, 0)
        min_price = (10000000, 100000000)
        buy_price = (0, 0)
        for dat in res_dic["data"]["fangjianewcode"]:
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
        plt.savefig("1.jpg")
        mail.sentemailPic('mail subject', changanhuaStat + [price], ["1.jpg"])
    except Exception as err:
        mail.sentemail('mail subject fail', changanhuaStat + [price, traceback.format_exc()])
        
else:
    mail.sentemail('mail subject', changanhuaStat + [res.status_code])
#print(json.loads(res.text))


