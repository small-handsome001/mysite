// layout.js —— 全站共用的页头 / 页脚 / 明暗切换

// ============ 1. 导航数据（以后加页面只改这里）============
const NAV_ITEMS = [
  { href: "index.html", text: "首页" },
  { href: "projects.html", text: "项目" },
  { href: "music.html", text: "音乐" },
  { href: "notes.html", text: "笔记" },
  { href: "about.html", text: "关于" }
];

const LOGO = "YORIN";
const FOOTER_TEXT = "© 2026 幽林 · 手写 HTML";

// ============ 2. 算出「当前在第几层目录」============
// 根目录的页面：index.html      → prefix = ""
// notes/ 里的页面：ssh-key.html → prefix = "../"
function getPrefix() {
  const path = location.pathname;
  if (path.indexOf("/notes/") !== -1) return "../";
  return "";
}

// ============ 3. 当前页面 ============
function getCurrent() {
  const path = location.pathname;
  if (path.indexOf("/notes/") !== -1) return "notes.html";
  return path.split("/").pop() || "index.html";
}

// 项目子页面用的简化导航：页面上写 <body data-nav="project">
const NAV_PROJECT = [
  { href: "projects.html", text: "← 返回" },
  { href: "rank.html", text: "榜单" }
];

function getNavItems() {
  if (document.body.dataset.nav === "project") return NAV_PROJECT;
  return NAV_ITEMS;
}

// ============ 4. 两个图标（SVG，跟着文字大小走）============
const ICON_SUN = `
  <svg viewBox="0 0 24 24" width="18" height="18" fill="none"
       stroke="currentColor" stroke-width="2" stroke-linecap="round">
    <circle cx="12" cy="12" r="4" />
    <path d="M12 2v2M12 20v2M2 12h2M20 12h2
             M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4
             M19.1 4.9l-1.4 1.4M6.3 17.7l-1.4 1.4" />
  </svg>
`;

const ICON_MOON = `
  <svg viewBox="0 0 24 24" width="18" height="18" fill="none"
       stroke="currentColor" stroke-width="2" stroke-linecap="round"
       stroke-linejoin="round">
    <path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z" />
  </svg>
`;

// ============ 5. 页头 ============
function renderHeader(prefix) {
  const current = getCurrent();

  const links = getNavItems().map(function (item) {
    const isActive = item.href === current;
    const cls = isActive ? ' class="active"' : "";
    return `<a href="${prefix}${item.href}"${cls}>${item.text}</a>`;
  }).join("");

  return `
    <header class="site-header">
      <div class="brand">
        <a class="logo" href="${prefix}index.html">${LOGO}</a>
        <button id="theme-toggle" class="theme-toggle" type="button"
                aria-label="切换明暗">
          ${ICON_SUN}
        </button>
      </div>
      <nav class="nav">${links}</nav>
    </header>
  `;
}

// ============ 6. 页脚 ============
function renderFooter() {
  return `
    <footer class="site-footer">
      <p>${FOOTER_TEXT}</p>
    </footer>
  `;
}

// ============ 7. 明暗切换 ============
// 状态存在 localStorage，刷新和翻页都不会丢
const THEME_KEY = "site-theme";

function applyTheme(theme) {
  const isDark = theme === "dark";
  document.body.classList.toggle("dark", isDark);

  const btn = document.querySelector("#theme-toggle");
  if (btn) {
    btn.innerHTML = isDark ? ICON_MOON : ICON_SUN;
    btn.setAttribute("aria-label", isDark ? "切换到亮色" : "切换到暗色");
  }
}

function initTheme() {
  // 1. 先读上次的选择；没有就跟随系统
  const saved = localStorage.getItem(THEME_KEY);
  const theme = saved
    ? saved
    : (window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light");

  applyTheme(theme);

  // 2. 点按钮切换
  const btn = document.querySelector("#theme-toggle");
  if (!btn) return;

  btn.addEventListener("click", function () {
    const next = document.body.classList.contains("dark") ? "light" : "dark";
    applyTheme(next);
    localStorage.setItem(THEME_KEY, next);
  });
}

// ============ 8. 塞进页面 ============
(function mount() {
  const prefix = getPrefix();

  const headerBox = document.querySelector("#site-header");
  if (headerBox) headerBox.innerHTML = renderHeader(prefix);

  const footerBox = document.querySelector("#site-footer");
  if (footerBox) footerBox.innerHTML = renderFooter();

  // 页头渲染完才有按钮，所以放在最后
  initTheme();
})();
