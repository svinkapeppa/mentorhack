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

  const getMemberId = email =>
    axios
      .get(`https://api.trello.com/1/search/members/`, {
        params: {
          query: email,
          key,
          token,
        },
      })
      .then(response => {
        // console.log(888, response.data);

        return { email, id: response.data[0].id };
      })
      .catch(err => {
        // console.log({ err });
        if (err.response.status !== 404) {
          out.error = err.message;
        }
      });

  const userIdRequests = idMembers
    .split(',')
    .filter(e => e !== '')
    .map(getMemberId);

  Promise.all(userIdRequests).then(members => {
    const getMemberCardsAmount = ({ id, email }) =>
      axios
        .get(`https://api.trello.com/1/members/${id}/cards`, {
          params: {
            key,
            token,
          },
        })
        .then(response => {
          // console.log(3434, Array.isArray(response.data));

          out.memberCardAmounts.push({
            id,
            email,
            cardsAmount: response.data.length,
          });
        })
        .catch(err => {
          if (err.response.status !== 404) {
            out.error = err.message;
          }
        });

    const options = {
      method: 'POST',
      url: 'https://api.trello.com/1/cards',
      qs: {
        idList,
        name,
        desc,
        idMembers: members.map(m => m.id),
        due,
        keepFromSource: 'all',
        key,
        token,
      },
    };

    request(options, (error, response, body) => {
      if (error) {
        out.error = error.message;
        return;
      }
      // console.log({ error });
      // console.log({body});

      out.newCard = JSON.parse(body);

      const userCardAmountRequests = members.map(getMemberCardsAmount);

      Promise.all(userCardAmountRequests).then(() =>
        console.log(JSON.stringify(out))
      );
      // .catch(e => console.log({ e }));
    });
  });
});
