# Imagem nos slides: quando, qual modelo, qual prompt

## 1. O slide precisa de imagem?

Na maioria dos casos, não. Carrossel de tipografia limpa performa bem e não corre risco de foto genérica de banco de imagem enfraquecer a peça.

Precisa de imagem quando:
- O slide mostra prova visual (print de painel, gráfico, antes e depois).
- O gancho depende de uma cena concreta que o texto não entrega.
- A capa precisa de peso visual e a tipografia sozinha ficou vazia.

Não precisa quando o objetivo é ilustrar conceito abstrato. Foto de aperto de mão, martelo de juiz e balança da justiça em slide sobre funil é ruído.

## 2. Interface de produto: nunca por IA

Modelo de imagem inventa interface. Tela de CRM gerada por IA sai com campo que não existe, texto ilegível e layout que não é o do produto, e isso assinado pela Eyes Tech destrói credibilidade técnica.

Para mostrar tela:
1. Print real, capturado em 2x.
2. Recorte da parte que importa, não a janela inteira.
3. Anotação por cima em HTML (seta, caixa, rótulo), no mesmo sistema de cor da marca.
4. Se o print tiver dado de cliente, substitua por dado fictício antes. Nome, telefone, e-mail e valor de contrato não vão para post.

## 3. Escolha do modelo

| Precisa de | Modelo | Por quê |
|---|---|---|
| Texto legível dentro da imagem | Ideogram 3.0 | melhor tipografia entre os modelos |
| Foto realista, cena de escritório | Flux Pro, Gemini Image | fotorrealismo e coerência de luz |
| Consistência entre várias imagens | Flux (referência múltipla), Gemini Nano Banana Pro | mantém personagem e estilo |
| Ilustração ou vetor de marca | Recraft V3 | vetor e consistência de traço |
| Editar imagem existente | Gemini, Flux Kontext | edição no lugar, sem refazer |
| Volume a custo baixo | Flux Schnell, Gemini Flash | rascunho e variação |

Regra prática para carrossel: texto do slide é sempre HTML, nunca dentro da imagem gerada. Imagem entra como fundo ou como elemento, e o texto por cima em CSS. Isso resolve legibilidade, permite corrigir uma palavra sem regenerar arte, e dispensa depender do modelo acertar acento em português.

## 4. Estrutura do prompt

Sujeito + cenário + estilo + luz + composição + técnica.

```
Advogada de 40 anos revisando documento em mesa de escritório,
luz natural lateral suave, profundidade de campo rasa,
fotografia editorial corporativa, tons frios,
espaço negativo no terço superior para texto, 4:5, alta resolução
```

O trecho de espaço negativo é o que mais importa aqui: sem ele a imagem volta com o assunto no centro e não sobra área para a headline. Peça o vazio onde o texto vai entrar.

Erros que voltam sempre:
- Prompt vago ("imagem corporativa").
- Esquecer a proporção. Sempre declare 4:5.
- Pedir texto complexo na imagem. Texto vai por cima, em HTML.
- Não declarar estilo. "Fotorrealista", "ilustração plana" e "render 3D" mudam tudo.

Para prompt por modelo em detalhe, a skill `image` tem `references/ai-image-prompting.md`.

## 5. Fluxo quando a foto ainda não existe

Não invente arte e não deixe o slide vazio esperando:

1. Monte o carrossel com o slide sem `imagem`, funcionando em tipografia.
2. Entregue, junto do preview, o prompt pronto para a pessoa gerar onde ela já tem crédito (Gemini, Ideogram, Midjourney).
3. Quando o arquivo chegar em `/mnt/user-data/uploads`, acrescente `"imagem": "/mnt/user-data/uploads/arquivo.jpg"` no slide do JSON e rode o gerador de novo.

O gerador embute a imagem como data URI, cobre com véu escuro em `rgba(13,12,13,.62)` e sobe o conteúdo para cima dela. Se o texto ainda ficar difícil de ler, escureça o véu antes de mexer no texto: contraste é problema de fundo, não de tamanho de fonte.

## 6. Peso do arquivo

PNG de slide fica entre 60 KB e 250 KB, e isso está certo. Slide com foto passa de 1 MB fácil: reduza a foto antes de embutir, porque o base64 de uma imagem de 4 MB engorda o HTML em 5 MB e o preview fica lento.

```bash
convert foto.jpg -resize 1080x1350^ -gravity center -extent 1080x1350 -quality 82 foto_pronta.jpg
```

O Instagram recomprime tudo de qualquer forma, então PNG de 250 KB em 1080x1350 já é o teto útil. Exportar em 2x e reduzir depois só faz sentido se houver print de tela fino no slide.
