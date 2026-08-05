"""Render the FORJA Mermaid atlas to a self-contained HTML document."""

from __future__ import annotations

import argparse
import html
import re
import shutil
import subprocess
from pathlib import Path

from bs4 import BeautifulSoup
from markdown_it import MarkdownIt


ROOT = Path(__file__).resolve().parent
DEFAULT_SOURCE = ROOT / "reports" / "ATLAS_VISUAL_FORJA_ATUAL_E_PSO_PET_2026-07-11.md"
DEFAULT_OUTPUT = ROOT / "reports" / "ATLAS_VISUAL_FORJA_ATUAL_E_PSO_PET_2026-07-11.html"
FRIENDLY_OUTPUT = ROOT / "reports" / "FORJA_EXPLICADA_PARA_ADVOGADOS.html"


def slugify(value: str) -> str:
    normalized = value.casefold()
    normalized = re.sub(r"[^a-z0-9à-ÿ]+", "-", normalized, flags=re.IGNORECASE)
    return normalized.strip("-") or "secao"


def mermaid_command() -> str:
    command = shutil.which("mmdc.cmd") or shutil.which("mmdc")
    if not command:
        raise RuntimeError("mermaid-cli (mmdc) não localizado")
    return command


def namespace_svg_ids(svg: str, diagram_index: int) -> str:
    """Prevent inline Mermaid SVGs from sharing marker, clip-path and CSS IDs."""
    ids = set(re.findall(r'\bid="([^"]+)"', svg))
    for original in sorted(ids, key=len, reverse=True):
        namespaced = f"d{diagram_index:02d}-{original}"
        svg = svg.replace(f'id="{original}"', f'id="{namespaced}"')
        svg = re.sub(
            rf"(?<![A-Za-z0-9_-])#{re.escape(original)}(?![A-Za-z0-9_-])",
            f"#{namespaced}",
            svg,
        )
    return svg


def render_diagrams(markdown: str, assets: Path) -> tuple[str, list[dict]]:
    assets.mkdir(parents=True, exist_ok=True)
    command = mermaid_command()
    records: list[dict] = []

    def replace(match: re.Match[str]) -> str:
        index = len(records) + 1
        source = match.group(1).strip() + "\n"
        headings = re.findall(r"^###\s+(.+?)\s*$", markdown[: match.start()], flags=re.MULTILINE)
        diagram_title = headings[-1] if headings else f"Diagrama {index:02d}"
        stem = f"diagrama-{index:02d}"
        input_path = assets / f"{stem}.mmd"
        output_path = assets / f"{stem}.svg"
        input_path.write_text(source, encoding="utf-8")
        process = subprocess.run(
            [command, "-i", str(input_path), "-o", str(output_path), "-b", "transparent"],
            capture_output=True,
            text=True,
            timeout=90,
        )
        if process.returncode != 0 or not output_path.exists():
            raise RuntimeError(f"falha no Mermaid {index}: {process.stderr or process.stdout}")
        svg = output_path.read_text(encoding="utf-8")
        svg = re.sub(r"^<\?xml[^>]*>\s*", "", svg)
        svg = re.sub(r"^<!DOCTYPE[^>]*>\s*", "", svg)
        svg = namespace_svg_ids(svg, index)
        record = {
            "index": index,
            "title": diagram_title,
            "source": source,
            "svg": output_path.name,
            "bytes": output_path.stat().st_size,
        }
        records.append(record)
        return f"""
<div class="diagram-tool" data-diagram="{index}">
  <div class="diagram-toolbar">
    <span class="diagram-title"><small>Diagrama {index:02d}</small><strong>{html.escape(diagram_title)}</strong></span>
    <div class="diagram-actions" aria-label="Controles do diagrama">
      <button type="button" data-zoom="out" title="Reduzir" aria-label="Reduzir diagrama">−</button>
      <button type="button" data-zoom="reset" title="Tamanho original" aria-label="Restaurar tamanho">100%</button>
      <button type="button" data-zoom="in" title="Ampliar" aria-label="Ampliar diagrama">+</button>
      <button type="button" data-expand title="Abrir em tela ampliada" aria-label="Abrir diagrama em tela ampliada">⛶</button>
    </div>
  </div>
  <div class="diagram-viewport">
    <div class="diagram-canvas">{svg}</div>
  </div>
</div>
"""

    rendered = re.sub(r"```mermaid\s*\r?\n(.*?)```", replace, markdown, flags=re.DOTALL)
    return rendered, records


