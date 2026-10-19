// 11-demo.js —— 把 JSON 数据渲染成页面
// 打开方式必须是 http://127.0.0.1:8123/learning/11-demo.html
// 用 file:// 双击打开会失败（CORS），这是第 1 课讲过的 file:// 与 http:// 的区别。

// ---------- 1. 拿到要放内容的盒子 ----------
const listEl = document.querySelector("#track-list");

// ---------- 2. 把一个数组变成一段 HTML ----------
function renderTracks(tracks) {
  // map：对每一首曲子执行一次函数，收集成新数组
  const parts = tracks.map(function (t) {
    // 反引号 = 模板字符串，只有它能在字符串里直接写 ${变量}
    return `
      <div class="track">
        <h3>${t.title}</h3>
        <p class="meta">${t.meta}</p>
        <audio controls src="${t.file}"></audio>
      </div>
    `;
  });

  // join("")：把 ["<div>..</div>", "<div>..</div>"] 粘成一个字符串
  return parts.join("");
}

// ---------- 3. 出错时给用户看的提示 ----------
function renderError(message) {
  listEl.innerHTML = `
    <div class="track">
      <h3>曲目加载失败</h3>
      <p class="meta">${message}</p>
      <p class="meta">检查：文件名写对了吗？服务器开了吗？JSON 里少逗号了吗？</p>
    </div>
  `;
}

// ---------- 4. fetch 读 JSON（异步，数据在 .then 里） ----------
fetch("11-demo.json")
  .then(function (res) {
    // res 是 HTTP 响应对象，不是数据
    if (!res.ok) {
      throw new Error("HTTP " + res.status);
    }
    return res.json();          // 解析成 JS 数组，返回 Promise
  })
  .then(function (tracks) {
    // 这里才是真正的数据
    listEl.innerHTML = renderTracks(tracks);
    console.log("渲染了 " + tracks.length + " 首曲子");
  })
  .catch(function (err) {
    // 路径错、JSON 语法错、服务器没开，全都会走到这里
    console.log("加载失败：", err);
    renderError(err.message);
  });
