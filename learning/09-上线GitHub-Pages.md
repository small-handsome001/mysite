# 第 9 课 · 上线：GitHub Pages

学完这一课，你有一个**别人能打开的网址**。简历上能写、发给同学能点。

---

## 一、先做了一次结构调整（我已经做完了）

**变化：**

```
之前                                    现在
D:\my-site\                             D:\my-site\
├── assets\                             ├── index.html      ← 网站首页
├── learning\                           ├── projects.html
│   └── site\                           ├── music.html
│       ├── index.html                  ├── notes.html
│       └── ...                         ├── site.css
└── 启动服务器.bat                       ├── assets\
                                        ├── learning\      ← 学习资料
                                        └── 启动服务器.bat
```

**为什么必须改？** GitHub Pages 只会把你的仓库当网站发布，它**只认根目录的 `index.html`**。文件藏在 `learning/site/` 里，它找不到。

**路径也跟着变了**（这是个重要细节）：

```html
<!-- 之前：从 learning/site/index.html 出发 -->
<img src="../../assets/img/avatar.jpg" />

<!-- 现在：从仓库根出发 -->
<img src="assets/img/avatar.jpg" />
```

**预览地址也变了**：

```
http://127.0.0.1:8123/index.html
```

已提交：`0b45b7e`。改坏了还能退回去。

---

## 二、GitHub 上建仓库

1. 打开 <https://github.com>，登录 `small_handsome`
2. 右上角 **+** → **New repository**
3. 填：

| 字段 | 填什么 |
|---|---|
| Repository name | `mysite` |
| Description | 可选，写"个人网站" |
| Public / Private | **选 Public**（Private 用 Pages 要付费） |
| Initialize with README | **不勾**（勾了会产生冲突） |

4. **Create repository**

建完它会给你一段命令，先别看，往下走。

> **国内网络提示**：github.com 网页可能非常慢（我实测 25 秒还没加载完）。如果卡得动不了，见本文第八节备选方案。

---

## 三、本地关联

```bash
cd D:\my-site

git remote add origin https://github.com/small_handsome/mysite.git
git branch -M main
git push -u origin main
```

逐条解释：

| 命令 | 作用 |
|---|---|
| `git remote add origin 地址` | 给这个仓库起个外号叫 `origin`，指向 GitHub 上那个空仓库 |
| `git branch -M main` | 把当前分支改名叫 `main`。GitHub 默认用 `main`，老电脑可能是 `master` |
| `git push -u origin main` | **把本地提交推上去**。`-u` 记住这个对应关系，以后直接 `git push` |

### 会要求输入用户名和密码

```
Username for 'https://github.com': small_handsome
Password for 'https://small_handsome@github.com': ← 这里不填登录密码！
```

**密码要填 Personal Access Token（PAT）**，不是你的 GitHub 登录密码。GitHub 早就禁了密码推送。

### 创建 PAT

1. GitHub → 右上角头像 → **Settings**
2. 左侧最下 → **Developer settings**
3. **Personal access tokens** → **Tokens (classic)**
4. **Generate new token (classic)**
5. 填：

| 字段 | 填什么 |
|---|---|
| Note | `my-site push` |
| Expiration | 30 days（安全，过期再建） |
| Scopes | **只勾 `repo`**（不要勾别的） |

6. **Generate token** → 复制那串 `ghp_xxxxxxxx`

**只显示一次，关掉页面就再也看不到。** 先粘到记事本里。

粘贴到密码提示处时，**终端里不会有任何显示**（连星号都没有），这是正常的，粘完直接回车。

成功后 Windows 凭据管理器会记住，以后不用再输。

---

## 四、开启 GitHub Pages

1. 打开仓库页 → **Settings**
2. 左侧 → **Pages**
3. **Source** 选 `Deploy from a branch`
4. **Branch** 选 `main`，目录选 `/ (root)`
5. **Save**

等 1~2 分钟，页面顶部会出现：

```
Your site is live at https://small_handsome.github.io/mysite/
```

**这个网址就是你的网站。** 手机也能打开，发给谁都能点。

---

## 五、以后每次更新（三步）

改了网页、`git commit` 之后：

```bash
git push
```

GitHub Pages 会自动重新发布，**等 1~2 分钟**刷新就能看到新版本。

**注意顺序**：先 commit 再 push。`push` 推的是已提交的历史，不是工作区的文件。

---

## 六、验证清单

打开 `https://small_handsome.github.io/mysite/`：

- [ ] 首页名字和头像正常
- [ ] 点导航，四个页面能互相跳
- [ ] 音乐页能播放
- [ ] 手机打开也正常（可以真拿手机试）
- [ ] 地址栏有 🔒 锁图标（HTTPS，GitHub 自动配的）

---

## 七、这一课的坑

| 现象 | 原因 |
|---|---|
| 404 页面 | `index.html` 不在仓库根目录；或 Pages 还没发布完（等 2 分钟） |
| 图片/音频 404 | 路径还写着 `../../assets/`，没改成 `assets/` |
| 样式全丢 | `site.css` 没推上去，或 `href` 路径错 |
| 推送被拒绝 `rejected` | 建仓库时勾了 README，远程有本地没有的东西。先 `git pull --rebase origin main` 再 push |
| `Authentication failed` | 密码填成了登录密码，要用 PAT |
| 改了但线上没变 | ①忘了 push ②Pages 还在构建 ③浏览器缓存（Ctrl+F5） |
| 文件名大小写问题 | 本地 Windows 不区分大小写，GitHub 区分。`Index.html` ≠ `index.html` |

---

## 八、说句实话：国内访问速度

我实测了你这台机器到 GitHub 的网络：

```
github.com 网页     → 25 秒只收到 412KB，极慢
api.github.com      → 0.9 秒，正常
```

**这意味着：**

- `git push` 大概率能成功（走的是 git 协议，不是网页），但**可能慢**
- GitHub 网页界面会很卡，建仓库、开 Pages 这几步要有耐心
- `*.github.io` 的网址在国内**可能打不开或很慢**，取决于网络环境

### 备选方案（如果 GitHub 实在用不了）

| 方案 | 优点 | 缺点 |
|---|---|---|
| **Gitee Pages** | 国内极快 | 需实名认证；免费版 Pages 需要手动"更新"才生效 |
| **Cloudflare Pages** | 免费、快、自动部署 | 国内访问也不稳定 |
| **Vercel** | 部署体验最好 | 国内同样不稳 |

**我的建议：先按 GitHub 走一遍**（它是最标准的做法，简历上也最认），跑通之后再考虑国内镜像。

---

## 九、验收

- [ ] `git push` 成功，GitHub 仓库页能看到 5 个文件 + assets
- [ ] Pages 显示 `Your site is live at ...`
- [ ] 用**手机流量**（不用家里 WiFi）打开那个网址，能看到你的网站
- [ ] 能说出改完代码后要执行哪两条命令（`git commit` + `git push`）

**全过了，你的网站就真的上线了。**

后面想加的东西：自定义域名、暗色模式、JS 交互、把曲子一首首加进去。
