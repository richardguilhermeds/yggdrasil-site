/* Yggdrasil Project · interações do site (sem dependências).
   Tudo é progressive enhancement: a página funciona inteira sem este arquivo. */
(function () {
  "use strict";

  var KEY = "yggdrasil-world";
  var DEFAULT_WORLD = "asgard";
  var root = document.documentElement;

  // texto limpo de um nó que pode não existir
  function textoDe(el) { return el ? el.textContent.trim() : ""; }

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

  /* ---------------- lightbox das figuras ----------------
     Clicar numa figura amplia na própria página em vez de abrir outra aba.
     Sem JS, ou num navegador sem <dialog>, o href da figura continua valendo e
     a imagem abre normalmente; ctrl/cmd/shift + clique seguem abrindo em aba. */

  var lb = document.querySelector("[data-lightbox]");

  if (lb && typeof lb.showModal === "function") {
    var lbImg   = lb.querySelector("[data-lb-img]");
    var lbStage = lb.querySelector("[data-lb-stage]");
    var lbNo    = lb.querySelector("[data-lb-no]");
    var lbTit   = lb.querySelector("[data-lb-title]");
    var lbSub   = lb.querySelector("[data-lb-sub]");
    var lbHint  = lb.querySelector("[data-lb-hint]");

    // preenche um slot com texto e o esconde quando não há o que mostrar
    var preencher = function (el, texto) {
      if (!el) return;
      el.textContent = texto || "";
      if (texto) el.removeAttribute("hidden");
      else el.setAttribute("hidden", "");
    };

    // em toque não há Esc nem cursor, então a dica muda de verbo e de saída
    var toque = !pontFino;
    var VERBO = toque ? "toque" : "clique";
    var SAIR = toque ? "toque fora para fechar" : "Esc para fechar";
    var DICA_AMPLIAR = VERBO + " na imagem para o tamanho real · " + SAIR;
    var DICA_AJUSTAR = VERBO + " de novo para ajustar à tela · " + SAIR;

    /* rx/ry são o ponto clicado em fração da imagem (0 a 1): depois de ampliar,
       a rolagem vai para lá, senão a pessoa amplia e perde a região que queria. */
    var zoom = function (on, rx, ry) {
      lb.classList.toggle("is-zoom", on);
      if (lbHint) lbHint.textContent = on ? DICA_AJUSTAR : DICA_AMPLIAR;
      if (!lbStage) return;
      if (!on) { lbStage.scrollTop = 0; lbStage.scrollLeft = 0; return; }
      var fx = typeof rx === "number" ? rx : 0.5;
      var fy = typeof ry === "number" ? ry : 0.5;
      lbStage.scrollLeft = fx * lbStage.scrollWidth - lbStage.clientWidth / 2;
      lbStage.scrollTop = fy * lbStage.scrollHeight - lbStage.clientHeight / 2;
    };

    // numa tela larga o bastante a figura já cabe inteira: aí não há o que ampliar
    var revisarGanho = function () {
      var cabe = lbImg.naturalWidth && lbImg.clientWidth >= lbImg.naturalWidth - 1;
      lb.classList.toggle("is-flat", !!cabe);
    };
    lbImg.addEventListener("load", revisarGanho);

    var abrir = function (link) {
      var img = link.querySelector("img");
      var cap = link.querySelector(".cap");

      lbImg.src = link.getAttribute("href");
      lbImg.alt = img ? img.getAttribute("alt") || "" : "";

      // legenda: a da galeria quando existe, senão o rótulo do mock do módulo
      preencher(lbNo, textoDe(link.querySelector(".mod__no")));
      preencher(lbTit, textoDe(cap) || textoDe(link.closest(".mock") &&
                link.closest(".mock").querySelector(".mock__bar")) || "Figura");
      preencher(lbSub, textoDe(link.querySelector(".sub")));

      zoom(false);
      root.classList.add("is-lb-open");
      lb.showModal();
      if (lbImg.complete) revisarGanho();
    };

    document.addEventListener("click", function (ev) {
      var link = ev.target.closest("[data-zoom]");
      if (!link) return;
      if (ev.metaKey || ev.ctrlKey || ev.shiftKey || ev.altKey) return;
      ev.preventDefault();
      abrir(link);
    });

    lb.addEventListener("click", function (ev) {
      if (ev.target.closest("[data-lb-close]")) { lb.close(); return; }
      if (ev.target === lbImg) {
        if (lb.classList.contains("is-flat")) return;
        var r = lbImg.getBoundingClientRect();
        zoom(!lb.classList.contains("is-zoom"),
             (ev.clientX - r.left) / r.width, (ev.clientY - r.top) / r.height);
        return;
      }
      // clique no vazio ao redor da figura fecha, como todo lightbox
      if (!ev.target.closest(".lb__fig")) lb.close();
    });

    lb.addEventListener("close", function () {
      zoom(false);
      root.classList.remove("is-lb-open");
    });
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
