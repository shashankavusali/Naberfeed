/*usnpl.js*/
var http = require("http");
var htttps = require("https");
var cheerio = require("cheerio");
var request = require("request");
var fs = require("fs");

// var sites = fs.readFileSync("sources.txt",'utf8').toString().split("\n");
var states = ["AL","AK","AZ","AR","CA","CO","CT","DE","DC",
"FL","GA","HI","ID","IL","IN","IA","KS","KY","LA","ME","MD",
"MA","MI","MN","MS","MO","MT","NE","NV","NH","NJ","NM","NY",
"NC","ND","OH","OK","OR","PA","RI","SC","SD","TN","TX","UT",
"VT","VA","WA","WV","WI","WY"];

var httpParameters = {
	host: "",
	path: "",
	port: 80,
	method: "GET"
}

var httpsParameters = {
	host: "www.usnpl.com",
	path: "",
	port: 443,
	method: "GET"
}