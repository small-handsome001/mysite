// notes.js —— 把 assets/notes.json 渲染成笔记列表
// 这是第 13 课的作业：结构照抄 music.js，数据换成笔记的。

const listEl = document.querySelector("#note-list");

fetch("assets/notes.json")
  .then(function (res) {
    if (!res.ok) throw new Error("HTTP " + res.status);
    return res.json();
  })
  .then(function (notes) {
    // TODO 1：用 notes.map(...) 把每条笔记变成一段 <li>...</li>
    //         每条的骨架和原来手写的一样：
    //         <li>
    //           <span class="note-date">日期</span>
    //           <a href="链接">标题</a>
    //         </li>
    //         字段名看 assets/notes.json：date / title / url
    //
    // TODO 2：把外层的 <ul class="note-list"> 和 </ul> 也拼进去
    //         因为页面里现在只剩一个空盒子 <div id="note-list"></div>
    //
    // TODO 3：塞进 listEl.innerHTML

    // 提示：map 里用反引号模板字符串，注意 note.date / note.title / note.url
  })
  .catch(function (err) {
    listEl.innerHTML = '<p class="meta">笔记加载失败：' + err.message + '</p>';
  });
