/* Yggdrasil Project · interações do site (sem dependências).
   Tudo é progressive enhancement: a página funciona inteira sem este arquivo. */
(function () {
  "use strict";

  var KEY = "yggdrasil-world";
  var DEFAULT_WORLD = "asgard";
  var root = document.documentElement;

  /* ---------------- os Nove Mundos (temas) ---------------- */

  function applyWorld(id) {
    if (id === DEFAULT_WORLD) root.removeAttribute("data-world");
    else root.setAttribute("data-world", id);
    try { localStorage.setItem(KEY, id); } catch (e) { /* modo privado */ }

    document.querySelectorAll("[data-world-btn]").forEach(function (b) {
      b.setAttribute("aria-pressed", String(b.dataset.worldBtn === id));
    });

    // mantém a barra do navegador coerente com o mundo escolhido
    var meta = document.querySelector('meta[name="theme-color"]');
    if (meta) {
      meta.content = getComputedStyle(root).getPropertyValue("--frame").trim() || "#08080a";
    }
  }

  var saved;
  try { saved = localStorage.getItem(KEY); } catch (e) { saved = null; }
  applyWorld(saved || DEFAULT_WORLD);

  document.addEventListener("click", function (ev) {
    var btn = ev.target.closest("[data-world-btn]");
    if (btn) applyWorld(btn.dataset.worldBtn);
  });

  /* ---------------- menu mobile ---------------- */

  var burger = document.querySelector("[data-burger]");
  var links = document.querySelector("[data-navlinks]");
  if (burger && links) {
    burger.addEventListener("click", function () {
      var open = links.classList.toggle("is-open");
      burger.setAttribute("aria-expanded", String(open));
    });
    links.addEventListener("click", function (ev) {
      if (ev.target.tagName === "A") {
        links.classList.remove("is-open");
        burger.setAttribute("aria-expanded", "false");
      }
    });
  }

  /* ---------------- copiar comando ---------------- */

  document.addEventListener("click", function (ev) {
    var btn = ev.target.closest("[data-copy]");
    if (!btn) return;
    var text = btn.dataset.copy;
    var done = function () {
      var old = btn.textContent;
      btn.textContent = "copiado";
      btn.classList.add("is-done");
      setTimeout(function () { btn.textContent = old; btn.classList.remove("is-done"); }, 1600);
    };
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(text).then(done, function () {});
    } else {
      var ta = document.createElement("textarea");
      ta.value = text; ta.style.position = "fixed"; ta.style.opacity = "0";
      document.body.appendChild(ta); ta.select();
      try { document.execCommand("copy"); done(); } catch (e) { /* nada a fazer */ }
      document.body.removeChild(ta);
    }
  });

  /* ---------------- revelação ao rolar ---------------- */

  var targets = document.querySelectorAll(".reveal");
  if (!("IntersectionObserver" in window) ||
      window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
    targets.forEach(function (el) { el.classList.add("is-in"); });
  } else {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add("is-in"); io.unobserve(e.target); }
      });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.05 });
    targets.forEach(function (el) { io.observe(el); });
  }
})();
