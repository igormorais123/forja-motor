from __future__ import annotations

import argparse
import hashlib
import json
import statistics
import sys
import time
from pathlib import Path

import easyocr
import fitz
import numpy as np
from PIL import Image, ImageDraw


def page_key(pdf: Path, page_number: int) -> str:
    return f"{pdf.name}::p{page_number:04d}"


def load_completed(path: Path) -> set[str]:
    if not path.exists():
        return set()
    completed: set[str] = set()
    for line in path.read_text(encoding="utf-8").splitlines():
        try:
            item = json.loads(line)
        except json.JSONDecodeError:
            continue
        completed.add(item["key"])
    return completed


def append_jsonl(path: Path, item: dict) -> None:
    with path.open("a", encoding="utf-8", newline="\n") as handle:
        handle.write(json.dumps(item, ensure_ascii=False) + "\n")
        handle.flush()


def render_array(page: fitz.Page, zoom: float) -> np.ndarray:
    pix = page.get_pixmap(matrix=fitz.Matrix(zoom, zoom), alpha=False)
    return np.frombuffer(pix.samples, dtype=np.uint8).reshape(
        pix.height, pix.width, pix.n
    )


def save_page_image(array: np.ndarray, output: Path) -> None:
    Image.fromarray(array).save(output, "JPEG", quality=88, optimize=True)


def make_contact_sheets(images: list[Path], output_dir: Path) -> None:
    sheets_dir = output_dir / "contatos"
    sheets_dir.mkdir(exist_ok=True)
    for old in sheets_dir.glob("contato_*.jpg"):
        old.unlink()
    batch_size = 9
    tile_width = 600
    margin = 18
    label_height = 34
    for batch_index in range(0, len(images), batch_size):
        selected = images[batch_index : batch_index + batch_size]
        prepared: list[tuple[Path, Image.Image]] = []
        max_tile_height = 0
        for path in selected:
            with Image.open(path) as image:
                rgb = image.convert("RGB")
                height = round(rgb.height * tile_width / rgb.width)
                thumb = rgb.resize((tile_width, height), Image.Resampling.LANCZOS)
            max_tile_height = max(max_tile_height, thumb.height)
            prepared.append((path, thumb))
        sheet = Image.new(
            "RGB",
            (
                3 * tile_width + 4 * margin,
                3 * (max_tile_height + label_height) + 4 * margin,
            ),
            "white",
        )
        draw = ImageDraw.Draw(sheet)
        for index, (path, thumb) in enumerate(prepared):
            row, col = divmod(index, 3)
            x = margin + col * (tile_width + margin)
            y = margin + row * (max_tile_height + label_height + margin)
            draw.text((x, y), path.stem, fill="black")
            sheet.paste(thumb, (x, y + label_height))
        number = batch_index // batch_size + 1
        sheet.save(
            sheets_dir / f"contato_{number:03d}.jpg",
            "JPEG",
            quality=88,
            optimize=True,
        )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--pdf", action="append", required=True, type=Path)
    parser.add_argument("--zoom", type=float, default=1.7)
    parser.add_argument("--contact-sheets", action="store_true")
    args = parser.parse_args()

    output_dir = Path(str(args.output).strip().strip('"')).resolve()
    pages_dir = output_dir / "paginas"
    pages_dir.mkdir(parents=True, exist_ok=True)
    ledger = output_dir / "OCR_LEDGER.jsonl"
    completed = load_completed(ledger)
    reader = easyocr.Reader(["pt", "en"], gpu=False, verbose=False)
    pdf_paths = [Path(str(pdf).strip().strip('"')).resolve() for pdf in args.pdf]
    total = sum(len(fitz.open(pdf)) for pdf in pdf_paths)
    done = len(completed)
    started = time.time()

    print(
        json.dumps(
            {"event": "start", "total_pages": total, "already_done": done},
            ensure_ascii=False,
        ),
        flush=True,
    )
    for pdf in pdf_paths:
        document = fitz.open(pdf)
        source_sha256 = hashlib.sha256(pdf.read_bytes()).hexdigest()
        for page_index, page in enumerate(document):
            page_number = page_index + 1
            key = page_key(pdf, page_number)
            if key in completed:
                continue
            page_started = time.time()
            array = render_array(page, args.zoom)
            image_name = f"{pdf.stem}_p{page_number:04d}.jpg"
            image_path = pages_dir / image_name
            save_page_image(array, image_path)
            results = reader.readtext(
                array,
                detail=1,
                paragraph=False,
                batch_size=1,
            )
            blocks = [
                {
                    "text": result[1].strip(),
                    "confidence": round(float(result[2]), 6),
                    "bbox": [[round(float(x), 2), round(float(y), 2)] for x, y in result[0]],
                }
                for result in results
                if result[1].strip()
            ]
            text = "\n".join(block["text"] for block in blocks)
            confidences = [block["confidence"] for block in blocks]
            item = {
                "key": key,
                "source_pdf": str(pdf),
                "source_sha256": source_sha256,
                "page": page_number,
                "page_count": len(document),
                "image": str(image_path),
                "image_sha256": hashlib.sha256(image_path.read_bytes()).hexdigest(),
                "text": text,
                "text_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
                "characters": len(text),
                "blocks": blocks,
                "mean_confidence": round(statistics.mean(confidences), 6)
                if confidences
                else 0.0,
                "minimum_confidence": round(min(confidences), 6)
                if confidences
                else 0.0,
                "elapsed_seconds": round(time.time() - page_started, 3),
                "ocr_engine": "easyocr-1.7.2-latin_g2",
                "review_status": "ocr_only_not_human_linear_reading",
            }
            append_jsonl(ledger, item)
            completed.add(key)
            done += 1
            print(
                json.dumps(
                    {
                        "event": "page",
                        "done": done,
                        "total": total,
                        "key": key,
                        "characters": len(text),
                        "mean_confidence": item["mean_confidence"],
                        "seconds": item["elapsed_seconds"],
                    },
                    ensure_ascii=False,
                ),
                flush=True,
            )
    images = sorted(pages_dir.glob("*.jpg"))
    if args.contact_sheets:
        make_contact_sheets(images, output_dir)
    print(
        json.dumps(
            {
                "event": "complete",
                "total": total,
                "done": len(completed),
                "elapsed_seconds": round(time.time() - started, 3),
                "ledger": str(ledger),
            },
            ensure_ascii=False,
        ),
        flush=True,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
