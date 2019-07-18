var nodemailer = require("nodemailer");
var http = require('http');
var sqlite3 = require('sqlite3');
/**/
var mailOptions = {
  from: '13007568302@163.com',
  to: '13007568302@163.com, 779220717@qq.com',
//	to: '13007568302@163.com',
  subject: 'Hello',
  html: 'Hello, World',
  index: 0
};

var db = new sqlite3.Database('./plan.db', sqlite3.OPEN_READWRITE, function(err){
	if(err){
		console.log(err.message);
	}
});
/*
var mysql = require('mysql');
var mysqlConn = mysql.createConnection({
host: '127.0.0.1',
user: 'root',
password: 'zheng',
database: 'day_job',
timezone: 'Asia/Shanghai'
    });
mysqlConn.connect();
*/

var mailTrans = nodemailer.createTransport({
service: '163',
auth: {
  user: '13007568302@163.com',
  pass: '13073shanguangy'
}
    });

function sendMailByPlan(){
	db.each("select * from plan where (trigger_date <= datetime('now', 'localtime') and isSent = 0 and isDaily = 0) or (isDaily = 1 and strftime('%H', `trigger_date`) = strftime('%H', datetime('now', 'localtime')) and abs(strftime('%M', `trigger_date`) - strftime('%M', datetime('now', 'localtime'))) < 2)", [], function(err, result){
       var myOptions = mailOptions;
        myOptions.subject = result["subject"];
        myOptions.html = result["data"];
        myOptions.index = result["index"];
        mailTrans.sendMail(myOptions, function(error, info){
          if(error){
            console.log(error);
          }else{
         }
      });
	var mysqlQuery = "update plan set isSent = 1 where plan.`index`=" + myOptions.index;
	console.log(mysqlQuery);
        db.each(mysqlQuery/*"update plan set isSent = 1 where plan.`index`=" + myOptions.index*/, [], function(err, info){;
		if(err){
			console.log(err.message);
		}
	})
	});
}

function printNewShare(newShare)
{
  var myOptions = mailOptions;
  myOptions.subject = "资讯";
  myOptions.html = "即将发行: </br>" + newShare;
  myOptions.index = 0;
  mailTrans.sendMail(myOptions, function(error, info){
      if(error){
      console.log(error);
      }else{
      }
   });
}

function getNewShareNearToday(nearDay, callbackFunc)
{
  var nowDate = new Date(Date.now());
  var options = {
    hostname: 'dcfm.eastmoney.com',
    port: 80,
    path: '/em_mutisvcexpandinterface/api/js/get?type=XGSG_LB&token=70f12f2f4f091e459a279469fe49eca5&st=purchasedate,securitycode&sr=-1&p=1&ps=50&js=var%20GDcpcZgv={pages:(tp),data:(x)}&rt=51356715',
    method: 'GET'
  };

var req = http.request(options, function(res){
    var data = '';
    res.setEncoding('utf8');
    res.on('data', function(chunk){
        data += chunk;
      });
    res.on('end', function(err){
      if(err)
      {
        console.log(err.message);
      }
      var MailSubject = "";
      var MailMessage = "";
      var MailMessageEnd = "";
      eval(data);
      var xgPages = GDcpcZgv.pages;
      var xgData = GDcpcZgv.data;
      var i = 0;
      var newShareList = "";
      for(i = 0; i < xgPages; i++)
      {
        var newShareDate = new Date(Date.parse(xgData[i].purchasedate));
        var nowSec = parseInt(nowDate.getTime() / 1000);
        var newShareSec = parseInt(newShareDate.getTime() / 1000);
        /*
        if(nowSec + (nearDay * 24 * 60 * 60) < newShareSec)
        {
            break;
        }
        */
        if(nowSec <= newShareSec && nowSec + (nearDay * 24 * 60 * 60) >= newShareSec)
        {
          newShareList +=  + "名称: " + xgData[i].securityshortname + " Time: " + new Date(newShareSec) + " " + "发行价: " + xgData[i].issueprice;
					if(xgData[i] == "kcb"){
						newShareList += "[创]";
					}else if(xgData[i] == "sh"){
						newShareList += "[沪]";
					}else{
						newShareList += "[深]";
					}
				 	newShareList += "</br>";
        }
      }
      if(newShareList != "")
      {
        callbackFunc(newShareList);
      }
    
      });
    res.on('error', function(err){
        console.log("Proble with request: " + err.message);
        });
      
    });
    req.end();

}

