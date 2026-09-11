---
name: post-insta
description: "Cria carrossel de Instagram ponta a ponta, da copy dos slides ao PNG 1080x1350 pronto para postar, no design system Eyes Tech. Preview primeiro, correcao slide a slide, export so depois de aprovacao explicita, e os arquivos como entrega final separada."
---

# Post de Instagram: carrossel

Fluxo fechado: briefing curto, copy dos slides, arte montada por gerador, preview no chat, correção slide a slide, export em 1080x1350 e entrega dos arquivos.

Template único: design system Eyes Tech, fundo escuro, azul como acento.

Formato: carrossel 4:5, 1080x1350. Story e post único de feed não estão no escopo. Se pedirem, diga em uma linha e ofereça adaptar (o exportador aceita outras dimensões, mas os dois templates são desenhados para 4:5).

Fronteira com outras skills, para não haver duas donas do mesmo pedido:
- Estratégia de conteúdo, calendário, ângulos de campanha e plano de mídia são da `marketing-digital`. Aqui o tema já vem definido.
- Foto e imagem gerada por IA são da `image`. Aqui entra o prompt pronto e o arquivo, não a geração.
- Se o pedido for "me dá 5 ideias de post", isso é `content-strategy` ou `marketing-digital`. Esta skill produz o post, não a pauta.

Legenda e hashtags saem daqui, porque carrossel sem legenda não é entregável. Variação de ângulo e teste de copy continuam na `marketing-digital`.

## A regra que mais quebra esta skill

**Preview primeiro. Arquivo só no fim, como entrega separada. O que separa os dois é um sim explícito.**

1. Toda rodada termina em preview, nunca em PNG.
2. Depois do preview, pergunte o que ajustar e espere resposta.
3. Exporte só com aprovação inequívoca: "pode exportar", "aprovado", "manda os arquivos".
4. Os PNGs são o fechamento do trabalho, não mais uma iteração.

O que **não** é aprovação de export, por mais que soe como seguir em frente:

| A pessoa diz | O que significa de verdade |
|---|---|
| "vamos fazer por aqui mesmo" | voltar de um desvio, não aprovar a arte |
| "esquece isso, continua" | abandonar um caminho paralelo |
| "pode seguir" / "vai" | seguir o fluxo, que pode ser só o próximo preview |
| um ajuste pedido e atendido | volte ao preview, não pule para o export |
| silêncio depois do preview | nada; pergunte de novo |

Na dúvida, gere o preview e pergunte. Preview custa segundos. Export entregue cedo demais deixa arquivo velho na mão da pessoa, e ela perde tempo descobrindo qual versão vale.

## O que a arte precisa saber antes de começar

Pergunte só o que falta e o que muda o resultado. Marca Eyes Tech já está definida (cores, logotipo, tom), então não pergunte cor nem fonte quando o post for da Eyes Tech.

Bloqueante:
1. Tema do carrossel, ou o texto de origem.
2. Número de slides, se a pessoa tiver preferência. Padrão: 7 slides, ou o que a sequência escolhida pedir.

Não bloqueante, assuma e sinalize em uma linha: idioma português do Brasil, sequência padrão de 7 slides, sem foto de fundo.

Quando o post for de outra marca, aí sim colete nome, handle, cor primária, foto de perfil e tom. A derivação de paleta a partir de uma cor primária única está em `references/estilos.md`.

## Fluxo

### 1. Copy dos slides

Escreva a copy antes de pensar em layout. Slide bonito com copy fraca não salva post.

Escolha a sequência (padrão, listicle, tutorial, comparação) e o formato de gancho da capa em `references/copy-slides.md`. Duas regras que valem sempre: o slide 1 existe para parar o dedo e nunca começa com o nome da marca, e cada slide carrega uma ideia só, terminada, sem frase cortada no meio para o slide seguinte.

Leia a seção de OAB nesse mesmo arquivo antes de escrever gancho. A Eyes Tech fala com escritório de advocacia, e vários dos formatos de gancho que funcionam em outros nichos ("esse post gerou 4.200 seguidores", "fature X") são promessa de resultado, que não entra em material desta casa.

Texto em português vai com acento, sempre. Script Python com docstring sem acento não é motivo para escrever o conteúdo do post sem acento.

### 2. Conteúdo em JSON

Todo o conteúdo vai para um JSON, nunca direto no HTML. O esquema completo está em `references/estilos.md`.

```json
{
  "slides": [
    {"tipo": "capa", "kicker": "Funil de escritório",
     "titulo": "O caso não sumiu.//Ele esfriou//esperando resposta.",
     "texto": "Onde o lead se perde entre o primeiro contato e a consulta."},
    {"tipo": "passos", "titulo": "Três pontos onde o caso esfria",
     "itens": ["...", "...", "..."]},
    {"tipo": "conteudo", "titulo": "...", "texto": "...", "cta": "Comentários abertos"}
  ],
  "legenda": "...",
  "hashtags": ["#advocacia", "#gestaojuridica"]
}
```

