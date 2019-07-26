#/usr/bin/python3
import sys
from urllib import request
import json
import redis
import time

class Share(object):
	def __init__(self):
		self.redis_cli = redis.Redis(host='127.0.0.1', password='')
		self.headers = {
			'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)',
			'Host': 'api-wows-wscn.xuangubao.cn'
		}
		self.initCodeMap = {'szzs': '000001.SS', 'dhgf': '002236.SZ', 'dh': '002236.SZ'}
		self.isExist = 0

	def exit(self):
		return self.isExist

	def getShareCodeByName(self, shareName):
		try:
			if self.initCodeMap[shareName]:
				return [{'code': str(self.initCodeMap[shareName]), 'prod_name': ''}]
		except Exception as err:
			pass
		searchReq = request.Request(url='http://api-wows-wscn.xuangubao.cn' + '/v3/search/stocks?q=' + shareName, headers=self.headers, method='GET')
		searchResponse = request.urlopen(searchReq)
		searchJson = json.loads(searchResponse.read().decode('utf-8'))
		return searchJson['data']['stocks']

	def getShareStatusByCode(self, shareName, shareCode):
		curShareReq = request.Request(url='http://api-ddc-wscn.xuangubao.cn/market/real?fields=symbol,prod_name,prod_en_name,price_precision,px_change_rate,px_change,last_px&prod_code=' + shareCode, headers=self.headers, method='GET')
		curShareResponse = request.urlopen(curShareReq)
		curShareJson = json.loads(curShareResponse.read().decode('utf-8'))
		curShareSet = curShareJson['data']['snapshot']
################处理返回的结果#############################
		for curShareDot in curShareSet:
			self.redis_cli.sadd('result_list', '{shareName}_{price}_{percent}'.format(shareName=shareName, price=curShareSet[curShareDot][6], percent=round(curShareSet[curShareDot][4], 2)))
#			print("%s %s" % (round(curShareSet[curShareDot][4], 2),curShareSet[curShareDot][6]))
	def clearRedisResultSet(self):
		self.redis_cli.delete("result_list")
	def getCodeSet(self):	
		return set(self.redis_cli.smembers("shareCodeSet"))

if __name__ == "__main__":
	share = Share()
	while not share.exit():
		shareCodeSet = share.getCodeSet()
		for shareCodeNode in shareCodeSet:
			for searchJsonCode in share.getShareCodeByName(shareCodeNode.decode()):
				share.getShareStatusByCode(shareCodeNode.decode(), searchJsonCode['code'])

		time.sleep(10)














