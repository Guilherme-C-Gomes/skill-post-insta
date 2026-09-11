#!/usr/bin/env python3
"""
Baixa fontes via npm (@fontsource/*) e gera um CSS com @font-face embutido em base64.

Por que base64 e nao link do Google Fonts: o container que exporta o PNG nao tem rede
para fora, entao fonte por URL nao carrega e o Chromium cai para uma fonte de sistema
sem avisar. O sintoma e traicoeiro, porque o HTML abre bonito no navegador da pessoa
(que tem rede) e sai errado no PNG. CSS embutido resolve os dois lados de uma vez.

Uso:
  python3 preparar_fontes.py --familias inter poppins --pesos 400 600 700 --saida assets/fontes.css
"""

import argparse
import base64
import json
import os
import shutil
import subprocess
import tarfile
import tempfile

FALLBACK_LOCAL = "Carlito, 'Liberation Sans', DejaVu Sans, sans-serif"


def baixar(familia, tmp):
    """npm pack tras o tarball do pacote sem instalar nada global."""
    pacote = f"@fontsource/{familia}"
    r = subprocess.run(["npm", "pack", pacote, "--silent"], cwd=tmp,
                       capture_output=True, text=True, timeout=300)
    if r.returncode != 0:
        raise RuntimeError(f"npm pack falhou para {pacote}: {r.stderr.strip()[:200]}")
    tgz = os.path.join(tmp, r.stdout.strip().splitlines()[-1])
    destino = os.path.join(tmp, familia)
    with tarfile.open(tgz) as t:
        t.extractall(destino, filter="data")
    return os.path.join(destino, "package", "files")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--familias", nargs="+", default=["inter"])
    p.add_argument("--pesos", nargs="+", default=["400", "600", "700"])
    p.add_argument("--subset", default="latin")
    p.add_argument("--saida", default="assets/fontes.css")
    args = p.parse_args()

    if not shutil.which("npm"):
        raise SystemExit("npm nao encontrado. Use as fontes locais: " + FALLBACK_LOCAL)

    css = ["/* Gerado por preparar_fontes.py. Fontes embutidas em base64: nao depende de rede. */"]
    relatorio = []

    with tempfile.TemporaryDirectory() as tmp:
        for familia in args.familias:
            pasta = baixar(familia, tmp)
            nome_css = familia.replace("-", " ").title()
            for peso in args.pesos:
                arquivo = os.path.join(pasta, f"{familia}-{args.subset}-{peso}-normal.woff2")
                if not os.path.exists(arquivo):
                    relatorio.append(f"  faltou: {familia} {peso} ({args.subset})")
                    continue
                b64 = base64.b64encode(open(arquivo, "rb").read()).decode()
                css.append(
                    "@font-face{"
                    f"font-family:'{nome_css}';font-style:normal;font-weight:{peso};"
                    "font-display:block;"
                    f"src:url(data:font/woff2;base64,{b64}) format('woff2');"
                    "}"
                )
                relatorio.append(f"  ok: {familia} {peso} ({len(b64)//1024} KB em base64)")

    os.makedirs(os.path.dirname(args.saida) or ".", exist_ok=True)
    with open(args.saida, "w", encoding="utf-8") as f:
        f.write("\n".join(css) + "\n")

    print(f"CSS gerado em {args.saida}")
    print("\n".join(relatorio))
    print(f"\nFallback local, se algo faltar: {FALLBACK_LOCAL}")
    print(json.dumps({"familias": args.familias, "pesos": args.pesos}, ensure_ascii=False))


if __name__ == "__main__":
    main()
