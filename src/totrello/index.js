#!/usr/bin/env node
const request = require('request');
const axios = require('axios');
const stdin = process.openStdin();

const key = '09ee14411f546915a65d690b1a8d36b0';

let out = { memberCardAmounts: [] };

stdin.on('data', input => {
  input = String(input).replace('\n', '');
  // console.log({input});

  const [token, idList, name, desc, idMembers, due] = JSON.parse(input);

  const getMemberCardsAmount = memberId =>
    axios
      .get(`https://api.trello.com/1/members/${memberId}/cards`, {
        params: {
          key,
          token,
        },
      })
      .then(response => {
        // console.log(3434, Array.isArray(response.data));

        out.memberCardAmounts.push({
          memberId,
          cardsAmount: response.data.length,
        });
      })
      .catch(err => {
        // console.log({ err });
        out.error = err.message;
      });

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
    if (error) {
      out.error = error.message;
      // console.log({ error });
      return;
    }

    out.newCard = JSON.parse(body);

    const userRequests = idMembers.split(',').map(getMemberCardsAmount);

    Promise.all(userRequests)
      .then(() => console.log(JSON.stringify(out)))
      // .catch(e => console.log({ e }));
  });
});
