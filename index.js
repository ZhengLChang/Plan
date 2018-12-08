var http = require("http");
var url = require("url");
var sqlObj = require("./sqlObj");
var sprintf = require("./sprintf.js");
var port = 8080;

var server = http.createServer(function(req, res){
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
					res.writeHead(200, {"Content-Type": "text/html; charset=utf8"});
					res.write('<!DOTTYPE html>');
					res.write('<html>');
					res.write('<head>');
					res.write('<meta charset=utf-8">');
					res.write(sprintf.sprintf(['<style>',
								'label{',
								'display: inline-block;',
								'width: 260px;',
								'margin: 10px 10px;',
								'}',
								'</style>'].join('')));
					res.write('</head>');
					res.write('<body>');
					sqlObj.queryAll('select * from plan where `index` >= 4', function(err, row){
							row.forEach(function(row){
							res.write(sprintf.sprintf(['<div>',
									'<label>%s</label>',
									'<label>%s</label>',
									'<label>%s</label></div>'].join(''), 
									row.trigger_date, 
									row.subject, 
									row.data));

									});
							res.write('</body>');
							res.write('</html>');
							res.end();
							//console.log(row.trigger_date);
							/*
									*/
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
		}).listen(8080);
