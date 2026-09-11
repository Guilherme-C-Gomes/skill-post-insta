# post-insta

Skill do Claude que cria carrossel de Instagram ponta a ponta, da copy dos slides ao PNG 1080x1350 pronto para postar.

Fluxo fechado: briefing curto, copy dos slides, arte montada por gerador, preview no chat, correção slide a slide, export só depois de aprovação explícita, e os arquivos como entrega final separada.

Formato: carrossel 4:5, 1080x1350.

## Conteúdo

```
skills/post-insta/
  SKILL.md
  references/
    copy-slides.md
    estilos.md
    imagem.md
  scripts/
    preparar_fontes.py
    montar_carrossel.py
    exportar_slides.py
  assets/
    exemplo_conteudo.json
    fontes.css
```

## Como instalar

```bash
git clone https://github.com/Guilherme-C-Gomes/skill-post-insta.git
cp -r skill-post-insta/skills/post-insta ~/.claude/skills/
```

Depois é só chamar `/post-insta` numa sessão do Claude.

## Fronteira com outras skills

Estratégia de conteúdo e calendário ficam na `marketing-digital`. Foto e imagem gerada por IA ficam na `image`. Aqui o tema já vem definido e a skill produz o post, não a pauta. Legenda e hashtags saem daqui.
