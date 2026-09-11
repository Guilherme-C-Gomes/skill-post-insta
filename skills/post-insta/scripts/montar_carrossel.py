#!/usr/bin/env python3
"""
Monta o HTML do carrossel Eyes Tech a partir de um JSON de conteudo.

Existe para eliminar de uma vez a familia de erros que mais custa tempo aqui:
HTML escrito por heredoc de shell (o $ e o backtick corrompem base64), caminho
relativo de imagem que quebra fora da pasta, contagem de slides escrita na mao
que desatualiza, e token de cor deixado como nome de variavel no CSS final.

Template unico: design system Eyes Tech, carrossel 4:5.

Slides sao construidos no tamanho nativo (1080x1350) e o preview e apenas um
CSS marcado com data-preview-only, que o exportador remove antes de fotografar.
Assim preview e PNG saem do mesmo DOM, sem escala fracionaria no meio.

Uso:
  python3 montar_carrossel.py conteudo.json --saida carrossel.html
  python3 montar_carrossel.py conteudo.json --saida carrossel.html --fontes assets/fontes.css
"""

import argparse
import base64
import html
import json
import os
import sys

LARGURA, ALTURA = 1080, 1350
ESCALA_PREVIEW = 0.3667  # 1080 -> 396px

PALETA = {
    "azul": "#00B7FF", "azul_escuro": "#0077A8",
    "fundo": "#0D0C0D", "texto": "#FFFFFF", "texto_suave": "#D7DBDE",
    "apagado": "#9AA0A6", "grade": "rgba(0,183,255,.10)",
}

MIMES = {b"\x89PNG": "image/png", b"\xff\xd8\xff": "image/jpeg", b"RIFF": "image/webp", b"GIF8": "image/gif"}


def embutir(caminho):
    """Le a imagem e devolve data URI. Confere o formato pelos bytes, porque
    extensao mente: .png contendo JPEG quebra a renderizacao sem erro visivel."""
    if not caminho:
        return None
    if str(caminho).startswith("data:"):
        return caminho
    if not os.path.exists(caminho):
        raise SystemExit(f"Imagem nao encontrada: {caminho}")
    dados = open(caminho, "rb").read()
    mime = next((m for assinatura, m in MIMES.items() if dados[:len(assinatura)] == assinatura), None)
    if not mime:
        raise SystemExit(f"Formato de imagem nao reconhecido em {caminho}")
    return f"data:{mime};base64,{base64.b64encode(dados).decode()}"


def e(txto):
    """Escapa texto, preservando quebra de linha simples marcada com //."""
    return html.escape(str(txto or "")).replace("//", "<br>")


# ----------------------------------------------------------------------------- estilo Eyes Tech

def css_eyes_tech(p):
    return f"""
.slide{{width:{LARGURA}px;height:{ALTURA}px;position:relative;overflow:hidden;
  background:{p['fundo']};color:{p['texto']};padding:96px 88px;display:flex;flex-direction:column;
  background-image:linear-gradient({p['grade']} 1px,transparent 1px),linear-gradient(90deg,{p['grade']} 1px,transparent 1px);
  background-size:120px 120px;font-family:'Inter',Carlito,'Liberation Sans',sans-serif}}
.slide .brilho{{position:absolute;top:-260px;right:-160px;width:760px;height:760px;border-radius:50%;
  background:radial-gradient(circle,rgba(0,183,255,.22) 0%,rgba(0,183,255,0) 70%)}}
.marca{{font-family:'Poppins',sans-serif;font-weight:700;font-size:40px;letter-spacing:-.02em;position:relative}}
.marca span{{color:{p['azul']}}}
.corpo{{flex:1;display:flex;flex-direction:column;justify-content:center;gap:36px;position:relative}}
.filete{{height:6px;width:180px;background:{p['azul']};border-radius:3px}}
.kicker{{font-size:30px;font-weight:600;color:{p['azul']};text-transform:uppercase;letter-spacing:.12em}}
h1{{font-family:'Poppins',sans-serif;font-weight:700;font-size:104px;line-height:1.02;letter-spacing:-.03em;margin:0}}
h2{{font-family:'Poppins',sans-serif;font-weight:600;font-size:72px;line-height:1.08;letter-spacing:-.02em;margin:0}}
.slide p{{font-size:40px;line-height:1.45;color:{p['texto_suave']};margin:0}}
.lista{{display:flex;flex-direction:column;gap:28px}}
.item{{display:flex;gap:24px;align-items:flex-start}}
.num{{font-family:'Poppins',sans-serif;font-weight:700;font-size:34px;color:{p['fundo']};background:{p['azul']};
  min-width:62px;height:62px;border-radius:16px;display:flex;align-items:center;justify-content:center;flex:0 0 auto}}
.item p{{font-size:36px}}
.cta{{background:{p['azul']};color:{p['fundo']};font-family:'Poppins',sans-serif;font-weight:700;
  font-size:38px;padding:28px 44px;border-radius:20px;align-self:flex-start}}
.rodape{{display:flex;justify-content:space-between;align-items:flex-end;position:relative;
  font-size:28px;color:{p['apagado']}}}
.foto{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;z-index:0}}
.veu{{position:absolute;inset:0;background:rgba(13,12,13,.62);z-index:1}}
.slide.com-foto>*:not(.foto):not(.veu){{position:relative;z-index:2}}
"""


