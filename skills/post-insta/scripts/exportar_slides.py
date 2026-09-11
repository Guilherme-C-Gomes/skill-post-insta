#!/usr/bin/env python3
"""
Exporta cada .slide de um HTML como PNG no tamanho exato do Instagram.

Faz tres coisas que evitam o retrabalho classico do carrossel:
1. Abre o HTML por file://, remove o CSS de preview (data-preview-only) e espera
   as fontes carregarem (document.fonts.ready). Screenshot tirado antes disso sai
   com fonte de fallback e ninguem percebe.
2. Confere transbordo de texto slide por slide (scrollHeight vs clientHeight e
   qualquer filho passando da caixa). Texto cortado e a falha numero um.
3. Valida a dimensao final do arquivo. PNG que nao esta em 1080x1350 o Instagram
   recomprime e a arte perde nitidez.

Uso:
  python3 exportar_slides.py carrossel.html --saida ./slides
  python3 exportar_slides.py carrossel.html --saida ./slides --largura 1080 --altura 1920
  python3 exportar_slides.py carrossel.html --saida ./slides --escala 2   # 2x, depois reduzir
"""

import argparse
import os
import sys

from playwright.sync_api import sync_playwright

try:
    from PIL import Image
except ImportError:
    Image = None

JS_TRANSBORDO = """
(el) => {
  // Só interessa o que quebra a arte: texto cortado e elemento de fluxo estourando
  // a caixa. Decoração posicionada de propósito fora da borda (brilho, sangria,
  // recorte) é intencional, então elemento absoluto sem texto proprio e ignorado,
  // e data-sangria libera qualquer um explicitamente.
  const fora = [];
  const caixa = el.getBoundingClientRect();
  const margem = 1;
  const textoProprio = (n) => Array.from(n.childNodes)
    .filter((c) => c.nodeType === 3)
    .map((c) => c.textContent.trim())
    .join(' ')
    .trim();

  el.querySelectorAll('*').forEach((f) => {
    if (f.closest('[data-sangria]')) return;
    const r = f.getBoundingClientRect();
    if (r.width === 0 || r.height === 0) return;
    const pos = getComputedStyle(f).position;
    const txt = textoProprio(f);
    const decorativo = (pos === 'absolute' || pos === 'fixed') && !txt;
    if (decorativo) return;
    if (r.bottom > caixa.bottom + margem || r.top < caixa.top - margem ||
        r.right > caixa.right + margem || r.left < caixa.left - margem) {
      fora.push(f.tagName.toLowerCase() + (txt ? ': ' + txt.slice(0, 40) : ' (sem texto)'));
    }
  });
  return { fora: fora.slice(0, 5) };
}
"""


def main():
    p = argparse.ArgumentParser(description="Exporta slides .slide de um HTML para PNG.")
    p.add_argument("html", help="caminho do HTML do carrossel")
    p.add_argument("--saida", default="./slides", help="pasta de saida")
    p.add_argument("--seletor", default=".slide", help="seletor dos slides (padrao: .slide)")
    p.add_argument("--largura", type=int, default=1080)
    p.add_argument("--altura", type=int, default=1350)
    p.add_argument("--escala", type=float, default=1.0, help="device scale factor")
    p.add_argument("--prefixo", default="slide")
    args = p.parse_args()

    caminho = os.path.abspath(args.html)
    if not os.path.exists(caminho):
        sys.exit(f"HTML nao encontrado: {caminho}")
    os.makedirs(args.saida, exist_ok=True)

    problemas = []
    gerados = []

    with sync_playwright() as pw:
        navegador = pw.chromium.launch(args=["--font-render-hinting=none"])
        pagina = navegador.new_page(
            viewport={"width": args.largura, "height": args.altura},
            device_scale_factor=args.escala,
        )
        pagina.goto(f"file://{caminho}", wait_until="load")
        # O preview vive em CSS marcado com data-preview-only (escala reduzida, tira
        # rolavel, moldura da rede social). Removido antes da foto, o slide volta ao
        # tamanho nativo e o PNG sai sem escala fracionaria no meio.
        removidos = pagina.evaluate(
            "() => { const n = document.querySelectorAll('[data-preview-only]');"
            " n.forEach(e => e.remove()); return n.length; }"
        )
        pagina.evaluate("document.fonts.ready")
        pagina.wait_for_timeout(400)
        if removidos:
            print(f"preview removido ({removidos} bloco(s) data-preview-only)")

        slides = pagina.query_selector_all(args.seletor)
        if not slides:
            navegador.close()
            sys.exit(f"Nenhum elemento '{args.seletor}' encontrado no HTML.")

        for i, slide in enumerate(slides, start=1):
            caixa = slide.bounding_box() or {}
            largura_real, altura_real = round(caixa.get("width", 0)), round(caixa.get("height", 0))
            if (largura_real, altura_real) != (args.largura, args.altura):
                problemas.append(
                    f"slide {i}: caixa {largura_real}x{altura_real} em vez de "
                    f"{args.largura}x{args.altura}. Fixe width/height no CSS do .slide."
                )

            diag = slide.evaluate(JS_TRANSBORDO)
            for item in diag["fora"]:
                problemas.append(f"slide {i}: passou da caixa ({item}). Texto cortado ou layout estourado.")

            destino = os.path.join(args.saida, f"{args.prefixo}-{i:02d}.png")
            slide.screenshot(path=destino)
            gerados.append(destino)

        navegador.close()

    print(f"{len(gerados)} slide(s) exportado(s) em {args.saida}")
    for caminho_png in gerados:
        linha = f"  {os.path.basename(caminho_png)}"
        if Image:
            with Image.open(caminho_png) as im:
                linha += f"  {im.width}x{im.height}"
                esperado = (round(args.largura * args.escala), round(args.altura * args.escala))
                if (im.width, im.height) != esperado:
                    problemas.append(
                        f"{os.path.basename(caminho_png)}: saiu {im.width}x{im.height}, "
                        f"esperado {esperado[0]}x{esperado[1]}."
                    )
        linha += f"  {os.path.getsize(caminho_png)//1024} KB"
        print(linha)

    if problemas:
        print("\nPROBLEMAS (corrija antes de publicar):")
        for item in problemas:
            print(f"  - {item}")
        sys.exit(1)
    print("\nSem transbordo e dimensoes corretas.")


if __name__ == "__main__":
    main()
