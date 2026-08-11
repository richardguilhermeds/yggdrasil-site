# yggdrasil-site

Site institucional do **[Yggdrasil Project](https://github.com/richardguilhermeds/Yggdrasil-Project)**:
biblioteca Python de esteiras governadas de machine learning para ciência de dados e risco de crédito.

🔗 **https://richardguilhermeds.github.io/yggdrasil-site/**

---

## O que é

Site estático, com temática de mitologia nórdica, que apresenta o projeto:

| Página | Conteúdo |
|---|---|
| `index.html` | Landing: as três raízes (estatística, ML, tutoriais), o ciclo do crédito, os sete módulos com mockups de saída, galeria, índice de tutoriais, seletor de temas e instalação. |
| `tutoriais.html` | Os doze notebooks organizados em quatro trilhas, com o que cada um cobre. |
| `metodologia.html` | Mapa da metodologia (KS, ratings monotônicos, PSI/CSI, SHAP, veredito de EDA) apontando para `docs/metodologia.md` no repo principal. |

## Stack

HTML, CSS e JavaScript puros: **sem build, sem dependências, sem framework**. Basta abrir os
arquivos. As únicas requisições externas são as fontes do Google Fonts (Anton, Inter, JetBrains Mono).

```
index.html
tutoriais.html
metodologia.html
assets/
  css/site.css      # tokens semânticos + os 9 temas
  js/site.js        # troca de tema, menu mobile, copiar comando, reveal
  img/              # capturas vindas de Yggdrasil-Project/docs/img/
.nojekyll           # o GitHub Pages serve os arquivos como estão
```

## Os Nove Mundos (temas)

O site inteiro é pintado por tokens semânticos (`--accent`, `--bg`, `--card`, `--ink`, `--line`…).
Cada tema é um bloco `[data-world="…"]` em `assets/css/site.css` que redefine esses tokens; o
atributo vai no `<html>` e a escolha fica no `localStorage`.

Sete escuros (Ásgard, que é o padrão, Midgard, Niflheim, Muspelheim, Jötunheim, Svartálfheim e
Helheim) e dois claros: Álfheim e Vanaheim.

> **Nunca use hex fixo no HTML.** Um valor cravado não acompanha a troca de mundo e quebra o tema.
> Para criar um tema novo, copie um bloco existente e troque só os valores.

## A árvore interativa (e como desligá-la)

A árvore do hero reage ao ponteiro de duas formas:

- **Inclinação com profundidade.** O JS escreve `--mx` e `--my` (de −0,5 a 0,5) conforme o
  mouse anda pelo hero; o resto é CSS. A copa, o halo e as raízes se deslocam em
  intensidades diferentes, o que dá a sensação de camadas.
- **Realce por ramo.** Passar o ponteiro sobre um galho ou sua cápsula acende aquele módulo
  e recua os outros para 32% de opacidade. Cada ramo tem uma trilha invisível de 26px
  (`.ramo__hit`), porque acertar um traço de 1,7px com o mouse é impossível.

Fica desligada em telas de toque e sob `prefers-reduced-motion`. O realce por ramo continua
valendo nos dois casos.

**Para voltar atrás.** O estado anterior está na tag `arvore-estatica`, e a interatividade
entrou num commit único, então reverter é um comando:

```bash
git revert --no-edit 97030aa && git push
```

Se preferir voltar os arquivos exatamente como estavam, sem criar commit de revert:

```bash
git checkout arvore-estatica -- index.html assets/css/site.css assets/js/site.js
```

## Rodar localmente

```bash
python -m http.server 8000
```

Depois abra http://localhost:8000. Abrir o `index.html` direto pelo `file://` também funciona.

## Publicação

Deploy pelo **GitHub Pages** a partir da branch `main`, pasta raiz (`/`). Todo push na `main`
republica o site em um ou dois minutos.

## Atualizar as imagens da galeria

As capturas vêm do repositório principal. Para sincronizá-las:

```bash
cp ../Yggdrasil-Project/docs/img/*.png assets/img/
```

## Licença

MIT, mesma licença do projeto principal.
