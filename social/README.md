# Conteúdo social — LinkedIn e Instagram

Posts de **imagem única** (1080×1350, sem carrossel), sempre com gancho, gráfico ou
comentário na própria arte. Perfil: cientista de dados de risco de crédito.
Referências de estilo: kipper.dev, manodeyvin, boreggiodesign, moon.dsgr —
tipografia protagonista, alto contraste, uma ideia por imagem, voz própria.

## Regras anti-slop (valem para toda série)

1. Nenhuma imagem gerada por IA, nenhum stock, nenhum robô/cérebro brilhante.
2. Tipografia e gráfico são a arte. Paleta fixa por série, 2 fontes no máximo.
3. Uma ideia por imagem. Se precisa de 2 slides, é outro post.
4. Todo número é real (com fonte) ou explicitamente sintético/didático.
5. Sem emoji na arte, sem hashtag na arte, sem "🚀 descubra o poder de".
6. Dado de trabalho: nunca. Só dado público ou sintético (restrição de banco).

## Identidade visual base

| Token | Valor |
|---|---|
| Fundo | `#0E0F12` |
| Tinta | `#F4F1EA` |
| Cinza | `#9BA1AB` |
| Acento (série Eixo Torto) | `#FF4D00` |
| Título | Archivo Black |
| Texto/labels | Space Grotesk |

Margem 84px, coluna útil 912px, rodapé com marca + "Richard Guilherme · ciência
de dados & risco de crédito". Cada série nova troca só a cor de acento.

## Os 10 temas

1. **Eixo Torto** *(série produzida — ver `eixo-torto/`)* — crimes de visualização:
   eixo cortado, dois eixos, raio×área, janela conveniente, acumulado. Antes/depois
   com o mesmo dado.
2. **Por Trás do Score** — como um modelo de crédito enxerga as pessoas: o que sobe
   e desce score, mito vs. mecânica, por que "consultar não baixa". Alcance enorme
   no Brasil + autoridade direta no seu nicho.
3. **Glossário de Risco Ilustrado** *(série produzida — ver `glossario-risco/`)* —
   um termo por post com mini-diagrama: PD, LGD, EAD, KS, Gini, PSI, safra/vintage,
   ECL, estágio 2, write-off. Conteúdo salvável, autoridade 4.966/IFRS 9.
   Acento da série: verde-lima `#BEF264`. Próximos verbetes sugeridos: EAD, ECL,
   estágio 2, Gini, cura, write-off.
4. **Estatística Sem Anestesia** — um mal-entendido clássico por post: p-valor,
   média×mediana, viés de sobrevivência, base rate, regressão à média.
5. **Números do Brasil** — um dado público por post (BCB, IBGE, Serasa) com gráfico
   honesto e fonte na arte: inadimplência, endividamento das famílias, juros.
6. **Notebook Sujo** — humor confessional de ciência de dados: `df_final_v2_AGORA_VAI`,
   a célula 47 que ninguém roda, o seed que "funcionou uma vez".
7. **Opinião com Eixo** — hot take tipográfico defensável, um por post: "AUC alto
   não paga boleto", "modelo simples em produção > modelo genial no notebook".
8. **Erro Meu** — postmortem pessoal: o leakage que passou, o target mal definido,
   o que custou e a regra que ficou.
9. **A Régua** — checklists opinativos: "modelo pronto pra produção?", "essa feature
   vale a pena?", "esse gráfico aguenta comitê?".
10. **Yggdrasil em Público** — bastidores do projeto open source: uma decisão de
    design por post, antes/depois de API, número que surpreendeu.

## Pilares recomendados (não postar os 10)

Três a quatro pilares sustentam meses; dez viram improviso. Sugestão, na
distribuição ~6/2/1/1 a cada dez posts:

- **Principal (6):** Glossário de Risco Ilustrado ou Por Trás do Score — o que
  constrói autoridade no nicho que emprega.
- **Alcance qualificado (2):** Eixo Torto — visual, compartilhável, já pronto.
- **Processo/humano (1):** Erro Meu (ou Notebook Sujo, se quiser humor).
- **Artefato (1):** Yggdrasil em Público.

Cadência realista: 1–2 por semana. Métrica que importa: mensagens e convites
qualificados por mês — não curtida, não impressão.

## Como gerar os posts

```bash
pip install matplotlib pillow python-pptx fonttools numpy

# série Eixo Torto
cd social/eixo-torto
python3 make_charts.py <dir_fontes> charts           # gráficos 2x + marca
python3 make_pptx.py <dir_fontes> charts pptx        # 6 posts .pptx 1080×1350
python3 make_preview.py <dir_fontes> charts preview  # prévias .png

# série Glossário de Risco
cd social/glossario-risco
python3 make_charts.py <dir_fontes> charts           # diagramas 2x + marca ≔
python3 make_posts.py <dir_fontes> charts pptx preview
```

Fontes: Archivo Black e Space Grotesk (Google Fonts). Os `.pptx` importam no
Canva como designs editáveis (texto vivo, gráfico como imagem).
