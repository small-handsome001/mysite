// notes.js —— 把 assets/notes.json 渲染成笔记列表
// 这是第 13 课的作业：结构照抄 music.js，数据换成笔记的。
const filterEl = document.querySelector("#note-filter");
const listEl = document.querySelector("#note-list");

function renderNotes(list) {
  const items = list.map(function (note) {
    return `
      <li>
        <span class="note-date">${note.date}</span>
        <a href="${note.url}">${note.title}</a>
        <span class="note-tag">${note.tags[0]}</span>
      </li>
    `;
  }).join("");

  listEl.innerHTML = `<ul class="note-list">${items}</ul>`;
}

fetch("assets/notes.json")
  .then(function (res) {
    if (!res.ok) throw new Error("HTTP " + res.status);
    return res.json();
  })
  
    .then(function (notes) {
    // 1. 收集每条笔记的标签 → ["SSH", "CSS", "HTML"]
    const tags = notes.map(function (note) {
      return note.tags[0];
    });

    // 2. 前面补一个「全部」→ ["全部", "SSH", "CSS", "HTML"]
    const allTags = ["全部"].concat(tags);

    // 3. 每个标签变成一个按钮
    const buttons = allTags.map(function (tag) {
      return `<button class="filter-btn" data-tag="${tag}">${tag}</button>`;
    }).join("");

    // 4. 塞进筛选区（外层包 div.filter-bar 才能横排）
    filterEl.innerHTML = `<div class="filter-bar">${buttons}</div>`;
        // 默认选中「全部」
    filterEl.querySelector(".filter-btn").classList.add("is-active");
    filterEl.addEventListener("click", function (event) {
      const tag = event.target.dataset.tag;
      if (!tag) return;
              // 先清掉所有按钮的高亮
      filterEl.querySelectorAll(".filter-btn").forEach(function (btn) {
        btn.classList.remove("is-active");
      });
      // 再点亮被点的这个
      event.target.classList.add("is-active");              // 点到按钮之间的空隙，退出

       
      const filtered = tag === "全部"
        ? notes

        : notes.filter(function (note) {
            return note.tags[0] === tag;
          });

      renderNotes(filtered);
    });   

    renderNotes(notes);
  })
  .catch(function (err) {
    listEl.innerHTML = '<p class="meta">笔记加载失败：' + err.message + '</p>';
  });