O JSON é o que torna a correção barata: ajustar o slide 3 é editar um objeto e rodar o gerador de novo, não reescrever a arte. Guarde o JSON junto do HTML durante toda a conversa.

`//` dentro de um texto vira quebra de linha. Serve para controlar onde a headline quebra, que é decisão de composição e não de sorte.

### 3. Montar e mostrar

```bash
# uma vez por sessão, se assets/fontes.css ainda não existir
python3 scripts/preparar_fontes.py --familias inter poppins --pesos 400 600 700 --saida assets/fontes.css

python3 scripts/montar_carrossel.py conteudo.json --saida /mnt/user-data/outputs/carrossel.html --fontes assets/fontes.css
```

Apresente o HTML com `present_files`. Ele abre como tira rolável, slides em escala reduzida, e é assim que a pessoa revisa sem gastar export.

Olhe você mesmo antes de mostrar: tire um screenshot da tira com Playwright e confira. Texto vazando ou elemento colidindo se corrige antes de chegar na pessoa, não depois que ela aponta.

### 4. Revisão, antes de qualquer export

Pergunte: **"quais slides precisam de ajuste antes de exportar?"**

Corrija só o que foi citado. Não refaça o carrossel inteiro por causa de um slide, a menos que a direção mude de verdade. Refazer tudo joga fora as decisões que já estavam aprovadas e obriga a pessoa a revisar de novo o que ela já tinha aceito.

Não exporte sem aprovação explícita. Preview aprovado é o gate, e a tabela lá em cima lista o que costuma ser confundido com aprovação.

Quando o ajuste vier como print com marcação, confirme o que cada marca aponta antes de apagar. Seta em cima de um canto pode estar mirando o elemento decorativo, não o número atrás dele. Errar isso custa duas rodadas: remova o que foi apontado, liste em uma linha o que saiu, e deixe a pessoa corrigir a leitura.

Se a remoção tirar alguma função da peça (o contador, por exemplo, que sinaliza que há mais slides adiante), diga em uma linha e siga com o pedido mesmo assim.

### 5. Export

```bash
python3 scripts/exportar_slides.py /mnt/user-data/outputs/carrossel.html --saida /mnt/user-data/outputs/slides
```

O script remove o CSS de preview, espera as fontes carregarem, fotografa cada `.slide` em 1080x1350, confere transbordo de texto elemento por elemento e valida a dimensão de cada arquivo. Se ele apontar transbordo, corrija antes de entregar: texto cortado só aparece depois de publicado, quando já não dá para consertar.

### 6. Entrega

Chame `present_files` com os PNGs na ordem, o slide 1 primeiro. Sem isso a pessoa não tem como baixar nada, e no celular não aparece nem o cartão do arquivo.

Depois dos arquivos, entregue a legenda e as hashtags em texto no chat, para copiar e colar. Ordem de postagem dos slides e nada mais: sem parágrafo de encerramento explicando o que foi feito.

Quando o post citar número que veio de fonte externa, diga em uma linha que o dado não é da casa e de onde veio. Número sem procedência vira promessa.

## Canva: o que dá e o que não dá

Quando pedirem o carrossel dentro do Canva, saiba de antemão onde cada caminho trava, em vez de descobrir no meio:

- **Subir os PNGs pelo conector do Canva não funciona.** `upload-asset-from-url` exige URL pública, e publicar arte de cliente em hospedagem aberta não é opção. Não ofereça isso como saída.
- **Arquivo no computador da pessoa funciona.** Exporte aqui, grave numa pasta conectada e ela arrasta para o Canva. Preserva a arte exata.
- **Montar nativo no Canva funciona e fica totalmente editável.** `read-design` com `open_transaction`, depois `edit-design` com `insert_shape` (path SVG, fill, stroke, corner_rounding, rotation), `add_text`, `format_text` e `add_page` (largura, altura e cor de fundo). Texto entra sem formatação: é preciso uma segunda passada de `format_text` usando os locator_id devolvidos.
- **O que não atravessa para o Canva:** textura de grão (é imagem), gradiente radial e família tipográfica (a API não define fonte). Diga isso antes de montar, não depois.

Qualquer que seja o caminho, ele só começa depois da arte aprovada no preview.

## Como este ambiente quebra carrossel (e o que o gerador já resolve)

Estes quatro pontos custaram tempo antes. Estão resolvidos nos scripts, e a explicação fica aqui para que ninguém "conserte" de volta:

