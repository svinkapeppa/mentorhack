const fs = require('fs');
const jsdom = require('jsdom');
const csvStringify = require('csv-stringify');
const { JSDOM } = jsdom;

// let pages = fs.readdirSync('./pages').filter(el => el !== '.' && el !== '..');
//
// const tasks = pages.map(page => {
//   const body = fs.readFileSync('./pages/' + page);
  const body = fs.readFileSync('./pages/1056095.html');
  const dom = new JSDOM(body);
  const document = dom.window.document;

  const taskTitle = document.querySelector(
    '.b-page__title.b-page__title_ellipsis'
  ).textContent.trim();

  const taskBody = document.querySelector(
    '.b-layout__txt.b-layout__txt_padbot_20'
  ).textContent.trim();

  csvStringify([[taskTitle, taskBody]], (err, csv) => {
    if (err) return console.log(`Error: ${err}`);
    console.log(csv);
  });

  // return { taskTitle, taskBody };
// });
