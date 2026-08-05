"""Deterministic SVG layout lint for Medina Osório visual-law diagrams."""

from __future__ import annotations

import argparse
import json
import math
import re
import xml.etree.ElementTree as ET
from pathlib import Path


WEIGHTS = {"normal", "bold", "bolder", "lighter", *{str(value) for value in range(100, 1000, 100)}}
STYLES = {"normal", "italic", "oblique"}
ANCHORS = {"start", "middle", "end"}


def _tag(element: ET.Element) -> str:
    return element.tag.rsplit("}", 1)[-1]


def _number(value: object, default: float = 0.0) -> float:
    match = re.search(r"-?\d+(?:\.\d+)?", str(value or ""))
    return float(match.group()) if match else default


def _intersection(a: tuple[float, float, float, float], b: tuple[float, float, float, float]) -> float:
    width = max(0.0, min(a[2], b[2]) - max(a[0], b[0]))
    height = max(0.0, min(a[3], b[3]) - max(a[1], b[1]))
    return width * height


def _area(box: tuple[float, float, float, float]) -> float:
    return max(0.0, box[2] - box[0]) * max(0.0, box[3] - box[1])


def _text_box(element: ET.Element) -> tuple[float, float, float, float]:
    text = " ".join("".join(element.itertext()).split())
    size = _number(element.get("font-size"), 12)
    weight = element.get("font-weight", "normal")
    factor = 0.58 if weight in {"bold", "600", "700", "800", "900"} else 0.52
    width = max(size * 0.35, len(text) * size * factor)
    x, y = _number(element.get("x")), _number(element.get("y"))
    anchor = element.get("text-anchor", "start")
    if anchor == "middle":
        x0, x1 = x - width / 2, x + width / 2
    elif anchor == "end":
        x0, x1 = x - width, x
    else:
        x0, x1 = x, x + width
    return x0, y - size, x1, y + size * 0.22


def _rect_box(element: ET.Element) -> tuple[float, float, float, float]:
    x, y = _number(element.get("x")), _number(element.get("y"))
    return x, y, x + _number(element.get("width")), y + _number(element.get("height"))


def _line_hits_box(element: ET.Element, box: tuple[float, float, float, float]) -> bool:
    x1, y1 = _number(element.get("x1")), _number(element.get("y1"))
    x2, y2 = _number(element.get("x2")), _number(element.get("y2"))
    if abs(y2 - y1) < 0.5:
        return box[1] <= y1 <= box[3] and max(min(x1, x2), box[0]) < min(max(x1, x2), box[2])
    if abs(x2 - x1) < 0.5:
        return box[0] <= x1 <= box[2] and max(min(y1, y2), box[1]) < min(max(y1, y2), box[3])
    # Sample diagonal connectors; sufficient for warning-level detection.
    for step in range(21):
        ratio = step / 20
        x, y = x1 + (x2 - x1) * ratio, y1 + (y2 - y1) * ratio
        if box[0] <= x <= box[2] and box[1] <= y <= box[3]:
            return True
    return False


