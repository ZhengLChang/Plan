#/usr/bin/python3
import sys
from urllib import request
import json
import requests

class Share(object):
  def __init__(self):
    self.headers  = {
	  'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)',
	  #'Host': 'api-wows-wscn.xuangubao.cn'
          'Host': 'api-ddc-wscn.xuangubao.cn',
    }
  def getShareCodeByName(self, shareName):
    searchResponse = requests.get(url='http://api-wows-wscn.xuangubao.cn' + '/v3/search/stocks?q=' + shareName, headers=self.headers)
    searchJson = json.loads(searchResponse.text)
    return searchJson['data']['stocks']

  def getShareStatusByCode(self, shareCode):
    curShareResponse = requests.get(url='https://api-ddc-wscn.xuangubao.cn/market/real?fields=symbol,prod_name,prod_en_name,price_precision,px_change_rate,px_change,last_px&prod_code=' + shareCode, headers=self.headers);

    #print(curShareResponse.text)
    curShareJson = json.loads(curShareResponse.text)
    curShareSet = curShareJson['data']['snapshot']
################处理返回的结果#############################
    for curShareDot in curShareSet:
      #print(curShareSet)
      print("%s %s" % (round(curShareSet[curShareDot][4], 2),curShareSet[curShareDot][6]))

if __name__ == '__main__':
  myshare = Share()
  argvLen = len(sys.argv)
  for shareName in sys.argv[1:]:
    for searchJsonCode in myshare.getShareCodeByName(shareName):
      myshare.getShareStatusByCode(searchJsonCode['code'])

