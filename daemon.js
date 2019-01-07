var spawn = require('child_process').spawn;
var process = require('process');

var p = spawn('node', ['nodemailer.js'], {
	detached: true
});
var p = spawn('node', ['index.js'], {
	detached: true
});
process.exit(0);
