var http = require('http');
var https = require('https');
var hostName = 'api-ddc.wallstreetcn.com';

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
sendRequestToHost({hostname: hostName,
                            port: 443,
                            path: '/search/assets?q='+args[i],
                            method: 'GET',
                            isUseHttps: 1,
                            callback: 
function(resData){
  var share_message = JSON.parse(resData);
  var i = 0, mes_arr_len = share_message.data.items.length;
  var msg_arr = share_message.data.items;
  for(i = 0; i < mes_arr_len; i++){
    if(msg_arr[i].market_type == "mdc" &&
        msg_arr[i].asset_type == "stock"){
        //console.log(msg_arr[i]);
        sendRequestToHost({hostname: hostName,
                            port: 443,
                            path: '/market/real?fields=symbol,prod_name,prod_en_name,price_precision,px_change_rate,px_change,last_px&prod_code=' + msg_arr[i].wscn_code,
                            method: 'GET',
                            isUseHttps: 1,
                            callback: 
                function(resData){
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
                         // console.log(msg_arr[index][1] + msg_arr[index][4].toFixed(2) + " " + msg_arr[index][6]);
                         console.log(msg_arr[index][4].toFixed(2) + " " + msg_arr[index][6]);
                        }
                      }
                  });
    }
  }
}});
}
