#/usr/bin/python3
import sys
from urllib import request
import json

class Share(object):
  def __init__(self):
    self.headers  = {
	  'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)',
	  'Host': 'api-wows-wscn.xuangubao.cn'
    }
  def getShareCodeByName(self, shareName):
    searchReq = request.Request(url='http://api-wows-wscn.xuangubao.cn' + '/v3/search/stocks?q=' + shareName, headers=self.headers, method='GET')
    searchResponse = request.urlopen(searchReq)
    searchJson = json.loads(searchResponse.read().decode('utf-8'))
    return searchJson['data']['stocks']

  def getShareStatusByCode(self, shareCode):
    #print(shareCode)
    curShareReq = request.Request(url='http://api-ddc-wscn.xuangubao.cn/market/real?fields=symbol,prod_name,prod_en_name,price_precision,px_change_rate,px_change,last_px&prod_code=' + shareCode, headers=self.headers, method='GET')
    curShareResponse = request.urlopen(curShareReq)
    curShareJson = json.loads(curShareResponse.read().decode('utf-8'))
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