function sendMailByNewShare(){
  var nowDate = new Date(Date.now());
  var nowYear = nowDate.getFullYear();
  var nowMonth = nowDate.getMonth();
  var nowDay = nowDate.getDate();
//  console.log(nowDate);
//  console.log(nowDay);
  if(!((nowDate.getHours() ==10  && nowDate.getMinutes() <= 15) ||  
      (nowDate.getHours() == 11 && nowDate.getMinutes() <= 15) || 
      (nowDate.getHours() == 8 && nowDate.getMinutes() <= 25)))
  {
//    console.log("Now Hour: " + nowDate.getHours);
    return false;
  }
  var options = {
    hostname: 'dcfm.eastmoney.com',
    port: 80,
    path: '/em_mutisvcexpandinterface/api/js/get?type=XGSG_LB&token=70f12f2f4f091e459a279469fe49eca5&st=purchasedate,securitycode&sr=-1&p=1&ps=50&js=var%20GDcpcZgv={pages:(tp),data:(x)}&rt=51356715',
    method: 'GET'
};

var req = http.request(options, function(res){
    var data = '';
    res.setEncoding('utf8');
    res.on('data', function(chunk){
        data += chunk;
      });
    res.on('end', function(err){
      if(err)
      {
        console.log(err.message);
      }
      var MailSubject = "New Share for U";
      var MailMessage = "小姐姐，今天有新股可以申购了， 新股名称： ";
      var MailMessageEnd = "要及时申购噢，么么哒, 小姐姐，申购时间随意";
      eval(data);
      var xgPages = GDcpcZgv.pages;
      var xgData = GDcpcZgv.data;
      var i = 0;
      var newShareList = "";
      for(i = 0; i < xgPages; i++)
      {
        var newShareDate = new Date(Date.parse(xgData[i].purchasedate));
        var newShareYear = newShareDate.getFullYear();
        var newShareMonth = newShareDate.getMonth();
        var newShareday = newShareDate.getDate();
        if(nowYear > newShareYear ||
            (nowYear == newShareYear && nowMonth > newShareMonth) ||
            (nowYear == newShareYear && nowMonth == newShareMonth && nowDay > newShareday))
        {
            break;
        }
        if(nowYear == newShareYear && nowMonth == newShareMonth && nowDay == newShareday)
        {
					if(xgData[i].sc == "kcb"){
						newShareList += xgData[i].securityshortname + "【创】 ";
					}else if(xgData[i].sc == "sh"){
						newShareList += xgData[i].securityshortname + "【沪】 ";
					}else{
						newShareList += xgData[i].securityshortname + "【深】 ";
					}
        }
      }
      if(newShareList != "")
      {
          var myOptions = mailOptions;
          myOptions.subject = MailSubject;
          myOptions.html = MailMessage + newShareList + MailMessageEnd;
          myOptions.index = 0;
          mailTrans.sendMail(myOptions, function(error, info){
          if(error){
            console.log(error);
            }else{
          }
         });
      }
    
      });
    res.on('error', function(err){
        console.log("Proble with request: " + err.message);
        });
      
    });
    req.on('error', function(err){
        console.log(err.message);
        });
    req.on('timeout', function(err){
        console.log(err.message);
        });
    req.end();
}
function getMarketMessage()
{
  /*
http://api-ddc.wallstreetcn.com/market/real?fields=symbol,prod_name,prod_en_name,price_precision,px_change_rate,px_change,last_px&prod_code=000001.SS,600519.SS,NAS.OTC,JP225.OTC,CNA50.FTSE,603260.SS,600848.SS,CN10YR.OTC,US10YR.OTC,USDCNY.OTC,600309.SS,000001.SZ,600050.SS,002352.SZ,600145.SS,000063.SZ,601633.SS,000895.SZ,USCL.OTC,002266.SZ,002680.SZ,601000.SS,000538.SZ,600606.SS,XAUUSD.OTC,USDCNH.OTC,000338.SZ,399001.SZ,600029.SS,US30.OTC,VIX.OTC,US500.OTC,DXY.OTC,UKOIL.OTC,XAGUSD.OTC,USPL.OTC
     */
  var options = {
    hostname: 'api-ddc.wallstreetcn.com',
    port: 80,
    path: '/market/real?fields=symbol,prod_name,prod_en_name,price_precision,px_change_rate,px_change,last_px&prod_code=000001.SS,600519.SS,NAS.OTC,JP225.OTC,CNA50.FTSE,603260.SS,600848.SS,CN10YR.OTC,US10YR.OTC,USDCNY.OTC,600309.SS,000001.SZ,600050.SS,002352.SZ,600145.SS,000063.SZ,601633.SS,000895.SZ,USCL.OTC,002266.SZ,002680.SZ,601000.SS,000538.SZ,600606.SS,XAUUSD.OTC,USDCNH.OTC,000338.SZ,399001.SZ,600029.SS,US30.OTC,VIX.OTC,US500.OTC,DXY.OTC,UKOIL.OTC,XAGUSD.OTC,USPL.OTC',
    method: 'GET'
  };
var req = http.request(options, function(res){
    var data = '';
    var market_message;
    res.setEncoding('utf8');
    res.on('data', function(chunk){
        data += chunk;
      });
    res.on('end', function(err){
      if(err)
      {
        console.log(err.message);
        return;
      }
      try
      {
        market_message = JSON.parse(data);
      }
      catch(error){
        console.log(err.message);
        return ;
      }
      console.log(market_message.stringify());
    })

    res.on('error', function(err){
        console.log("Proble with request: " + err.message);
        });
    });
    req.end();
}

//getNewShareNearToday(3, printNewShare)
sendMailByNewShare();
setInterval(sendMailByNewShare, (15 * 60 + 32)* 1000);
setInterval(sendMailByPlan, (3 * 60) * 1000);
//mysqlConn.end();

