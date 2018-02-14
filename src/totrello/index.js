#!/usr/bin/env node
const request = require('request');
const stdin = process.openStdin();

const key = '09ee14411f546915a65d690b1a8d36b0';

let out = { memberCardAmounts: [] };

stdin.on('data', input => {
  input = String(input).replace('\n', '');
  // console.log({input});

  const [token, idList, name, desc, idMembers, due] = JSON.parse(input);

  const getMemberCardsAmount = memberId => {
    const options = {
      method: 'GET',
      url: `https://api.trello.com/1/members/${memberId}/cards`,
      qs: {
        key,
        token,
      },
    };

    request(options, (error, response, body) => {
      if (error) throw new Error(error);
      // console.log('cards for user: ', JSON.parse(body).length);
      out.memberCardAmounts.push({ memberId, cardsAmount: JSON.parse(body).length });

      console.log(out);
    });
  };

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
      key,
      token,
    },
  };

  request(options, (error, response, body) => {
    if (error) throw new Error(error);
    out.newCard = body;
    idMembers.split(',').forEach(getMemberCardsAmount);
  });
});
