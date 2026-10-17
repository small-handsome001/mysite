# 第 8 课 · Git 版本管理

这一课**不写网页**。它解决一件事：**改坏了怎么回去。**

## 先看你要解决的问题

你现在的处境：

- `site/` 里 5 个文件，改一个可能连带搞坏另一个（你已经经历过：导航漏改、标签少个 `>`）
- 想试个大改动，比如换配色、改布局，**但不敢动**，怕改坏没法回退
- 改完三天后想不起来"我昨天到底改了啥"

**Git 就是给代码拍快照。** 每次你满意了，就拍一张；改坏了，退回任意一张。

---

## 一、先确认环境（我查过了）

```
git version 2.55.0.windows.5    ← 已装
user.name  = 空                 ← 没配
user.email = 空                 ← 没配
```

**不配这两项，`git commit` 会直接报错。** 先配：

```bash
git config --global user.name "幽林"
git config --global user.email "13646048515@163.com"
```

`--global` 意思是"这台电脑上所有仓库都用这个"，只需做一次。

> 邮箱建议和以后注册 GitHub 用的**一致**，否则 GitHub 不会把你的提交算到你头上。

---

## 二、Git 的三个区（先建概念）

```
工作区              暂存区              仓库
（你正在编辑的文件） →（准备提交的）→（已存档的历史）

   git add            git commit
```

| 区 | 是什么 | 类比 |
|---|---|---|
| **工作区** | `site/` 里的文件，你正在改的 | 桌上的草稿 |
| **暂存区** | 你挑出来"这次要存档"的改动 | 装进信封 |
| **仓库** | `.git/` 目录，永久保存的历史 | 档案柜 |

**为什么要中间那个"暂存区"？** 因为你可能同时改了三件事（修导航、改配色、加新页面），想分开存档。`git add` 就是挑：这次只存哪几件。

简单场景下你只需要记住三步：`git add` → `git commit` → 完事。

---

## 三、初始化：让 `my-site` 变成仓库

**一次性操作，只做一次：**

```bash
cd D:\my-site
git init
```

输出 `Initialized empty Git repository in D:/my-site/.git/` 就成功了。

**这一步做了什么**：在 `D:\my-site\` 下建了一个 `.git` 文件夹。所有历史都存在里面。

**注意**：

- `.git` 是隐藏文件夹，别手动删它（删了历史全没）
- **绝对不要**把 `.git` 拷来拷去
- 整个 `my-site` 用 Git 管，不是只给 `site/` 建

---

## 四、先写 `.gitignore`

在 `D:\my-site\` 下新建文件 `.gitignore`（**注意开头有个点**），内容：

```gitignore
# Windows 自动生成的缩略图缓存
Thumbs.db
Desktop.ini

# 编辑器临时文件
*.tmp
*.swp
.vscode/

# 我自己的临时截图
shot*.png
```

**为什么**：这些是系统/编辑器自动生成的垃圾文件，提交上去只会让历史变脏。`shot*.png` 是我给你截图时产生的，不该进仓库。

**语法**：一行一个规则，`#` 开头是注释，`*` 是通配符。

---

## 五、第一次提交

```bash
cd D:\my-site

git status              # ① 看现在什么状态
git add .               # ② 把所有改动装进信封
git commit -m "初始化：学习记录 + 我的网站"   # ③ 存档
```

三个命令逐个解释：

### `git status` —— 你最常用的命令

```
Untracked files:        ← 未跟踪（新文件，Git 没见过）
  learning/
  assets/

Changes not staged:     ← 已跟踪但改过，还没装信封
  modified:   learning/site/index.html
```

**任何时候不确定状态，先 `git status`。** 它不会破坏任何东西。

### `git add .` —— 装信封

`.` 表示"当前目录下的所有改动"。也可以只加一个文件：`git add learning/site/index.html`。

### `git commit -m "说明"` —— 存档

`-m` 后面是**这次改动的说明**。写清楚"做了什么"，不要写 "update"、"修改"。

**好的提交说明**：

- `修复音乐页导航链接`
- `首页加头像，改用 flex 布局`
- `完成第 7 课：四页导航统一`

**坏的**：

- `update`
- `1`
- `改了点东西`

半年后你只会看到这些说明。写给未来的自己看。

---

## 六、看历史

```bash
git log --oneline
```

输出像这样：

