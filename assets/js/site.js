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

  /* ---------------- árvore que segue o ponteiro ----------------
     Só escreve duas custom properties; toda a animação é CSS. Fica fora de
     touch e de prefers-reduced-motion, e as escritas são agrupadas num
     requestAnimationFrame para não recalcular estilo a cada pixel do mouse. */

  var hero = document.querySelector(".hero");
  var tree = document.querySelector(".tree");
  var pontFino = window.matchMedia("(hover: hover) and (pointer: fine)").matches;
  var calmo = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  if (hero && tree && pontFino && !calmo) {
    var raf = 0, mx = 0, my = 0;

    var aplicar = function () {
      raf = 0;
      tree.style.setProperty("--mx", mx.toFixed(3));
      tree.style.setProperty("--my", my.toFixed(3));
    };
    var agendar = function () { if (!raf) raf = requestAnimationFrame(aplicar); };

    hero.addEventListener("pointermove", function (ev) {
      var r = hero.getBoundingClientRect();
      if (!r.width || !r.height) return;
      // -0.5 a 0.5 em cada eixo, medido sobre o hero inteiro
      mx = Math.min(0.5, Math.max(-0.5, (ev.clientX - r.left) / r.width - 0.5));
      my = Math.min(0.5, Math.max(-0.5, (ev.clientY - r.top) / r.height - 0.5));
      agendar();
    });

    hero.addEventListener("pointerleave", function () { mx = my = 0; agendar(); });
  }

  /* ---------------- estrelas do GitHub ----------------
     Os contadores nascem com `hidden` e só aparecem se a API responder: sem
     rede, offline ou estourando o rate limit (60 req/h por IP, sem token), a
     página simplesmente não mostra o número em vez de exibir um placeholder. */

  var starHosts = document.querySelectorAll("[data-stars-host]");
  if (starHosts.length) {
    var SKEY = "ygg-gh-stars";
    var STTL = 3600000;   // 1 h de cache por sessão, para não repetir a chamada a cada página

    var paintStars = function (n) {
      starHosts.forEach(function (host) {
        var slot = host.querySelector("[data-stars]");
        if (slot) slot.textContent = String(n);
        host.removeAttribute("hidden");
      });
    };

    var cached = null;
    try { cached = JSON.parse(sessionStorage.getItem(SKEY) || "null"); } catch (e) { /* modo privado */ }

    if (cached && typeof cached.n === "number" && Date.now() - cached.t < STTL) {
      paintStars(cached.n);
    } else if (window.fetch) {
      fetch("https://api.github.com/repos/richardguilhermeds/Yggdrasil-Project")
        .then(function (r) { return r.ok ? r.json() : Promise.reject(r.status); })
        .then(function (d) {
          if (typeof d.stargazers_count !== "number") return;
          paintStars(d.stargazers_count);
          try {
            sessionStorage.setItem(SKEY, JSON.stringify({ n: d.stargazers_count, t: Date.now() }));
          } catch (e) { /* modo privado */ }
        })
        .catch(function () { /* contadores seguem ocultos */ });
    }
  }

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
