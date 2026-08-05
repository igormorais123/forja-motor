# -*- coding: utf-8 -*-
"""Aumenta as fontes internas do SVG de um diagrama archify já renderizado.

Uso: python ajustar_fontes_diagrama.py <arquivo.html>
Reaplicar SEMPRE após regenerar o HTML com `archify render` (o render restaura
os tamanhos padrão do renderizador: título 11, sub-rótulo 9, rótulo de seta 8,
etiqueta 7). Este script só toca atributos font-size dentro do SVG, nunca o
CSS da página nem o renderizador do archify.
"""
import re
import sys

MAPA = {"11": "13", "9": "10.5", "8": "9.5", "7": "8.5"}


def main(caminho):
    html = open(caminho, encoding="utf-8").read()
    trocas = 0

    def sub(m):
        nonlocal trocas
        novo = MAPA.get(m.group(1))
        if novo:
            trocas += 1
            return f'font-size="{novo}"'
        return m.group(0)

    novo_html = re.sub(r'font-size="(\d+)"', sub, html)
    largura, n_larg = re.subn(r"max-width:\s*1200px", "max-width: 1780px", novo_html)
    novo_html = largura
    if trocas == 0 and n_larg == 0:
        print("nenhum ajuste pendente — arquivo já ajustado?")
        return
    open(caminho, "w", encoding="utf-8").write(novo_html)
    print(f"{trocas} atributos font-size ampliados e {n_larg} moldura(s) alargada(s) em {caminho}")


if __name__ == "__main__":
    main(sys.argv[1])