def slide_eyes_tech(s, i, total, p):
    tipo = s.get("tipo", "conteudo")
    foto = embutir(s.get("imagem"))
    partes = ['<div class="brilho"></div>'] if not foto else []
    if foto:
        partes = [f'<img class="foto" src="{foto}">', '<div class="veu"></div>']
    partes.append('<div class="marca"><span>eyes</span> tech</div>')

    corpo = []
    if s.get("kicker"):
        corpo.append('<div class="filete"></div>')
        corpo.append(f'<div class="kicker">{e(s["kicker"])}</div>')
    if s.get("titulo"):
        tag = "h1" if tipo == "capa" else "h2"
        corpo.append(f'<{tag}>{e(s["titulo"])}</{tag}>')
    if s.get("texto"):
        corpo.append(f'<p>{e(s["texto"])}</p>')
    if s.get("itens"):
        linhas = []
        for n, item in enumerate(s["itens"], start=1):
            marcador = f'<div class="num">{n}</div>' if tipo in ("passos", "lista") else ""
            linhas.append(f'<div class="item">{marcador}<p>{e(item)}</p></div>')
        corpo.append('<div class="lista">' + "".join(linhas) + "</div>")
    if s.get("cta"):
        corpo.append(f'<div class="cta">{e(s["cta"])}</div>')

    partes.append('<div class="corpo">' + "".join(corpo) + "</div>")
    dica = s.get("dica", "arrasta para o lado" if i < total else "salva para depois")
    partes.append(f'<div class="rodape"><span>{e(dica)}</span><span>{i}/{total}</span></div>')
    classe = "slide com-foto" if foto else "slide"
    return f'<section class="{classe}">' + "".join(partes) + "</section>"


# ----------------------------------------------------------------------------- montagem

CSS_PREVIEW = f"""
body{{background:#171717;margin:0;padding:20px;font-family:'Inter',sans-serif}}
.tira{{display:flex;gap:16px;overflow-x:auto;scroll-snap-type:x mandatory;padding:4px 0 14px}}
.moldura{{flex:0 0 auto;width:{round(LARGURA*ESCALA_PREVIEW)}px;height:{round(ALTURA*ESCALA_PREVIEW)}px;
  overflow:hidden;border-radius:16px;scroll-snap-align:center;box-shadow:0 10px 30px rgba(0,0,0,.45)}}
.moldura>.slide{{transform:scale({ESCALA_PREVIEW});transform-origin:top left}}
.aviso{{color:#8b8b8b;font-size:13px;padding:6px 2px}}
"""


def montar(dados, fontes_css):
    if dados.get("estilo") and dados["estilo"] != "eyes-tech":
        raise SystemExit(
            f"estilo '{dados['estilo']}' nao existe mais nesta skill. "
            "O unico template e o design system Eyes Tech: remova o campo 'estilo' do JSON."
        )
    p = PALETA
    slides = dados.get("slides") or []
    if not slides:
        raise SystemExit("JSON sem slides")
    total = len(slides)

    corpo = [slide_eyes_tech(s, i, total, p) for i, s in enumerate(slides, start=1)]
    molduras = "".join(f'<div class="moldura">{bloco}</div>' for bloco in corpo)

    return f"""<!DOCTYPE html>
<html lang="pt-BR"><head><meta charset="utf-8">
<title>{e(dados.get('titulo', 'Carrossel'))}</title>
<style>{fontes_css}</style>
<style>*{{box-sizing:border-box}}{css_eyes_tech(p)}</style>
<style data-preview-only>{CSS_PREVIEW}</style>
</head><body>
<div class="aviso" data-preview-only>Pre-visualizacao a {int(ESCALA_PREVIEW*100)}%. Arraste para o lado. O PNG sai em {LARGURA}x{ALTURA}.</div>
<div class="tira">{molduras}</div>
</body></html>"""


def main():
    ap = argparse.ArgumentParser(description="Monta o HTML do carrossel a partir de um JSON.")
    ap.add_argument("json", help="arquivo de conteudo")
    ap.add_argument("--saida", default="carrossel.html")
    ap.add_argument("--fontes", default=None, help="CSS de fontes embutidas (preparar_fontes.py)")
    args = ap.parse_args()

    dados = json.load(open(args.json, encoding="utf-8"))
    fontes_css = ""
    if args.fontes:
        if not os.path.exists(args.fontes):
            sys.exit(f"CSS de fontes nao encontrado: {args.fontes}. Rode preparar_fontes.py primeiro.")
        fontes_css = open(args.fontes, encoding="utf-8").read()
    else:
        print("AVISO: sem --fontes, o PNG vai sair em fonte de sistema (Carlito).")

    html_final = montar(dados, fontes_css)
    with open(args.saida, "w", encoding="utf-8") as f:
        f.write(html_final)

    print(f"HTML gerado: {args.saida}  ({len(html_final)//1024} KB, {len(dados['slides'])} slides)")
    if dados.get("legenda"):
        print("\nLEGENDA:\n" + dados["legenda"])
    if dados.get("hashtags"):
        print("\n" + " ".join(dados["hashtags"]))


if __name__ == "__main__":
    main()
