#!/usr/bin/env node
const { exec } = require('child_process');
const stdin = process.openStdin();

stdin.on('data', task => {
  task = String(task).replace('\n', '');


  var request = require("request");

  var options = { method: 'POST',
    url: 'https://api.trello.com/1/cards',
    qs: 
     { name: task,
       idList: '5a820d4e3ec5319990007898',
       keepFromSource: 'all',
       key: '09ee14411f546915a65d690b1a8d36b0',
       token: 'cb3a3b3c080047af57ad3d4f37ac45e252aecf11ba5e577d6ff01072d899954e' } };

  request(options, function (error, response, body) {
    if (error) throw new Error(error);

    console.log(body);
  });
});

