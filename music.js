const listEl = document.querySelector("#track-list");

fetch("assets/music.json")
  .then(function (res) {
    if (!res.ok) throw new Error("HTTP " + res.status);
    return res.json();
  })
  .then(function (tracks) {
    const parts = tracks.map(function (track) {
      return `
        <div class="track">
          <h3>${track.title}</h3>
          <p class="meta">${track.meta}</p>
          <audio controls src="${track.file}"></audio>
        </div>
      `;
    });

    listEl.innerHTML = parts.join("");
    console.log("渲染了 " + tracks.length + " 首");
  })
  .catch(function (err) {
    listEl.innerHTML = `
      <div class="track">
        <h3>曲目加载失败</h3>
        <p class="meta">页面未能读到曲目数据，请刷新重试。</p>
        <p class="meta">技术信息：${err.message}</p>
      </div>
    `;
    console.log("加载失败：", err);
  });
