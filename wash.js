/* The wash: opening a book or a door floods the page with gold, and the next
   page rises out of the same gold. Made from Sam's film of the book opening.
   Reduced motion, or any browser that will not play it, goes straight through. */
(function () {
  var GOLD = "#e6c277", CLIP = "/images/wash/gold.mp4";
  var calm = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;

  function washTo(url) {
    if (calm) { location.href = url; return; }
    var v = document.createElement("video");
    v.src = CLIP; v.muted = true; v.playsInline = true; v.setAttribute("playsinline", ""); v.setAttribute("aria-hidden", "true");
    v.style.cssText = "position:fixed;inset:0;width:100%;height:100%;object-fit:cover;z-index:2147483646;background:#000;opacity:0;transition:opacity .2s ease;pointer-events:none";
    document.body.appendChild(v);
    var done = false;
    function go(washed) {
      if (done) return; done = true;
      if (washed) {
        try { sessionStorage.setItem("washIn", "1"); } catch (e) {}
        document.documentElement.style.background = GOLD; v.style.background = GOLD;
      }
      location.href = url;
    }
    v.addEventListener("ended", function () { go(true); });
    setTimeout(function () { go(true); }, 1700);
    var p = v.play();
    v.style.opacity = "1";
    if (p && p.catch) p.catch(function () { v.remove(); go(false); });
  }
  window.washTo = washTo;

  /* the next book, at the end of the Phoenix and the Mirror; and any link marked data-wash */
  document.addEventListener("click", function (e) {
    var a = e.target.closest && e.target.closest("a[data-wash], p.next a");
    if (!a || e.defaultPrevented || e.metaKey || e.ctrlKey || e.shiftKey || a.target) return;
    e.preventDefault(); washTo(a.href);
  });

  /* warm the clip so the first wash is instant */
  addEventListener("load", function () {
    if (calm) return;
    var w = document.createElement("link"); w.rel = "prefetch"; w.href = CLIP; w.as = "video"; document.head.appendChild(w);
  });
  addEventListener("pageshow", function (e) {
    if (e.persisted) document.querySelectorAll("body>video[aria-hidden]").forEach(function (v) { if (v.src.indexOf("/images/wash/") > -1) v.remove(); });
  });
})();
