// notes.js —— 把 assets/notes.json 渲染成笔记列表
// 这是第 13 课的作业：结构照抄 music.js，数据换成笔记的。

const listEl = document.querySelector("#note-list");

fetch("assets/notes.json")
  .then(function (res) {
    if (!res.ok) throw new Error("HTTP " + res.status);
    return res.json();
  })
  .then(function (notes) {
    const items = notes.map(function (note) {
      return `
        <li>
          <span class="note-date">${note.date}</span>
          <a href="${note.url}">${note.title}</a>
          <span class="note-tag">${note.tags[0]}</span>
        </li>
      `;
    }).join("");

    listEl.innerHTML = `<ul class="note-list">${items}</ul>`;
  })
  .catch(function (err) {
    listEl.innerHTML = '<p class="meta">笔记加载失败：' + err.message + '</p>';
  });
