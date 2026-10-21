// layout.js —— 全站共用的页头 / 页脚
// 一个地方改，7 个页面同时变。

// ============ 1. 导航数据（以后加页面只改这里）============
const NAV_ITEMS = [
  { href: "index.html", text: "首页" },
  { href: "projects.html", text: "项目" },
  { href: "music.html", text: "音乐" },
  { href: "notes.html", text: "笔记" }
];

const LOGO = "YORIN";
const FOOTER_TEXT = "© 2026 幽林";

// ============ 2. 算出「当前在第几层目录」============
// 根目录的页面：index.html      → prefix = ""
// notes/ 里的页面：ssh-key.html → prefix = "../"
function getPrefix() {
  const path = location.pathname;
  // notes/ 子目录下的页面，路径里会有 /notes/
  if (path.indexOf("/notes/") !== -1) return "../";
  return "";
}

// ============ 3. 生成页头 HTML ============
// 当前打开的是哪个页面 —— 用来决定哪个导航项高亮
function getCurrent() {
  const path = location.pathname;
  // notes/ 里的文章页（ssh-key.html 等）算作「笔记」这一项
  if (path.indexOf("/notes/") !== -1) return "notes.html";
  return path.split("/").pop() || "index.html";
}

function renderHeader(prefix) {
  const current = getCurrent();

  const links = NAV_ITEMS.map(function (item) {
    // 给当前页的链接加一个 active 类，用来高亮
    const isActive = item.href === current;
    const cls = isActive ? ' class="active"' : "";
    return `<a href="${prefix}${item.href}"${cls}>${item.text}</a>`;
  }).join("");

  return `
    <header class="site-header">
      <a class="logo" href="${prefix}index.html">${LOGO}</a>
      <nav class="nav">${links}</nav>
    </header>
  `;
}

// ============ 4. 生成页脚 HTML ============
function renderFooter() {
  return `
    <footer class="site-footer">
      <p>${FOOTER_TEXT}</p>
    </footer>
  `;
}

// ============ 5. 塞进页面 ============
// 页面里只留两个空盒子：<div id="site-header"></div> 和 <div id="site-footer"></div>
// 找不到盒子就跳过（比如某个页面不需要页脚）
(function mount() {
  const prefix = getPrefix();

  const headerBox = document.querySelector("#site-header");
  if (headerBox) headerBox.innerHTML = renderHeader(prefix);

  const footerBox = document.querySelector("#site-footer");
  if (footerBox) footerBox.innerHTML = renderFooter();
})();
