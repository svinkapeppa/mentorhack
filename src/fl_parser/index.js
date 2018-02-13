const axios = require('axios');
const fs = require('fs');

const tasksAmount = 3520000;
const flowsAmount = 10;
const tasksPerFlow = tasksAmount / flowsAmount;
let currentTotalTaskN = 0;

const getPage = id => {
  const url = 'https://www.fl.ru/projects/' + id;
  console.log(`getting page #${id}, url: ${url}`);

  return axios
    .get(url)
    .then(async response => {
      // console.log('DATA', response.data);

      console.log(`got page #${id}`);

      fs.writeFile(`./pages/${id}.html`, response.data, err => {
        if (err) {
          console.log('writing file error: ' + err);
        } else {
          console.log(`wrote page #${id}`);
        }
      });
    })
    .catch(err => console.error('fetch error: ' + err));
};

const runFlow = n =>
  setImmediate(async () => {
    const padding = tasksPerFlow * n;

    console.log(`flow #${n} padding: ${padding}`);

    for (let i = padding - tasksPerFlow; i < padding; ++i) {
      ++currentTotalTaskN;
      console.log(`!!!!!! current total task # ${currentTotalTaskN}`);
      await getPage(i);
    }
  });

for (let j = 1; j <= flowsAmount; ++j) {
  runFlow(j);
  console.log(`ran flow #${j}`);
}
