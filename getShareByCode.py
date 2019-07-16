#/usr/bin/python3
import sys
from urllib import request
import json

headers = {
	'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)',
	'Host': 'api-wows-wscn.xuangubao.cn'
}
argvLen = len(sys.argv)
for codeName in sys.argv[1:]:
##############根据传入名称，得到对应代码#######################
	searchReq = request.Request(url='http://api-wows-wscn.xuangubao.cn' + '/v3/search/stocks?q=' + codeName, headers=headers, method='GET')
	searchResponse = request.urlopen(searchReq)
	searchJson = json.loads(searchResponse.read().decode('utf-8'))
#	print(type(searchJson['data']['stocks']))
################遍历结果集##############################
	for searchJsonCode in searchJson['data']['stocks']:
		curShareReq = request.Request(url='http://api-ddc-wscn.xuangubao.cn/market/real?fields=symbol,prod_name,prod_en_name,price_precision,px_change_rate,px_change,last_px&prod_code=' + searchJsonCode['code'], headers=headers, method='GET')
		curShareResponse = request.urlopen(curShareReq)
		curShareJson = json.loads(curShareResponse.read().decode('utf-8'))
		
		curShareSet = curShareJson['data']['snapshot']
################处理返回的结果##############################
		for curShareDot in curShareSet:
			print("%s %s" % (round(curShareSet[curShareDot][4], 2),curShareSet[curShareDot][6]))


