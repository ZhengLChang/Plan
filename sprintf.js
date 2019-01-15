var sprintf = function(str){
	var args = arguments;
	var i = 1;
	/*
	console.log("=======================");
	console.log(str);
	console.log("=======================");
	*/
	var str = str.replace(/%s/g, function(){
			var arg = args[i++];
			if(typeof arg === 'undefined'){
				return '';
			}
			return arg;
			});
	/*
	console.log("=======================");
	console.log(str);
	console.log("=======================");
	*/
	return str;
};

module.exports = sprintf;
