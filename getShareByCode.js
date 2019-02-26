var http = require('http');
var https = require('https');
var hostName = 'api-ddc.wallstreetcn.com';

function getCurrentDataFromCode(code){
  console.log(code);
  /*
  var share_message = JSON.parse(resData);
  var i = 0, mes_arr_len = share_message.data.items.length;
  var msg_arr = share_message.data.items;
  for(i = 0; i < mes_arr_len; i++){
    if(msg_arr[i].market_type == "mdc"){
      getCurrentDataFromCode(msg_arr[i].wscn_code);
    }
  }
  */
}
/*
function getResultInput(abbreviation){
  try{
    var req = http.request({hostname: hostName,
                            port: 80,
                            path: '/search/assets?q='+abbreviation,
                            method: 'GET'},
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
          var share_message = JSON.parse(resData);
          var i = 0, mes_arr_len = share_message.data.items.length;
          var msg_arr = share_message.data.items;
          for(i = 0; i < mes_arr_len; i++){
            if(msg_arr[i].market_type == "mdc"){
              getCurrentDataFromCode(msg_arr[i].wscn_code);
            }
          }
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
*/

function sendRequestToHost(option){
  var hostname = option.hostname,
      port = option.port,
      path = option.path,
      method = option.method,
      callback = option.callback;
  if(!hostname || !callback){
    console.log("hostname or callback cannot by empty!!!");
    return false;
  }
  if(!port) port = 80;
  if(!method) method = 'GET';
  try{
    var req = http.request({"hostname": hostname,
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

sendRequestToHost({hostname: hostName,
                            port: 80,
                            path: '/search/assets?q='+'pinganyinhang',
                            method: 'GET',
                            callback: 
function(resData){
  var share_message = JSON.parse(resData);
  var i = 0, mes_arr_len = share_message.data.items.length;
  var msg_arr = share_message.data.items;
  for(i = 0; i < mes_arr_len; i++){
    if(msg_arr[i].market_type == "mdc"){
        sendRequestToHost({hostname: hostName,
                            port: 80,
                            path: '/market/real?fields=symbol,prod_name,prod_en_name,price_precision,px_change_rate,px_change,last_px&prod_code=' + msg_arr[i].wscn_code,
                            method: 'GET',
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
                          console.log(msg_arr[index][4].toFixed(2) + " " + msg_arr[index][6]);
                        }
                      }
                  });
    }
  }
}});
