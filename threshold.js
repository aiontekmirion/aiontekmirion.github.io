/* The threshold back into the Room, from the heart of the Compass Rose:
   the book falls open, the phoenix rises, glitches and vanishes, and the Room
   fades up. The same crossing as the front door. */
(function () {
  var CSS = "#tx{position:fixed;inset:0;z-index:2147483600;background:#000;opacity:0;transition:opacity .35s ease}#tx.on{opacity:1}" +
    "#tx video{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;background:#000;transition:opacity .25s ease}" +
    "#tx .bd{position:absolute;inset:0;display:grid;place-items:center;overflow:hidden;visibility:hidden}#tx .bd.go{visibility:visible}" +
    "#tx .bd i{position:absolute;width:min(70vmin,560px);aspect-ratio:1;background:url(/images/door/phoenix-glitch.webp) center/contain no-repeat;opacity:0}" +
    "#tx .bd .r{mix-blend-mode:screen;filter:sepia(1) saturate(9) hue-rotate(-50deg)}#tx .bd .c{mix-blend-mode:screen;filter:sepia(1) saturate(9) hue-rotate(150deg)}" +
    "#tx .bd b{position:absolute;inset:0;background:repeating-linear-gradient(0deg,rgba(255,255,255,.045) 0 1px,transparent 1px 3px)}" +
    "#tx .bd u{position:absolute;left:0;right:0;top:50%;height:2px;background:#fff;box-shadow:0 0 18px 4px #fff;opacity:0}" +
    "#tx .bd.go .a{animation:txm 1.6s steps(1,end) forwards}#tx .bd.go .r{animation:txs 1.4s steps(1,end) forwards}#tx .bd.go .c{animation:txs2 1.4s steps(1,end) forwards}#tx .bd.go u{animation:txl 1.6s ease-out forwards}" +
    "@keyframes txm{0%{opacity:0}6%{opacity:1}14%{opacity:.2;transform:translateX(-6px)}18%{opacity:1;transform:none}30%{opacity:1;clip-path:inset(20% 0 55% 0);transform:translateX(10px)}34%{opacity:1;clip-path:none;transform:none}48%{opacity:1;clip-path:inset(60% 0 10% 0);transform:translateX(-12px)}52%{opacity:1;clip-path:none;transform:none}62%{opacity:1;filter:brightness(2.4);transform:scale(1.02)}66%{opacity:1;filter:brightness(1);transform:none}78%{opacity:1;filter:brightness(3);transform:scaleY(.04) scaleX(1.15)}84%{opacity:0;transform:scaleY(0)}100%{opacity:0}}" +
    "@keyframes txs{0%{opacity:0}12%{opacity:.8;transform:translate(-9px,2px)}20%{opacity:0}40%{opacity:.7;transform:translate(14px,-3px);clip-path:inset(35% 0 40% 0)}46%{opacity:0}64%{opacity:.9;transform:translate(-5px,0)}70%{opacity:0}100%{opacity:0}}" +
    "@keyframes txs2{0%{opacity:0}12%{opacity:.8;transform:translate(9px,-2px)}20%{opacity:0}40%{opacity:.7;transform:translate(-14px,3px);clip-path:inset(10% 0 70% 0)}46%{opacity:0}64%{opacity:.9;transform:translate(5px,0)}70%{opacity:0}100%{opacity:0}}" +
    "@keyframes txl{0%,74%{opacity:0;transform:scaleX(.2)}80%{opacity:1;transform:scaleX(1)}92%{opacity:0;transform:scaleX(1.1) scaleY(.3)}100%{opacity:0}}";
  window.crossToRoom = function (url) {
    if (window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches) { location.href = url; return; }
    var st = document.createElement("style"); st.textContent = CSS; document.head.appendChild(st);
    var o = document.createElement("div"); o.id = "tx"; o.setAttribute("aria-hidden", "true");
    o.innerHTML = '<div class="bd"><i class="a"></i><i class="r"></i><i class="c"></i><b></b><u></u></div>';
    var v = document.createElement("video"); v.src = "/images/door/book-opens.mp4"; v.muted = true; v.playsInline = true; v.setAttribute("playsinline", "");
    o.appendChild(v); document.body.appendChild(o);
    var bd = o.querySelector(".bd"), stage = 0;
    function enter() { try { sessionStorage.setItem("fdJust", "1"); } catch (e) {} location.href = url; }
    function glitch() { if (stage > 0) return; stage = 1; v.style.opacity = "0"; bd.classList.add("go"); setTimeout(enter, 1650); }
    requestAnimationFrame(function () { o.classList.add("on"); });
    setTimeout(function () {
      var p = v.play(); if (p && p.catch) p.catch(glitch);
      v.addEventListener("ended", glitch, { once: true });
      o.addEventListener("click", glitch, { once: true });
      setTimeout(glitch, 6500);
    }, 350);
  };
  addEventListener("pageshow", function (e) { if (e.persisted) { var o = document.getElementById("tx"); if (o) o.remove(); } });
})();
