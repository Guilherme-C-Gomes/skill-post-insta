# Estilo: esquema do JSON e design system Eyes Tech

Índice:
1. Esquema do JSON de conteúdo
2. Tokens e componentes
3. Outra marca: derivar paleta e tipografia
4. Componentes extras, quando o slide pedir

---

## 1. Esquema do JSON de conteúdo

```json
{
  "titulo": "nome interno do carrossel",
  "slides": [
    {
      "tipo": "capa | conteudo | lista | passos",
      "kicker": "rótulo curto acima do título",
      "titulo": "headline do slide",
      "texto": "parágrafo de apoio",
      "itens": ["linha 1", "linha 2"],
      "cta": "texto do botão, só no último slide",
      "imagem": "/caminho/da/foto.jpg",
      "dica": "arrasta para o lado"
    }
  ],
  "legenda": "texto da legenda do post",
  "hashtags": ["#advocacia"]
}
```

Notas de campo:
- A assinatura de marca é o logotipo, desenhado no template. Não há campo de handle nem de avatar.
- `tipo` muda a composição: `capa` usa título de 104px, `lista` e `passos` numeram os itens, `conteudo` é título mais parágrafo, e `cta` é o parágrafo com a pílula azul.
- `imagem` aceita caminho de arquivo ou data URI. O gerador identifica o formato pelos bytes.
- `//` no meio de qualquer texto vira quebra de linha.
- `dica` no Eyes Tech: padrão "arrasta para o lado", e no último slide "salva para depois".

## 2. Tokens e componentes

| Token | Valor | Uso |
|---|---|---|
| Azul da marca | `#00B7FF` | acento, filete, numeração, CTA, "eyes" no logotipo |
| Azul escuro | `#0077A8` | títulos em fundo branco (documento, não post) |
| Fundo | `#0D0C0D` | fundo padrão de todo slide |
| Texto | `#FFFFFF` | título |
| Texto suave | `#D7DBDE` | parágrafo |
| Apagado | `#9AA0A6` | rodapé, contador |
| Grade | `rgba(0,183,255,.10)` | grade de 120px ao fundo, referência do logotipo |

Escala tipográfica, em pixel real de 1080x1350:

| Elemento | Fonte | Tamanho | Peso |
|---|---|---|---|
| Logotipo | Poppins | 40 | 700 |
| Kicker | Inter | 30, caixa alta, tracking .12em | 600 |
| Título de capa | Poppins | 104, line-height 1.02 | 700 |
| Título interno | Poppins | 72, line-height 1.08 | 600 |
| Parágrafo | Inter | 40, line-height 1.45 | 400 |
| Item de lista | Inter | 36 | 400 |
| Numeração | Poppins | 34, em quadrado azul 62px | 700 |
| CTA | Poppins | 38, em pílula azul | 700 |
| Rodapé | Inter | 28 | 400 |

Composição: respiro de 96px no topo e na base, 88px nas laterais. Logotipo no topo, conteúdo centralizado verticalmente, rodapé com dica de navegação e contador. Filete azul de 180x6px abre capa e slide de virada.

O azul é acento, nunca texto corrido. Slide inteiro azul não existe nesta identidade.

Diferença proposital em relação à skill de origem: não há alternância de fundo claro e escuro nem gradiente de marca. A identidade Eyes Tech é escura por padrão, e alternar quebraria a marca em vez de criar ritmo. O ritmo vem da variação de tipo de slide (capa, lista, passos, virada).

## 3. Outra marca: derivar paleta e tipografia

Quando o post não é da Eyes Tech, peça uma cor primária e derive o resto:

```
PRIMARIA   = cor informada
CLARA      = primária clareada ~20%    tags sobre fundo escuro, pílulas
ESCURA     = primária escurecida ~30%  texto de CTA, âncora de gradiente
FUNDO_CLARO= off-white puxando para o tom da primária, nunca #fff puro
BORDA      = uma sombra mais escura que o fundo claro
FUNDO_ESCURO = quase preto com leve tinta da marca
```

Fundo quente puxa creme (`#1A1918` no escuro), fundo frio puxa cinza-azulado (`#0F172A`). Off-white puro e preto puro deixam a arte com cara de template.

Pares de fonte que funcionam, todos disponíveis por `@fontsource`:

| Intenção | Título | Corpo |
|---|---|---|
| Editorial, premium | Playfair Display | DM Sans |
| Moderno, limpo | Plus Jakarta Sans 700 | Plus Jakarta Sans 400 |
| Técnico, afiado | Space Grotesk | Space Grotesk |
| Acolhedor | Lora | Nunito Sans |
| Expressivo | Fraunces | Outfit |
| Confiável, clássico | Libre Baskerville | Work Sans |

Passe as famílias escolhidas para `preparar_fontes.py --familias`. Nome do pacote é o nome em minúsculas com hífen (`plus-jakarta-sans`).

## 4. Componentes extras, quando o slide pedir

Não estão no gerador para manter o template enxuto. Se o conteúdo pedir, acrescente no CSS gerado, em pixel real de 1080:

**Pílula de tag**: fonte 30, padding 14px 32px, borda 2px `rgba(255,255,255,.12)`, raio 51px.

**Pílula riscada** (ferramenta ou processo que sai): mesma pílula com `text-decoration:line-through` e cor apagada. Boa em slide de comparação.

**Caixa de citação**: padding 44px, fundo `rgba(0,0,0,.25)`, borda 2px `rgba(255,255,255,.08)`, raio 32px, rótulo 30px apagado e frase 41px em itálico.

**Amostra de cor**: quadrado 86px, raio 20px, borda 2px translúcida. Só quando o assunto for identidade visual.

Regra geral: componente novo entra em pixel real, seguindo a escala da seção 2. Copiar tamanho de layout de 420px deixa tudo miúdo no PNG.
