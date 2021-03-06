const fs = require('fs');
const jsdom = require('jsdom');
const csvStringify = require('csv-stringify/lib/sync');
const { JSDOM } = jsdom;

const n = process.argv[2];
if (!n) throw new Error('pass n');

const pagesPath = './pages';
let i = 0;

console.log({n});

let pages = fs.readdirSync(pagesPath).filter(el => el !== '.' && el !== '..');

console.log(pages.length, pages[0], pages[pages.length - 1]);

const batch = 260000;
// const batch = 1000;

const padding = batch * n - batch;

pages = pages.slice(padding, padding + batch);

console.log(pages.length, pages[0], pages[pages.length - 1]);

pages.forEach(page => {
  const body = fs.readFileSync(`${pagesPath}/${page}`);
  const dom = new JSDOM(body);
  const document = dom.window.document;

  let taskTitle = document.querySelector(
    '.b-page__title.b-page__title_ellipsis'
  );

  if (taskTitle === null) return;
  taskTitle = taskTitle.textContent.trim();

  let taskBody = document.querySelector(
    '.b-layout__txt.b-layout__txt_padbot_20'
  );

  if (taskBody === null) return;
  taskBody = taskBody.textContent.trim();

  // console.log({taskTitle, taskBody });
  const csv = csvStringify([[ taskTitle, taskBody ]]);
  // console.log({csv});
  fs.appendFileSync(`./out${n}.csv`, csv);

  console.log(++i);
});