**Fonte por link não carrega.** O container não alcança o Google Fonts. `@import` de fonte cai silenciosamente para fonte de sistema, e o pior é que o HTML abre certo no navegador da pessoa (que tem rede) e sai errado no PNG. `preparar_fontes.py` baixa por npm (`@fontsource/*`, que está liberado) e embute em base64. O export espera `document.fonts.ready`, não um `sleep` de 3 segundos.

**Slide montado em 420px e escalado 2,57x sai borrado.** Escala fracionária põe borda de 1px em 2,57px e desalinha meio pixel em tudo. O gerador monta no tamanho nativo, 1080x1350, com tipografia em escala real, e o preview é só um `<style data-preview-only>` com `transform: scale(0.3667)` que o exportador remove antes de fotografar. Preview e PNG saem do mesmo DOM, sem intermediário.

**HTML escrito por heredoc de shell corrompe base64.** `$` e acento grave são interpolados e a imagem quebra sem erro visível. Por isso o HTML sai de `montar_carrossel.py` (Python) e nunca de `echo` ou heredoc.

**Caminho relativo de imagem quebra.** Imagem entra sempre como data URI. O gerador identifica o formato pelos bytes do arquivo, não pela extensão, porque `.png` contendo JPEG é comum e o MIME errado não renderiza.

Mais um do ambiente: arquivo que a pessoa sobe fica em `/mnt/user-data/uploads` (somente leitura) e o que ela precisa baixar tem que ir para `/mnt/user-data/outputs` e ser apresentado. Chromium e Playwright já estão instalados: não tente `playwright install`, porque o download é bloqueado pela rede.

## Densidade visual

Quando a referência que a pessoa mandar for densa (tipografia gigante, recorte colado com fita, badge, textura) e o template padrão parecer vazio ao lado dela, ela vai dizer que falta elemento. Dá para densificar sem sair da identidade, em três camadas:

- **Fundo:** grão por `feTurbulence` em data URI, grade, mancha radial, número do slide gigante como marca d'água.
- **Rótulo:** badge numerada, pílula com ponto, filete.
- **Conteúdo:** um elemento forte por slide, alternando entre número gigante, diagrama de mecanismo em SVG, medidor, pílulas comparadas e recorte colado.

Composição da referência entra; paleta não. Fundo `#0D0C0D` e azul `#00B7FF` como acento continuam valendo, mesmo que a referência seja vermelha. Diga isso quando a referência for de outra marca.

Elemento novo vai em pixel real de 1080, nunca em escala de preview. Marque decoração que sangra com `data-sangria`, senão o verificador de transbordo acusa falso positivo.

## Imagem e foto nos slides

Slide com foto de fundo pede véu escuro por cima, senão o texto morre. O gerador já faz isso: basta `"imagem": "/mnt/user-data/uploads/foto.jpg"` no slide.

Quando o slide precisar de uma foto que não existe, não invente arte: entregue o prompt pronto e monte o slide com o espaço reservado. Qual modelo pedir para cada caso, e como escrever o prompt, está em `references/imagem.md`. Nunca use imagem gerada por IA para mostrar interface de produto ou tela de CRM: o modelo inventa a interface e o resultado é uma tela que não existe assinada pela Eyes Tech. Vale o mesmo para rosto de pessoa em post de autoridade técnica.

## Checklist antes de entregar

- Preview mostrado e aprovado explicitamente antes de qualquer export.
- Capa não começa com o nome da marca e para o dedo em menos de um segundo.
- Uma ideia por slide, nenhuma frase cortada para o slide seguinte.
- Nenhuma promessa de resultado, nenhum comparativo com concorrente, nada que induza escritório a captação indevida.
- Número citado tem procedência declarada.
- Export sem aviso de transbordo, todos os arquivos em 1080x1350.
- PNGs apresentados na ordem, com o slide 1 primeiro.
- Legenda e hashtags entregues junto.

## Arquivos de apoio

- `references/estilos.md`: esquema do JSON, tokens e componentes do design system Eyes Tech, derivação de paleta quando o post for de outra marca.
- `references/copy-slides.md`: sequências de slide, formatos de gancho permitidos e proibidos, legenda, hashtags, OAB.
- `references/imagem.md`: quando o slide precisa de foto, escolha de modelo e prompt pronto.
- `scripts/preparar_fontes.py`: baixa fontes e gera CSS embutido. Uma vez por sessão.
- `scripts/montar_carrossel.py`: JSON de conteúdo para HTML.
- `scripts/exportar_slides.py`: HTML para PNG 1080x1350, com checagem de transbordo.
- `assets/exemplo_conteudo.json`: JSON de referência, com os quatro tipos de slide.