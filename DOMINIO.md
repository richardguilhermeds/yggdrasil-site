# Domínio próprio: yggdrasil-project.com.br

Passo a passo para apontar o domínio para este site no GitHub Pages. O endereço
principal é o **domínio puro** (apex); o `www` redireciona para ele.

| | |
|---|---|
| Domínio | `yggdrasil-project.com.br` |
| Registro | [Registro.br](https://registro.br) (NIC.br) |
| Hospedagem | GitHub Pages, gratuita |
| HTTPS | Let's Encrypt via GitHub, gratuito e automático |
| Custo | **R$ 40** por 1 ano, R$ 76 por 2, R$ 112 por 3 (R$ 36/ano a partir do segundo) |

---

## 1. Registrar no Registro.br

1. Crie a conta em [registro.br](https://registro.br) com **CPF ou CNPJ** (obrigatório
   para `.com.br`, é um domínio restrito a titulares brasileiros).
2. Busque `yggdrasil-project` e escolha `.com.br`.
3. Na solicitação, **não informe servidores DNS próprios**: deixe o Registro.br usar os
   servidores autoritativos dele, que são gratuitos.
4. O domínio é registrado em até 5 minutos (a fila de tickets roda a cada 5 min) e a
   cobrança chega depois, por e-mail. Pague por Pix, cartão VISA/MasterCard ou boleto.

> **O registro vem antes do pagamento.** No Registro.br o domínio já é seu assim que o
> ticket é processado; a cobrança é uma manutenção anual com vencimento, não um portão de
> liberação. Ou seja, dá para configurar o DNS e subir o site enquanto a fatura está em
> aberto. Se a fatura vencer sem pagamento, o domínio congela e depois volta para o
> mercado.

> Registre direto no Registro.br, não por revenda. Revendas cobram de R$ 45 a R$ 80 no
> primeiro ano e sobem na renovação.

## 2. Configurar o DNS

No painel do domínio, abra **Editar Zona** e adicione:

```zone
@     A       185.199.108.153
@     A       185.199.109.153
@     A       185.199.110.153
@     A       185.199.111.153
@     AAAA    2606:50c0:8000::153
@     AAAA    2606:50c0:8001::153
@     AAAA    2606:50c0:8002::153
@     AAAA    2606:50c0:8003::153
www   CNAME   richardguilhermeds.github.io.
```

Os quatro **A** (e os quatro **AAAA**, para IPv6) são os endereços do GitHub Pages para
domínios apex. O **CNAME** do `www` aponta para o domínio padrão do usuário,
`richardguilhermeds.github.io`, **sem o nome do repositório** e **com o ponto final**.

Verifique a propagação:

```bash
dig +short yggdrasil-project.com.br A
dig +short www.yggdrasil-project.com.br CNAME
```

O primeiro deve devolver os quatro IPs `185.199.10x.153`; o segundo,
`richardguilhermeds.github.io.`. Costuma levar de alguns minutos a uma hora.

## 3. Ligar o domínio no GitHub Pages

Só depois que o DNS estiver respondendo. Se fizer antes, o Pages passa a redirecionar
`richardguilhermeds.github.io/yggdrasil-site/` para um domínio que ainda não resolve, e
o site fica fora do ar até o DNS subir.

1. Crie na raiz do repositório um arquivo `CNAME` contendo uma única linha:
   ```
   yggdrasil-project.com.br
   ```
   (equivale a preencher o campo em **Settings → Pages → Custom domain**, que gera esse
   mesmo arquivo).
2. Aguarde o check de DNS do GitHub ficar verde.
3. Marque **Enforce HTTPS**. O certificado sai em alguns minutos.

## 4. Depois de ligar

- `richardguilhermeds.github.io/yggdrasil-site/` passa a redirecionar para o domínio novo,
  então links antigos continuam funcionando.
- Atualize no `index.html`, `tutoriais.html` e `metodologia.html`:
  - a tag `<link rel="canonical">`;
  - as URLs absolutas de `og:image` e `og:url`.
- Vale apontar o campo **Homepage** do repositório
  [Yggdrasil-Project](https://github.com/richardguilhermeds/Yggdrasil-Project) para o
  domínio novo.

## Renovação

O Registro.br cobra por ano. Deixe a **renovação automática** ligada e mantenha o e-mail
de contato do domínio atualizado: `.com.br` que expira entra em período de retenção e
depois volta para o mercado.
