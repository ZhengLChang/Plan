var sqlObj = require('./sqlObj');
sqlObj.queryEach('select * from plan;', function(err, row){
//db.each('update plan set isSent=1 where `index`=1;', [], function(err, row){
	if(err){
		console.log(err.message);
	}
	console.log([row.data, row.trigger_date, row.isSent].join('\t'));
});
sqlObj.close();

