var Web3 = require("web3");
var web3 = new Web3("http://localhost:9090");

web3.eth.isMining().then(console.log);