def build_html(source: Path, output: Path) -> dict:
    markdown = source.read_text(encoding="utf-8")
    assets = output.parent / "atlas_forja_assets"
    expanded, records = render_diagrams(markdown, assets)
    parser = MarkdownIt("commonmark", {"html": True}).enable("table")
    body = parser.render(expanded)
    soup = BeautifulSoup(body, "html.parser")
    used: set[str] = set()
    navigation = []
    for heading in soup.find_all(["h2", "h3"]):
        base = slugify(heading.get_text(" ", strip=True))
        slug = base
        suffix = 2
        while slug in used:
            slug = f"{base}-{suffix}"
            suffix += 1
        used.add(slug)
        heading["id"] = slug
        if heading.name == "h2":
            navigation.append((slug, heading.get_text(" ", strip=True)))
    title = "FORJA explicada por dentro"
    source_name = source.name
    document = f"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="icon" href="data:,">
<title>{title}</title>
<style>
:root {{
  --petroleo:#395c60; --petroleo-escuro:#21383b; --petroleo-claro:#e8f1ef;
  --terracota:#9c5b38; --terracota-claro:#fbf2ec; --grafite:#49494d;
  --papel:#f5f7f5; --superficie:#ffffff; --linha:rgba(57,92,96,.22);
  --azul:#315f8c; --verde:#2f6f54; --vermelho:#a33b2b; --amarelo:#9a6b18;
  --texto:#242729; --texto-2:#4d5558; --texto-3:#71797c; --sidebar:272px;
}}
* {{ box-sizing:border-box; }}
html {{ scroll-behavior:smooth; }}
body {{ margin:0; color:var(--texto); background:var(--papel); font-family:"Segoe UI",Aptos,Arial,sans-serif; letter-spacing:0; line-height:1.58; }}
a {{ color:var(--petroleo); text-decoration-thickness:1px; text-underline-offset:3px; }}
.shell {{ min-height:100vh; }}
.sidebar {{ position:fixed; inset:0 auto 0 0; width:var(--sidebar); padding:24px 18px; background:var(--papel); border-right:1px solid var(--linha); overflow:auto; }}
.brand {{ padding:0 8px 18px; border-bottom:1px solid var(--linha); }}
.brand strong {{ display:block; font-family:Georgia,"Times New Roman",serif; font-size:23px; color:var(--petroleo-escuro); }}
.brand span {{ display:block; margin-top:5px; color:var(--texto-3); font-size:12px; }}
.nav-search {{ width:100%; height:36px; margin-top:16px; padding:0 10px; border:1px solid var(--linha); border-radius:4px; background:#fff; color:var(--texto); font:inherit; font-size:13px; }}
.nav-search:focus {{ outline:2px solid rgba(57,92,96,.28); border-color:var(--petroleo); }}
.nav {{ display:grid; gap:3px; margin-top:18px; }}
.nav a {{ display:block; padding:8px 9px; border-left:3px solid transparent; color:var(--texto-2); text-decoration:none; font-size:13px; }}
.nav a:hover,.nav a.active {{ color:var(--petroleo-escuro); background:var(--petroleo-claro); border-left-color:var(--petroleo); }}
.main {{ margin-left:var(--sidebar); }}
.masthead {{ padding:34px 48px 26px; background:var(--superficie); border-bottom:1px solid var(--linha); }}
.eyebrow {{ color:var(--terracota); font-weight:700; font-size:12px; text-transform:uppercase; }}
.masthead h1 {{ margin:8px 0 10px; font-family:Georgia,"Times New Roman",serif; font-size:42px; line-height:1.08; color:var(--petroleo-escuro); }}
.masthead p {{ max-width:820px; margin:0; color:var(--texto-2); }}
.atlas-stats {{ display:grid; grid-template-columns:repeat(4,minmax(120px,1fr)); gap:10px; max-width:900px; margin-top:22px; }}
.atlas-stat {{ min-height:78px; padding:12px 14px; border-top:4px solid var(--petroleo); background:var(--papel); }}
.atlas-stat:nth-child(2) {{ border-top-color:var(--terracota); }} .atlas-stat:nth-child(3) {{ border-top-color:var(--azul); }} .atlas-stat:nth-child(4) {{ border-top-color:var(--verde); }}
.atlas-stat strong {{ display:block; font-family:Georgia,"Times New Roman",serif; font-size:25px; line-height:1.05; color:var(--petroleo-escuro); }}
.atlas-stat span {{ display:block; margin-top:5px; color:var(--texto-2); font-size:12px; }}
.status-strip {{ display:flex; flex-wrap:wrap; gap:8px; margin-top:20px; }}
.status {{ display:inline-flex; align-items:center; gap:7px; padding:6px 9px; border:1px solid var(--linha); border-radius:4px; font-size:12px; font-weight:650; background:#fff; }}
.status::before {{ content:""; width:9px; height:9px; border-radius:50%; background:var(--grafite); }}
.status.active::before {{ background:var(--petroleo); }} .status.shadow::before {{ background:var(--terracota); }} .status.planned::before {{ background:#707078; }} .status.blocker::before {{ background:var(--vermelho); }}
.mast-actions {{ margin-top:18px; display:flex; gap:10px; flex-wrap:wrap; }}
.mast-actions a {{ padding:7px 10px; border:1px solid var(--linha); border-radius:4px; background:var(--superficie); font-size:13px; text-decoration:none; }}
article {{ max-width:1320px; margin:0 auto; padding:30px 48px 80px; }}
article > h1 {{ display:none; }}
h2 {{ margin:54px 0 12px; padding-top:12px; font-family:Georgia,"Times New Roman",serif; font-size:29px; color:var(--petroleo-escuro); border-top:1px solid var(--linha); }}
h2:first-of-type {{ margin-top:12px; border-top:0; }}
h3 {{ margin:30px 0 10px; font-size:19px; color:var(--grafite); }}
p,li {{ max-width:970px; }}
blockquote {{ margin:18px 0; padding:14px 18px; border-left:4px solid var(--terracota); background:var(--terracota-claro); color:#543827; }}
.executive-cards {{ display:grid; grid-template-columns:repeat(4,minmax(0,1fr)); gap:14px; margin:18px 0 34px; }}
.executive-card {{ min-height:116px; padding:18px; border-top:5px solid var(--petroleo); background:var(--superficie); box-shadow:0 1px 0 rgba(57,92,96,.08); }}
.executive-card strong {{ display:block; font-family:Georgia,"Times New Roman",serif; font-size:22px; color:var(--petroleo-escuro); }}
.executive-card span {{ display:block; margin-top:9px; color:var(--texto-2); font-size:14px; line-height:1.4; }}
.executive-card.evidence {{ border-top-color:var(--verde); }} .executive-card.human {{ border-top-color:var(--amarelo); }} .executive-card.shadow {{ border-top-color:var(--terracota); }}
table {{ width:100%; border-collapse:collapse; margin:18px 0 28px; background:var(--superficie); font-size:14px; }}
th,td {{ padding:10px 12px; border-bottom:1px solid var(--linha); text-align:left; vertical-align:top; }}
th {{ background:var(--petroleo-claro); color:var(--petroleo-escuro); }}
code {{ font-family:Consolas,"Cascadia Mono",monospace; }}
.diagram-tool {{ margin:14px 0 34px; border:1px solid var(--linha); border-radius:6px; background:var(--superficie); overflow:hidden; }}
.diagram-toolbar {{ display:flex; justify-content:space-between; align-items:center; gap:14px; min-height:54px; padding:8px 10px 8px 14px; border-bottom:1px solid var(--linha); background:#fafbfa; color:var(--texto-3); font-size:12px; font-weight:700; }}
.diagram-title {{ min-width:0; }} .diagram-title small {{ display:block; color:var(--terracota); font-size:10px; text-transform:uppercase; }} .diagram-title strong {{ display:block; overflow:hidden; color:var(--petroleo-escuro); font-size:13px; text-overflow:ellipsis; white-space:nowrap; }}
.diagram-actions {{ display:flex; gap:4px; }}
.diagram-actions button {{ min-width:34px; height:28px; padding:0 8px; border:1px solid var(--linha); border-radius:4px; background:var(--superficie); color:var(--petroleo-escuro); font-weight:700; cursor:pointer; }}
.diagram-actions button:hover {{ background:var(--petroleo-claro); }}
.diagram-viewport {{ overflow:auto; padding:18px; background:#fff; }}
.diagram-canvas {{ width:100%; min-width:760px; transform-origin:top left; transition:width .12s ease; }}
.diagram-canvas svg {{ display:block; width:100% !important; height:auto !important; max-width:none !important; margin:0 auto; }}
.diagram-tool.is-expanded {{ position:fixed; inset:14px; z-index:1000; margin:0; border-color:var(--petroleo); box-shadow:0 24px 70px rgba(17,28,29,.28); overflow:auto; }}
.diagram-tool.is-expanded .diagram-toolbar {{ position:sticky; top:0; z-index:3; background:#fff; }}
.diagram-tool.is-expanded .diagram-viewport {{ min-height:calc(100vh - 130px); }}
.diagram-tool.is-expanded .diagram-canvas {{ min-width:1180px; }}
body.diagram-open {{ overflow:hidden; }}
.mermaid-source {{ border-top:1px solid var(--linha); background:#fafbfa; }}
.mermaid-source summary {{ padding:10px 14px; cursor:pointer; color:var(--petroleo); font-size:13px; font-weight:650; }}
.mermaid-source pre {{ margin:0; padding:14px; overflow:auto; border-top:1px solid var(--linha); background:#202425; color:#eef2f0; font-size:12px; line-height:1.45; }}
.footer {{ padding:22px 48px; border-top:1px solid var(--linha); color:var(--texto-3); font-size:12px; background:var(--superficie); }}
@media (max-width:900px) {{
  .sidebar {{ position:relative; width:auto; max-height:none; border-right:0; border-bottom:1px solid var(--linha); }}
  .nav {{ display:flex; overflow:auto; }} .nav a {{ white-space:nowrap; border-left:0; border-bottom:3px solid transparent; }}
  .nav a:hover,.nav a.active {{ border-bottom-color:var(--petroleo); }}
  .main {{ margin-left:0; }} .masthead,article,.footer {{ padding-left:20px; padding-right:20px; }}
  .masthead h1 {{ font-size:34px; }} .diagram-viewport {{ padding:10px; }}
  .atlas-stats,.executive-cards {{ grid-template-columns:repeat(2,minmax(0,1fr)); }}
  .diagram-title strong {{ max-width:180px; }}
}}
@media (max-width:520px) {{ .atlas-stats,.executive-cards {{ grid-template-columns:1fr; }} .diagram-actions button {{ min-width:32px; padding:0 6px; }} .diagram-title strong {{ max-width:125px; }} }}
@media print {{ .sidebar,.diagram-actions,.mermaid-source,.mast-actions {{ display:none !important; }} .main {{ margin:0; }} .diagram-viewport {{ overflow:visible; }} .diagram-canvas {{ min-width:0; }} article {{ max-width:none; }} }}
</style>
</head>
<body>
<div class="shell">
  <aside class="sidebar">
    <div class="brand"><strong>FORJA</strong><span>Guia visual para advogados · atualizado em 12/07/2026</span></div>
    <input class="nav-search" type="search" placeholder="Buscar seção" aria-label="Buscar seção do atlas">
    <nav class="nav">{''.join(f'<a href="#{slug}">{html.escape(label)}</a>' for slug,label in navigation)}</nav>
  </aside>
  <main class="main">
    <header class="masthead">
      <div class="eyebrow">Do recebimento à revisão humana</div>
      <h1>FORJA por dentro</h1>
      <p>Uma explicação visual de como a FORJA recebe a demanda, organiza os documentos, constrói a estratégia, redige, revisa e prepara a petição para a decisão humana.</p>
      <div class="atlas-stats">
        <div class="atlas-stat"><strong>{len(records)}</strong><span>diagramas navegáveis</span></div>
        <div class="atlas-stat"><strong>11 etapas</strong><span>da demanda à entrega comprovada</span></div>
        <div class="atlas-stat"><strong>{len(navigation)}</strong><span>capítulos de leitura</span></div>
        <div class="atlas-stat"><strong>12/07</strong><span>última consolidação</span></div>
      </div>
      <div class="status-strip">
        <span class="status active">Funcionamento atual</span><span class="status shadow">Melhoria em teste</span><span class="status planned">Próximo passo</span><span class="status blocker">Impedimento</span>
      </div>
      <div class="mast-actions"><a href="RELATORIO_PSO_PET_SOLUCAO_PROBLEMAS_E_METRICAS_2026-07-11.md" target="_blank" rel="noopener">Estudo do método de diagnóstico</a><a href="../FLUXO_BIZAGI_FORJA_PETICAO.md" target="_blank" rel="noopener">Fluxo completo de elaboração</a></div>
    </header>
    <article>{str(soup)}</article>
    <footer class="footer">Guia atualizado em 12/07/2026 · {len(records)} diagramas vetoriais conferidos.</footer>
  </main>
</div>
<script>
document.querySelectorAll('[data-diagram]').forEach(tool => {{
  const canvas = tool.querySelector('.diagram-canvas'); let zoom = 1;
  tool.querySelectorAll('[data-zoom]').forEach(button => button.addEventListener('click', () => {{
    const action = button.dataset.zoom;
    zoom = action === 'in' ? Math.min(2.2, zoom + .2) : action === 'out' ? Math.max(.6, zoom - .2) : 1;
    canvas.style.width = `${{Math.round(zoom * 100)}}%`;
    tool.querySelector('[data-zoom="reset"]').textContent = `${{Math.round(zoom * 100)}}%`;
  }}));
  const expand = tool.querySelector('[data-expand]');
  expand.addEventListener('click', () => {{
    const opening = !tool.classList.contains('is-expanded');
    document.querySelectorAll('.diagram-tool.is-expanded').forEach(item => item.classList.remove('is-expanded'));
    tool.classList.toggle('is-expanded', opening);
    document.body.classList.toggle('diagram-open', opening);
    expand.textContent = opening ? '×' : '⛶';
    expand.title = opening ? 'Fechar tela ampliada' : 'Abrir em tela ampliada';
  }});
}});
document.addEventListener('keydown', event => {{
  if (event.key === 'Escape') {{
    document.querySelectorAll('.diagram-tool.is-expanded').forEach(tool => {{ tool.classList.remove('is-expanded'); const button = tool.querySelector('[data-expand]'); button.textContent = '⛶'; button.title = 'Abrir em tela ampliada'; }});
    document.body.classList.remove('diagram-open');
  }}
}});
const links = [...document.querySelectorAll('.nav a')];
const search = document.querySelector('.nav-search');
search.addEventListener('input', () => {{ const query = search.value.trim().toLocaleLowerCase('pt-BR'); links.forEach(link => link.hidden = query && !link.textContent.toLocaleLowerCase('pt-BR').includes(query)); }});
const map = new Map(links.map(a => [a.getAttribute('href').slice(1), a]));
const observer = new IntersectionObserver(entries => entries.forEach(entry => {{
  if (entry.isIntersecting && map.has(entry.target.id)) {{ links.forEach(a => a.classList.remove('active')); map.get(entry.target.id).classList.add('active'); }}
}}), {{rootMargin:'-10% 0px -75% 0px'}});
document.querySelectorAll('h2[id]').forEach(h => observer.observe(h));
</script>
</body></html>"""
    output.write_text(document, encoding="utf-8")
    return {"source": str(source), "output": str(output), "diagrams": len(records), "assets": str(assets), "bytes": output.stat().st_size}


def main() -> None:
    parser = argparse.ArgumentParser(description="Renderiza o atlas visual da FORJA")
    parser.add_argument("--source", default=str(DEFAULT_SOURCE))
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    args = parser.parse_args()
    output = Path(args.output)
    result = build_html(Path(args.source), output)
    if output.resolve() == DEFAULT_OUTPUT.resolve():
        shutil.copyfile(output, FRIENDLY_OUTPUT)
        result["friendly_output"] = str(FRIENDLY_OUTPUT)
    print(result)


if __name__ == "__main__":
    main()
