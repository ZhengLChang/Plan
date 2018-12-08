var sqlite3 = require('sqlite3');

var db = new sqlite3.Database('./plan.db', sqlite3.OPEN_READWRITE, function(err){
	if(err){
		console.log(err.message);
	}
});
	exports.queryEach = function(queryStr, callback){
					db.each(queryStr, [], callback);
			};
	exports.queryAll = function(queryStr, callback){
					db.all(queryStr, [], callback);
			};
	exports.close = function(){
	 				db.close(function(err){
						if(err){
							console.log(err.message);
						}
					console.log('Close the database connection');
					});
			};

/*
	exports = {
			queryEach: function(queryStr, callback){
					db.each(queryStr, [], callback);
			},
			close: function(){
	 				db.close(function(err){
						if(err){
							console.log(err.message);
						}
					console.log('Close the database connection');
					});
			}
		};
*/
