var nodemailer = require("nodemailer");
var http = require('http');
/**/
var mailOptions = {
  from: '13007568302@163.com',
//  to: '13007568302@163.com, 779220717@qq.com',
  to: 'zhengtianjie@me.com',
  subject: 'Hello',
  html: 'Hello, World',
  index: 0
};
var mailTrans = nodemailer.createTransport({
service: '163',
auth: {
  user: '13007568302@163.com',
  pass: '13073shanguangy'
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
//mysqlConn.connect();

function sendMailByPlan(){
  mysqlConn.query("select * from plan where trigger_date <= NOW() and isSent = 0", function(err, result){
    var size = result.length;
    var i = 0;
    for(i = 0; i < size; i++)
    {
      {
        var myOptions = mailOptions;
        myOptions.subject = result[i]["subject"];
        myOptions.html = result[i]["data"];
        myOptions.index = result[i]["index"];
        mailTrans.sendMail(myOptions, function(error, info){
          if(error){
            console.log(error);
          }else{
         }
      });
        var mysqlQuery = "update plan set isSent = 1 where `index`=1";
    //    console.log(mysqlQuery);
        mysqlConn.query("update plan set isSent = 1 where plan.index=" + result[i]['index'], function(err, info){});
      }
    }
  });
}
*/
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
          console.log(xgData[i].purchasedate);
					if(xgData[i].issueprice != "-"){
          newShareList = "名称: " + xgData[i].securityshortname + " Time: " + newShareDate.getFullYear() + "-" + (newShareDate.getMonth() + 1) + "-" + newShareDate.getDate() + " " + "发行价: " + xgData[i].issueprice + "</br>" + newShareList;
					}else{
          newShareList = "名称: " + xgData[i].securityshortname + " Time: " + newShareDate.getFullYear() + "-" + (newShareDate.getMonth() + 1) + "-" + newShareDate.getDate() + " " + "预估发行价: " + xgData[i].jg1 + "</br>" + newShareList;
					}
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
  if(nowDate.getHours() != 9 || nowDate.getMinutes() >= 15)
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
      var MailSubject = "新股申购";
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
          newShareList += xgData[i].securityshortname + " ";
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
function dailyTask(){
  var nowDate = new Date(Date.now());
  var nowYear = nowDate.getFullYear();
  var nowMonth = nowDate.getMonth();
  var nowDay = nowDate.getDate();
  if(!(nowDate.getHours() == 7  && nowDate.getMinutes() <= 15))
  {
    return false;
  }
	getNewShareNearToday(55, printNewShare);
}

setInterval(dailyTask, 11 * 60 * 1000);
getNewShareNearToday(55, printNewShare);
/*
setInterval(sendMailByNewShare, 11 * 60 * 1000);
setInterval(sendMailByPlan, 30000);
*/
//mysqlConn.end();

