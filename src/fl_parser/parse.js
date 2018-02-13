const fs = require('fs');
const jsdom = require('jsdom');
const csvStringify = require('csv-stringify');
const { JSDOM } = jsdom;

const n = process.argv[2];
if (!n) throw new Error('pass n');

const pagesPath = './pages_' + n;
let i = 0;

console.log({n});

// const stringify = data => new Promise((resolve, reject) => {
//   return csvStringify(data, (err, csv) => {
//     if (err) return console.log(`Error: ${err}`);
//     return resolve(csv);
//   });
// });

let pages = fs.readdirSync(pagesPath).filter(el => el !== '.' && el !== '..');

const tasks = pages.map(page => {
  const body = fs.readFileSync(`${pagesPath}/${page}`);
  // const body = fs.readFileSync('./pages/1056093.html');
  const dom = new JSDOM(body);
  const document = dom.window.document;

  const taskTitle = document.querySelector(
    '.b-page__title.b-page__title_ellipsis'
  ).textContent.trim();

  const taskBody = document.querySelector(
    '.b-layout__txt.b-layout__txt_padbot_20'
  ).textContent.trim();

  console.log(++i);

  return taskTitle && taskBody ? [ taskTitle, taskBody ] : null;
});

const completedTasks = tasks.filter(t => t !== null);

csvStringify(completedTasks, (err, csv) => {
  if (err) return console.error(`Error: ${err}`);
  // console.log({csv, tasks});
  fs.writeFileSync(`./out${n}.csv`, csv);
});