```
a1b2c3d 完成第 7 课：四页导航统一
9f8e7d6 修复 projects 页 nav 缺少开头标签
```

`--oneline` 让每条只占一行。不加的话会显示完整信息（作者、时间、完整说明）。

---

## 七、看差异：到底改了什么

```bash
git diff                  # 工作区 vs 上次提交：哪些行变了
git diff --staged         # 暂存区 vs 上次提交：准备提交的到底改了啥
```

输出用 `+` 和 `-` 标出增加和删除的行：

```diff
-      <a href="notes.html">笔记</a>
+      <a href="music.html">音乐</a>
+      <a href="notes.html">笔记</a>
```

**提交前养成看 `git diff` 的习惯**，能发现"我是不是不小心删了一行"。

---

## 八、改坏了怎么回去（重点）

### 情况 1：改了但**还没 commit**，想放弃

```bash
git status                      # 先看哪个文件被改了
git restore learning/site/index.html
```

`restore` = 把这个文件恢复成上次提交时的样子。**你这次没提交的修改会丢**，所以先想清楚。

> 老教程里写 `git checkout -- 文件`，作用一样，`restore` 是新的、更清楚的写法。

### 情况 2：已经 commit 了，但想回去看看旧版本

```bash
git log --oneline               # 找到旧版本的编号，比如 9f8e7d6
git show 9f8e7d6:learning/site/index.html
```

`show` 只是**显示**那个版本的文件内容，不会改你的工作区。安全。

### 情况 3：想整个退回旧版本

```bash
git reset --hard 9f8e7d6
```

⚠️ **危险**：这会把工作区所有文件**变成那个版本**，之后的修改全部丢失。

**新手建议**：前两周只用 `git restore`（情况 1）和 `git show`（情况 2）。`reset --hard` 等熟了再说。

---

## 九、这一课的任务

在 PowerShell 里**逐条执行**，每条执行完看一眼输出：

| # | 命令 | 你要看到 |
|---|---|---|
| 1 | `git config --global user.name "幽林"` | 无输出 |
| 2 | `git config --global user.email "13646048515@163.com"` | 无输出 |
| 3 | `cd D:\my-site` | 提示符变成 `D:\my-site>` |
| 4 | `git init` | `Initialized empty Git repository` |
| 5 | 新建 `.gitignore`（内容见第四节） | 文件出现在资源管理器 |
| 6 | `git status` | 一片红色的 `Untracked files` |
| 7 | `git add .` | 无输出 |
| 8 | `git status` | 变成绿色的 `Changes to be committed` |
| 9 | `git commit -m "初始化：学习记录 + 我的网站"` | `5 files changed, ...` |
| 10 | `git log --oneline` | 出现一条记录 |

**做完 10 步，你的代码就有第一个存档了。**

---

## 十、第二个存档：验证它有用

做一次真实的改动来练：

1. 随便改 `site/index.html` 里的简介文字
2. `git diff` —— **看它把改动标出来**
3. `git status` —— 看到 `modified:`
4. **故意改坏**：把某个 `</div>` 删掉
5. `git restore learning/site/index.html` —— 恢复
6. 浏览器刷新 —— 页面变回去了

**这一步是整个第 8 课的核心。** 你亲眼看一次"改坏了能退回去"，以后才敢放开手改。

---

## 十一、坑

| 现象 | 原因 |
|---|---|
| `fatal: not a git repository` | 没在 `my-site` 目录里。先 `cd D:\my-site` |
| `Please tell me who you are` | 没配 `user.name` / `user.email`，回第一节 |
| `nothing to commit, working tree clean` | 没有改动，或你已经 commit 过了 |
| 提交了 `shot*.png` | `.gitignore` 没生效——检查文件名是 `.gitignore` 不是 `.gitignore.txt` |
| 中文显示乱码 | PowerShell 编码问题。用 `git log` 看是好的就不影响，别纠结 |

---

## 十二、验收

- [ ] `git log --oneline` 至少有 1 条记录
- [ ] `git status` 显示 `nothing to commit`（说明工作区干净）
- [ ] 能演示一次：改坏 → `git restore` → 恢复成功
- [ ] `.gitignore` 生效：`git status` 里看不到 `shot*.png`

**全过了 → 记 `进度.md`，进第 9 课：推到 GitHub，让别人能访问你的网站。**
