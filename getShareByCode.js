var http = require('http');
var https = require('https');
//var hostName = 'api-ddc.wallstreetcn.com';
var hostName = 'api-ddc-wscn.xuangubao.cn';
var shareNameToCode = new Map();
shareNameToCode.set('szzs', '000001.SS');
shareNameToCode.set('sh', '000001.SS');
shareNameToCode.set('szcz', '399001.SZ');
shareNameToCode.set('sz', '399001.SZ');
function sendRequestToHost(option){
  var hostname = option.hostname,
      port = option.port,
      path = option.path,
      method = option.method,
      isUseHttps = option.isUseHttps,
      callback = option.callback;
  if(!hostname || !callback){
    console.log("hostname or callback cannot by empty!!!");
    return false;
  }
  if(!port) port = 80;
  if(!method) method = 'GET';
  try{
    var httpReqest = null;
    if(isUseHttps){
      httpReqest = https;
    }else{
      httpReqest = http;
    }

    var req = httpReqest.request({"hostname": hostname,
                            "port": port,
                            "path": path,
                            "method": 'GET'},
      function(res){
        var resData = '';
        res.setEncoding('utf8');
        res.on('data', function(chunk){
          resData += chunk;
          });
        res.on('end', function(err){
          if(err){
            console.log(err.message);
            req.end();
            return;
          }
          callback(resData);
        });
        res.on('error', function(err){
          console.log(err.message);
          req.end();
          });
        res.on('timeout', function(err){
          console.log(err.message);
          })
        req.end();
      });
  }catch(err){
    console.log(err);
  }
  req.on('error', function(err){
      console.log(err.message);
      });
  req.on('timeout', function(err){
      console.log(err.message);
      });
  req.end();

}

var args = process.argv.splice(2);
for(var i = 0; i < args.length; i++){
	if(shareNameToCode.get(args[i].toLowerCase())){
		getSharePriceByCode(shareNameToCode.get(args[i].toLowerCase()));
		continue;
	}
	sendRequestToHost({hostname: 'api-wows-wscn.xuangubao.cn',
			port: 80,
			path: '/v3/search/stocks?q='+args[i],
			method: 'GET',
			//        isUseHttps: 1,
			callback: 
			function(resData){
			var share_message = JSON.parse(resData);
			var i = 0, mes_arr_len = share_message.data.stocks.length;
			var msg_arr = share_message.data.stocks;
			for(i = 0; i < mes_arr_len; i++){
			if(1 || msg_arr[i].market_type == "mdc" &&
					(msg_arr[i].asset_type == "stock" || msg_arr[i].asset_type == "index")){
			//console.log(msg_arr[i]);
				getSharePriceByCode(msg_arr[i].code);
			}
			}
		}});
}

function getSharePriceByCode(code){
	sendRequestToHost({hostname: hostName,
			port: 80,
			path: '/market/real?fields=symbol,prod_name,prod_en_name,price_precision,px_change_rate,px_change,last_px&prod_code=' + code,
			//path: '/market/trend?fields=tick_at,close_px,avg_px,turnover_volume,turnover_value,open_px,high_px,low_px,px_change,px_change_rate&prod_code=' + "000001.ss",
			method: 'GET',
			//       isUseHttps: 1,
			callback: shareCodeRequestProc,
			});
}

function shareCodeRequestProc(resData){
	var share_message = JSON.parse(resData);
	var msg_arr = null;
	var fields = null;
	if(share_message.message != "OK"){
		console.log(share_message);
		console.log("Request Error");
		return false;
	}
	fiels = share_message.data.fields;
	msg_arr = share_message.data.snapshot;
	for(var index in msg_arr){
		//console.log(msg_arr[index][1] + msg_arr[index][4].toFixed(2) + " " + msg_arr[index][6]);
		console.log(msg_arr[index][4].toFixed(2) + " " + msg_arr[index][6].toFixed(2));
	}
}
