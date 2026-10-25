// index.js —— 首页「最新」区块：拉三份数据，只取第一条
const latestEl = document.querySelector("#latest");

function row(kind, text, href) {
  return `
    <li>
      <a class="latest-item" href="${href}">
        <span class="latest-kind">${kind}</span>
        <span class="latest-text">${text}</span>
        <span class="latest-arrow">→</span>
      </a>
    </li>
  `;
}

Promise.all([
  fetch("assets/notes.json").then(function (r) { return r.json(); }),
  fetch("assets/music.json").then(function (r) { return r.json(); }),
  fetch("assets/rank.json").then(function (r) { return r.json(); })
])
  .then(function (results) {
    const notes = results[0];
    const music = results[1];
    const rank = results[2];

    const rows = [];

    if (notes.length) {
      rows.push(row("笔记", notes[0].title, notes[0].url));
    }

    if (music.length) {
      rows.push(row("音乐", music[0].title, "music.html"));
    }

    if (rank.books.length) {
      rows.push(row("榜单", rank.books[0].title + " 领跑月票", "rank.html"));
    }

    latestEl.innerHTML = `<ul class="latest-list">${rows.join("")}</ul>`;
  })
  .catch(function (err) {
    latestEl.innerHTML = '<p class="meta">最新内容加载失败：' + err.message + '</p>';
  });
