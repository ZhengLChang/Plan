import requests
import urllib
from urllib.parse import unquote
from urllib.parse import quote
import json
import traceback
import time
import gevent
from gevent import pool, monkey
monkey.patch_all()
gevent_pool = pool.Pool(50)


class Stock_Base(object):
    bad_news_keywords = ['暴跌', '暴雷']
    convertible_keywords = ["向不特定对象发行可转换公司债券"]
    stock_list_dict = {}
    def __init__(self):
        pass

    def get_stock_list(self, number=90000):
        try:
            if Stock_Base.stock_list_dict:
                return Stock_Base.stock_list_dict
            num = number
            if num <= 0:
                num = 90000

            query_str = "jQuery1124045799110120462316_1606530104662"
            headers = {
                "Host": "71.push2.eastmoney.com",
                "Connection": "keep-alive",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",
                "Accept": "*/*",
                "Referer": "http://quote.eastmoney.com/center/gridlist.html",
                "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7",
            }
            url = f"http://71.push2.eastmoney.com/api/qt/clist/get?cb={query_str}&pn=1&pz={num}&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&fid=f3&fs=m:0+t:6,m:0+t:13,m:0+t:80,m:1+t:2,m:1+t:23&fields=f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f22,f11,f62,f128,f136,f115,f152&_=1606530104691"
            res = requests.get(url, headers=headers)
            content = res.text.encode("utf-8") if isinstance(res.text, bytes) else res.text
            Stock_Base.stock_list_dict = json.loads(content[len(query_str) + 1:-2])
            return Stock_Base.stock_list_dict
        except Exception as err:
            print(f"[Exception] [get_stock_list] {traceback.format_exc()}")
        return {}

    def get_news(self, search_keyword):
        try:
            search_keyword_after_quote = quote(search_keyword)
            query_str = "jQuery112407775914653170029_1606528867863"
            headers = {
                "Host": "searchapi.eastmoney.com",
                "Connection": "keep-alive",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",
                "Accept": "*/*",
                "Referer": "http://so.eastmoney.com/Ann/s?keyword=%E9%95%BF%E6%B5%B7%E8%82%A1%E4%BB%BD",
                "Accept-Language": "zh-CN,zh",
            }
            url = f"http://searchapi.eastmoney.com/bussiness/Web/GetSearchList?type=401&pageindex=1&pagesize=10&keyword={search_keyword_after_quote}&name=normal&cb={query_str}&_=1606528867869"
            res = requests.get(url, headers=headers)
            content = res.text.encode("utf-8") if isinstance(res.text, bytes) else res.text
            return content[len(query_str) + 1:-1]
        except Exception as err:
            print(f"[Exception] [get_news {search_keyword}] {traceback.format_exc()}")
        return ""

    def _get_stock(self, search_keyword):
        try:
            headers = {
                "Host": "api-wows-wscn.xuangubao.cn",
                "User-Agent": "Mozilla/5.0 (Linux; Android 7.0; M3 Max Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/51.0.2074.203 Mobile Safari/537.36",
            }
            url = f"https://api-wows-wscn.xuangubao.cn/v3/search/stocks?q={search_keyword}"
            res = requests.get(url, headers=headers)
            content = res.text.encode("utf-8") if isinstance(res.text, bytes) else res.text
            return content
        except Exception as err:
            print(f"[Exception] [_get_stock {search_keyword}] {traceback.format_exc()}")
        return ""

    def get_stock(self, search_keyword): 
        try:
            stock_code_msg = self._get_stock(search_keyword)
            stock_code_msg_dict = json.loads(stock_code_msg)
            #print(stock_code_msg_dict)
            if stock_code_msg_dict["code"] != 20000:
                return None

            return stock_code_msg_dict["data"]["stocks"]
        except Exception as err:
            print(f"[Exception] [get_stock {search_keyword}] {traceback.format_exc()}")
        return {}

    def has_convertible_notes(self, search_keyword):
        for _ in range(3):
            try:
                notes = self.get_news(search_keyword)
                notes_dict = json.loads(notes)
                print(notes_dict)
                for data in notes_dict["Data"]:
                    for keywords in Stock_Base.convertible_keywords:
                        if keywords in data["NoticeTitle"]:
                            return True
            except Exception as err:
                print(f"[Exception] [has_convertible_notes {search_keyword}] {traceback.format_exc()}")
            time.sleep(1)
        return False

    def has_bad_news(self, search_keyword):
        try:
            notes = self.get_news(search_keyword)
            notes_dict = json.loads(notes)
            for data in notes_dict["Data"]:
                for keywords in Stock_Base.bad_news_keywords:
                    if keywords in data["NoticeTitle"]:
                        return True
        except Exception as err:
            print(f"[Exception] [has_bad_news {search_keyword}] {traceback.format_exc()}")
        return False

    def get_stocks_number(self):
        try:
            self.get_stock_list()
            #print(stock_list_str)
            #Stock_Base.stock_list_dict = json.loads(stock_list_str)
            return Stock_Base.stock_list_dict["data"]["total"]
        except Exception as err:
            print(f"[Exception] [get_stocks_number] {traceback.format_exc()}")
        return 0 

    def get_all_convertible(self):
        convertible_list = []
        try:
            self.get_stock_list()
            def empty_convertible_dict():
                convertible_dict = dict()
                stock_list = []
                for stock in Stock_Base.stock_list_dict["data"]["diff"]:
                    stock_name = stock["f14"]
                    convertible_dict[stock_name] = {
                        "stock_name": stock_name,
                        "is_convertible": False
                    }
                    stock_list.append(stock_name)
                return convertible_dict, stock_list

            def full_stock_convertible_status(convertible_dict, stock_name):
                #print(stock_name)
                if self.has_convertible_notes(stock_name):
                    print(convertible_dict[stock_name]["stock_name"])
                    convertible_dict[stock_name]["is_convertible"] = True
                else:
                    convertible_dict[stock_name]["is_convertible"] = False

            convertible_dict, stock_list = empty_convertible_dict()
            tasks = [gevent_pool.spawn(full_stock_convertible_status, convertible_dict, stock_name) for stock_name in stock_list]
            gevent.wait(tasks)
            
            for stock_key,stock_dict in convertible_dict.items():
                if stock_dict["is_convertible"]:
                    convertible_list.append(stock_dict["stock_name"])
        except Exception as err:
            print(f"[Exception] [get_stocks_number] {traceback.format_exc()}")
        return convertible_list

if __name__ == "__main__":
    obj = Stock_Base()
    #print(obj.get_stock_list())
    #print(obj.get_news(""))
    #print(obj.get_stock("zgpa"))
    #print(obj.has_convertible_notes("熊猫乳品"))
    print(obj.get_all_convertible())






