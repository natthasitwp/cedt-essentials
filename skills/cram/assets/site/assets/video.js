/* video.js: play the lecture recording at the moment a topic is taught.

   Opt in on the page:
     <body data-video="../materials/L01.mp4" data-captions="../materials/L01.vtt">
     <div class="lecture" data-t="1:23:14"> … </div>   gets a "▶ ดูช่วงนี้" button
     <button class="jump" data-t="0:42:10">0:42:10</button>

   Times are h:mm:ss or m:ss. Without data-video the buttons are hidden, so pages still
   work when the recording is not on this machine. The dock remembers where you stopped. */
(function () {
  const body = document.body, src = body.dataset.video;
  const toSec = (t) => String(t).split(":").map(Number).reduce((a, b) => a * 60 + b, 0);
  const store = {
    get: () => { try { return +localStorage.getItem("cram-video-" + src) || 0; } catch { return 0; } },
    set: (t) => { try { localStorage.setItem("cram-video-" + src, String(Math.floor(t))); } catch {} },
  };

  document.querySelectorAll(".lecture[data-t]").forEach((box) => {
    if (box.querySelector(".jump")) return;
    const b = document.createElement("button");
    b.type = "button"; b.className = "jump"; b.dataset.t = box.dataset.t; b.textContent = "▶ ดูช่วงนี้";
    box.append(document.createElement("br"), b);
  });
  if (!src) { document.querySelectorAll(".jump").forEach((b) => (b.hidden = true)); return; }

  let dock, video;
  function open(t) {
    if (!dock) {
      dock = document.createElement("div");
      dock.id = "dock";
      dock.innerHTML = `<div class="bar"><span>คลิปบรรยาย</span><button type="button" aria-label="ปิด">✕</button></div>
        <video controls preload="metadata" playsinline></video>`;
      video = dock.querySelector("video");
      video.src = src;
      if (body.dataset.captions) {
        const tr = document.createElement("track");
        tr.kind = "subtitles"; tr.src = body.dataset.captions; tr.default = true; tr.srclang = "th";
        video.append(tr);
      }
      video.addEventListener("timeupdate", () => store.set(video.currentTime));
      dock.querySelector("button").addEventListener("click", () => { video.pause(); dock.hidden = true; });
      document.body.append(dock);
    }
    dock.hidden = false;
    const go = () => { video.currentTime = t ?? store.get(); video.play().catch(() => {}); };
    video.readyState >= 1 ? go() : video.addEventListener("loadedmetadata", go, { once: true });
  }
  document.addEventListener("click", (e) => {
    const b = e.target.closest(".jump[data-t]");
    if (b) open(toSec(b.dataset.t));
  });
})();
