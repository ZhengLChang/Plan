var http = require("http");
var url = require("url");
var sqlObj = require("./sqlObj");
var sprintf = require("./sprintf.js");
var port = 80;
var path = require("path");
var fs = require("fs");


var server = http.createServer(function(req, res){
		var pathname = __dirname + url.parse(req.url).pathname;
		var body = "";
		var buffers = [];
		var nread = 0;
		req.on('data', function(chunk){
				try{
					body += chunk;
				}catch(err){
					console.log(err.message);
				}
				});
		req.on('end', function(){
				try{
				fs.exists(pathname, function(exists){
				if(exists){
					res.writeHead(200, {"Content-Type": "application/octet-stream"});
					fs.readFile(pathname, function(err, data){
							res.end(data);
						});
				}
				else{
					res.writeHead(200, {"Content-Type": "text/html; charset=utf8"});
					res.write('Hello, world');
					res.end();
					}
				});
				}catch(err){
					console.log(error.message);
					res.writeHead(200, {"Content-Type": "text/plain"});
					res.end('{"return_code": 0,"return_prompt": "Success"}');
				}
				});
		req.on('error', function(err){
				console.log(err.message);
				});
		}).listen(80);
