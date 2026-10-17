/* ============================================================
   06-demo.js —— 第 6 课练习

   你要做的：把三个任务里的 TODO 换成真正的代码。
   路径：改完 Ctrl+S → 浏览器 F5。
   ============================================================ */


/* ------------------------------------------------------------
   任务 1：暗色模式切换
   
   步骤：
     a) 用 document.querySelector("#toggle") 选中那个按钮
     b) 给它 addEventListener("click", function () { ... })
     c) 函数里写 document.body.classList.toggle("dark");
   
   写完点按钮，页面应该整体变暗；再点一次变回来。
   ------------------------------------------------------------ */

// 在这里写你的代码
document.querySelector("#toggle")
.addEventListener("click", function () {
   console.log("点击了切换暗色按钮");
  document.body.classList.toggle("dark");
});


/* ------------------------------------------------------------
   任务 2：点击计数
   
   步骤：
     a) 在函数外面声明 let count = 0;   ← 必须在外层！写在函数里每次都归零
     b) 选中 #counter 按钮 和 #count 显示元素
     c) 点击时：count = count + 1; 然后 countEl.textContent = count;
   
   写完点按钮，数字应该 1、2、3…… 一直加。
   ------------------------------------------------------------ */

// 在这里写你的代码
let count = 0;
const counterBtn = document.querySelector("#counter");
const countEl = document.querySelector("#count");
addEventListener("click", function () {
   console.log("点击了 +1 按钮");
   count = count + 1;
   document.querySelector("#count").textContent = count//把 count 的值显示在 #count 元素里，这里开始时没有理解要调用函数，记住！！
});


  

/* ------------------------------------------------------------
   任务 3：打印到控制台
   
   在两个点击函数里各加一行 console.log(...)，
   然后按 F12 → Console，看每次点击有没有输出。
   
   这是调试最基本的动作：先确认函数真的被执行了。
   ------------------------------------------------------------ */



/* ------------------------------------------------------------
   自检清单
   
   [ ] 点"切换暗色"，背景变深、按钮变白、数字变浅蓝
   [ ] 点"点我 +1"，数字逐个增加
   [ ] F12 → Console 有你的 console.log 输出
   [ ] F12 → Console 没有红字
        · 如果出现 Cannot read properties of null
          → querySelector 没找到元素，检查选择器拼写
   ------------------------------------------------------------ */
