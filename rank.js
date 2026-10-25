// rank.js —— 把 assets/rank.json 渲染成榜单
const listEl = document.querySelector("#rank-list");
const updatedEl = document.querySelector("#rank-updated");

fetch("assets/rank.json")
  .then(function (res) {
    if (!res.ok) throw new Error("HTTP " + res.status);
    return res.json();
  })
  .then(function (data) {
    const books = data.books;
    // 榜单里最多的一票，用来算条形长度
    const max = Math.max.apply(null, books.map(function (b) { return b.tickets; }));

    const rows = books.map(function (book) {
      const percent = (book.tickets / max) * 100;
      return `
        <li class="rank-item">
          <span class="rank-no">${book.rank}</span>
          <div class="rank-main">
            <div class="rank-line">
              <span class="rank-title">${book.title}</span>
              <span class="rank-tickets">${book.tickets.toLocaleString()}</span>
            </div>
            <div class="rank-bar"><i style="width:${percent}%"></i></div>
          </div>
        </li>
      `;
    }).join("");

    listEl.innerHTML = `<ol class="rank-list">${rows}</ol>`;
    updatedEl.textContent = `共 ${data.count} 本 · 抓取于 ${data.fetched_at}`;
  })
  .catch(function (err) {
    listEl.innerHTML = '<p class="meta">榜单加载失败：' + err.message + '</p>';
  });
