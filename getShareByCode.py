#/usr/bin/python3
import sys
from urllib import request
import json

headers = {
	'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)',
	'Host': 'api-wows-wscn.xuangubao.cn'
}
def getShareCodeByName(shareName):
	searchReq = request.Request(url='http://api-wows-wscn.xuangubao.cn' + '/v3/search/stocks?q=' + shareName, headers=headers, method='GET')
	searchResponse = request.urlopen(searchReq)
	searchJson = json.loads(searchResponse.read().decode('utf-8'))
	return searchJson['data']['stocks']

def getShareStatusByCode(shareCode):
	curShareReq = request.Request(url='http://api-ddc-wscn.xuangubao.cn/market/real?fields=symbol,prod_name,prod_en_name,price_precision,px_change_rate,px_change,last_px&prod_code=' + shareCode, headers=headers, method='GET')
	curShareResponse = request.urlopen(curShareReq)
	curShareJson = json.loads(curShareResponse.read().decode('utf-8'))
	curShareSet = curShareJson['data']['snapshot']
################处理返回的结果#############################
	for curShareDot in curShareSet:
		print("%s %s" % (round(curShareSet[curShareDot][4], 2),curShareSet[curShareDot][6]))


argvLen = len(sys.argv)
for shareName in sys.argv[1:]:
	for searchJsonCode in getShareCodeByName(shareName):
		getShareStatusByCode(searchJsonCode['code'])

