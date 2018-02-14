#!/usr/bin/env node
const request = require('request');
const parse = require('csv-parse/lib/sync');
const stdin = process.openStdin();

stdin.on('data', input => {
  input = String(input).replace('\n', '');
  // console.log({input});
  
  const [ token, idList, name, desc, idMembers, due ] = parse(input)[0];
  
  const options = {
    method: 'POST',
    url: 'https://api.trello.com/1/cards',
    qs: {
      idList,
      name,
      desc,
      idMembers,
      due,
      keepFromSource: 'all',
      key: '09ee14411f546915a65d690b1a8d36b0',
      token,
    },
  };

  request(options, (error, response, body) => {
    if (error) throw new Error(error);
    console.log(body);
  });
});
