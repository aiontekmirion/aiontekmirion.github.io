/* The threshold into the Room: the page floods with gold, then the Room fades up.
   One crossing for the whole site, the same one that ends the Mirror. */
(function () {
  var SRC = "/images/door/gold-wash.mp4", v = null;
  function make() {
    if (v) return v;
    v = document.createElement("video");
    v.src = SRC; v.muted = true; v.playsInline = true; v.preload = "auto";
    v.setAttribute("playsinline", ""); v.setAttribute("aria-hidden", "true");
    v.style.cssText = "position:fixed;inset:0;width:100%;height:100%;object-fit:cover;z-index:2147483646;background:#000;opacity:0;pointer-events:none;transition:opacity .25s ease";
    document.body.appendChild(v);
    return v;
  }
  /* have the wash ready before anyone reaches for a door */
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", make); else make();
  window.crossToRoom = function (url) {
    if (window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches) { location.href = url; return; }
    var w = make(), gone = false;
    function go() { if (gone) return; gone = true; try { sessionStorage.setItem("fdJust", "1"); } catch (e) {} location.href = url; }
    w.addEventListener("ended", go, { once: true });
    setTimeout(go, 2800);                       /* never wait longer than this */
    w.currentTime = 0;
    var p = w.play(); w.style.opacity = "1";
    if (p && p.catch) p.catch(go);              /* if a browser will not play it, go straight in */
  };
  addEventListener("pageshow", function (e) { if (e.persisted && v) { v.pause(); v.style.opacity = "0"; } });
})();