def lint_svg(path: str | Path) -> dict:
    path = Path(path)
    findings: list[dict] = []
    try:
        root = ET.parse(path).getroot()
    except ET.ParseError as exc:
        return {"approved": False, "p0": 1, "p1": 0, "findings": [{"severity": "P0", "code": "invalid_xml", "detail": str(exc)}]}
    view_box = [_number(value) for value in str(root.get("viewBox") or "").split()]
    if len(view_box) != 4 or view_box[2] <= 0 or view_box[3] <= 0:
        findings.append({"severity": "P0", "code": "invalid_viewbox"})
        width, height = math.inf, math.inf
    else:
        width, height = view_box[2], view_box[3]

    ordered = list(root.iter())
    text_items = []
    rect_items = []
    line_items = []
    rect_by_id = {}
    for order, element in enumerate(ordered):
        tag = _tag(element)
        if tag == "text":
            text = " ".join("".join(element.itertext()).split())
            weight, style, anchor = element.get("font-weight", "normal"), element.get("font-style", "normal"), element.get("text-anchor", "start")
            for attr, value, allowed in (("font-weight", weight, WEIGHTS), ("font-style", style, STYLES), ("text-anchor", anchor, ANCHORS)):
                if value not in allowed:
                    findings.append({"severity": "P0", "code": "invalid_svg_enum", "attribute": attr, "value": value, "text": text[:80]})
            size = _number(element.get("font-size"), 0)
            if size < 8:
                findings.append({"severity": "P0", "code": "font_too_small", "size": size, "text": text[:80]})
            box = _text_box(element)
            if box[0] < -1 or box[1] < -1 or box[2] > width + 1 or box[3] > height + 1:
                findings.append({"severity": "P0", "code": "text_outside_viewbox", "box": [round(value, 1) for value in box], "text": text[:80]})
            text_items.append({"order": order, "element": element, "text": text, "box": box})
        elif tag == "rect":
            item = {"order": order, "element": element, "box": _rect_box(element)}
            rect_items.append(item)
            if element.get("id"):
                rect_by_id[element.get("id")] = item
        elif tag == "line":
            line_items.append({"order": order, "element": element})

    for item in text_items:
        container_id = item["element"].get("data-container-id")
        if container_id and container_id in rect_by_id:
            container = rect_by_id[container_id]["box"]
            box = item["box"]
            if box[0] < container[0] + 2 or box[1] < container[1] + 1 or box[2] > container[2] - 2 or box[3] > container[3] - 1:
                findings.append({"severity": "P0", "code": "text_outside_container", "containerId": container_id, "text": item["text"][:80]})

    for index, left in enumerate(text_items):
        for right in text_items[index + 1:]:
            overlap = _intersection(left["box"], right["box"])
            minimum = min(_area(left["box"]), _area(right["box"]))
            if minimum and overlap / minimum > 0.18:
                findings.append({"severity": "P0", "code": "text_overlap", "textA": left["text"][:60], "textB": right["text"][:60]})

    for text_item in text_items:
        for rect_item in rect_items:
            rect = rect_item["element"]
            if rect_item["order"] <= text_item["order"] or rect.get("fill", "none") in {"none", "transparent"}:
                continue
            if _number(rect.get("opacity"), 1) <= 0.05 or _number(rect.get("fill-opacity"), 1) <= 0.05:
                continue
            overlap = _intersection(text_item["box"], rect_item["box"])
            if _area(text_item["box"]) and overlap / _area(text_item["box"]) > 0.2:
                findings.append({"severity": "P0", "code": "later_shape_covers_text", "text": text_item["text"][:80]})

    for text_item in text_items:
        for line_item in line_items:
            if _line_hits_box(line_item["element"], text_item["box"]):
                findings.append({"severity": "P1", "code": "connector_crosses_text", "text": text_item["text"][:80]})

    # De-duplicate identical geometry findings to keep reports actionable.
    unique = []
    seen = set()
    for finding in findings:
        key = json.dumps(finding, ensure_ascii=False, sort_keys=True)
        if key not in seen:
            unique.append(finding)
            seen.add(key)
    return {
        "schemaVersion": 1,
        "file": str(path),
        "approved": not unique,
        "p0": sum(item["severity"] == "P0" for item in unique),
        "p1": sum(item["severity"] == "P1" for item in unique),
        "counts": {"texts": len(text_items), "rects": len(rect_items), "lines": len(line_items)},
        "findings": unique,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Lint geométrico SVG Medina Osório")
    parser.add_argument("svg", nargs="+", type=Path)
    args = parser.parse_args()
    results = [lint_svg(path) for path in args.svg]
    print(json.dumps(results, ensure_ascii=False, indent=2))
    raise SystemExit(0 if all(item["approved"] for item in results) else 1)


if __name__ == "__main__":
    main()
