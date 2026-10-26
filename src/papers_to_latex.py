#!/usr/bin/env python3
"""Convert one paper per folder in a papers directory to XeLaTeX.

DOCX is read with python-docx. PDFs use pypdf. Legacy DOC text is recovered
from the WordDocument stream with 7-Zip when Office automation is unavailable.
For proceedings/books, --paper-title selects the intended paper; otherwise the
folder name is used as a title hint and the best matching source is chosen.
"""

from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import sys
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

try:
    from docx import Document
except ImportError:
    Document = None
try:
    from pypdf import PdfReader
except ImportError:
    PdfReader = None


SUPPORTED = {".docx", ".doc", ".pdf"}
SKIP_WORDS = {"paper", "article", "ст", "вак", "тз", "wos", "електронне", "моделювання"}


def normalize_folders(root: Path) -> None:
    for folder in root.iterdir():
        if folder.is_dir() and " " in folder.name:
            folder.rename(folder.with_name(folder.name.replace(" ", "_")))


def words(value: str) -> set[str]:
    return {
        re.sub(r"[^\w-]", "", item.casefold())
        for item in value.replace("_", " ").split()
        if len(item) > 2 and item.casefold() not in SKIP_WORDS
    }


def read_legacy_doc(source: Path) -> list[tuple[str, str]]:
    """Recover text from the WordDocument stream when Office automation is unavailable."""
    seven_zip = shutil.which("7z") or shutil.which("7za")
    if not seven_zip and sys.platform == "win32":
        candidate = Path(os.environ.get("ProgramFiles", r"C:\Program Files")) / "7-Zip" / "7z.exe"
        if candidate.is_file():
            seven_zip = str(candidate)
    if not seven_zip:
        raise RuntimeError("Legacy .doc input needs 7-Zip on PATH (or convert it to DOCX first)")
    run = subprocess.run(
        [seven_zip, "x", "-so", str(source.resolve()), "WordDocument"],
        capture_output=True,
        timeout=120,
    )
    if run.returncode or not run.stdout:
        raise RuntimeError(f"Could not unpack the legacy Word document: {run.stderr[-1000:].decode(errors='replace')}")
    raw = run.stdout
    pattern = re.compile(r"[A-Za-zА-Яа-яІіЇїЄєҐґ0-9][A-Za-zА-Яа-яІіЇїЄєҐґ0-9 ,.;:!?()\[\]/'’&%+–—-]{14,}")
    candidates = []
    for encoding in ("cp1251", "latin1", "utf-16le"):
        decoded = raw.decode(encoding, errors="ignore")
        runs = [" ".join(x.split()) for x in pattern.findall(decoded)]
        runs = [x for x in runs if len(words(x)) >= 3]
        candidates.append(runs)
    runs = max(candidates, key=lambda values: sum(map(len, values)))
    if not runs:
        raise RuntimeError("No readable text was found in this legacy Word document")
    return [("paragraph", text) for text in runs]


def read_docx(source: Path) -> list[tuple[str, str]]:
    if Document is None:
        raise RuntimeError("python-docx is required; install it in .venv")
    try:
        doc = Document(str(source))
    except Exception:
        # Recover paragraphs from packages with broken relationship metadata.
        with zipfile.ZipFile(source) as archive:
            xml = ET.fromstring(archive.read("word/document.xml"))
        ns = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main", "m": "http://schemas.openxmlformats.org/officeDocument/2006/math"}
        recovered = []
        if "wordprocessingml" in xml.tag:
            ns["w"] = xml.tag[1:].split("}")[0]
        paragraph_tag = f"{{{ns['w']}}}p"
        text_tag = f"{{{ns['w']}}}t"
        math_tag = f"{{{ns['m']}}}t"
        for paragraph in (node for node in xml.iter() if node.tag == paragraph_tag):
            nodes = [node for node in paragraph.iter() if node.tag in {text_tag, math_tag}]
            text = "".join(node.text or "" for node in nodes).strip()
            if text:
                recovered.append(("paragraph", text))
        if recovered:
            return recovered
        raise
    blocks: list[tuple[str, str]] = []
    for paragraph in doc.paragraphs:
        text = "".join(paragraph._p.itertext()).strip()
        if not text:
            continue
        style = paragraph.style.name.casefold() if paragraph.style else ""
        kind = "heading" if "heading" in style or "title" in style else "paragraph"
        blocks.append((kind, text))
    for table in doc.tables:
        for row in table.rows:
            cells = [" ".join(cell.text.split()) for cell in row.cells]
            blocks.append(("paragraph", " | ".join(cells)))
    return blocks


def read_pdf(source: Path, title_hint: str) -> list[tuple[str, str]]:
    if PdfReader is None:
        raise RuntimeError("pypdf is required for PDF input; install it with: python -m pip install pypdf")
    reader = PdfReader(str(source))
    pages = [(page.extract_text() or "").strip() for page in reader.pages]
    # Article PDFs are kept whole. For books/proceedings, locate the page that
    # best matches the folder/citation title and include subsequent continuation
    # pages until a new all-caps article heading begins (up to five pages).
    if len(pages) <= 20:
        return [block for text in pages for block in pdf_page_blocks(text)]
    hint = words(title_hint)
    scores = [len(hint & words(text)) for text in pages]
    if not max(scores, default=0):
        raise RuntimeError(f"Could not locate the requested article title in {source.name}; pass --paper-title FOLDER=TITLE")
    start = max(range(len(scores)), key=scores.__getitem__)
    selected = [trim_to_title(pages[start], hint)]
    for index in range(start + 1, min(len(pages), start + 5)):
        text = pages[index]
        if not text:
            break
        lines = [line.strip() for line in text.splitlines() if len(line.strip()) > 12]
        has_new_title = any(
            line.isupper() and len(words(line)) >= 4 and len(words(line) & hint) < 2
            for line in lines[:15]
        )
        if has_new_title:
            break
        selected.append(text)
    return [block for text in selected for block in pdf_page_blocks(text)]


def trim_to_title(text: str, hint: set[str]) -> str:
    tokens = list(re.finditer(r"[^\W_]+", text, flags=re.UNICODE))
    normalized = [re.sub(r"[^\w-]", "", item.group().casefold()) for item in tokens]
    width = min(16, len(tokens))
    best_start, best_score = 0, 0
    for start in range(max(1, len(tokens) - width + 1)):
        hits = {token for token in normalized[start:start + width] if token in hint}
        if len(hits) > best_score:
            best_start, best_score = start, len(hits)
    if best_score >= 3:
        first_hit = next((i for i in range(best_start, min(best_start + width, len(tokens))) if normalized[i] in hint), best_start)
        return text[tokens[first_hit].start():]
    return text


def pdf_page_blocks(text: str) -> list[tuple[str, str]]:
    blocks: list[tuple[str, str]] = []
    paragraph: list[str] = []
    def flush() -> None:
        if paragraph:
            blocks.append(("paragraph", " ".join(paragraph)))
            paragraph.clear()
    for line in text.splitlines():
        line = " ".join(line.split())
        if not line:
            flush()
        elif is_formula(line):
            flush()
            blocks.append(("paragraph", line))
        else:
            paragraph.append(line)
    flush()
    return blocks


def select_source(folder: Path, title_hint: str) -> Path | None:
    generated_stem = re.sub(r"[^\w.-]+", "_", folder.name, flags=re.UNICODE).strip("_.")
    sources = [
        p for p in folder.rglob("*")
        if p.is_file()
        and p.suffix.casefold() in SUPPORTED
        # A previous run may have left the output PDF beside its TeX source.
        # Do not accidentally feed that generated PDF back into the converter.
        and not (p.suffix.casefold() == ".pdf" and p.stem == generated_stem)
    ]
    if not sources:
        return None
    hint = words(title_hint)
    def rank(path: Path) -> tuple[int, int, int]:
        name_words = words(path.stem)
        overlap = len(hint & name_words)
        # DOCX generally gives more faithful structure than PDF; non-book filenames win.
        return (overlap, int(path.suffix.casefold() == ".docx"), -len(path.parts))
    selected = max(sources, key=rank)
    if len(sources) > 1:
        # If a folder contains related DOCs, compare their actual titles/body
        # with the citation hint so a template/example cannot win by filename.
        def content_rank(path: Path) -> tuple[int, tuple[int, int, int]]:
            if path.suffix.casefold() == ".doc":
                body = " ".join(text for _, text in read_legacy_doc(path)[:30])
            elif path.suffix.casefold() == ".docx":
                body = " ".join(text for _, text in read_docx(path)[:30])
            else:
                body = ""
            return (len(words(title_hint) & words(body)), rank(path))
        selected = max(sources, key=content_rank)
    return selected


def escape_tex(text: str) -> str:
    replacements = {
        "\\": r"\textbackslash{}", "&": r"\&", "%": r"\%", "$": r"\$",
        "#": r"\#", "_": r"\_", "{": r"\{", "}": r"\}",
        "~": r"\textasciitilde{}", "^": r"\textasciicircum{}",
    }
    return "".join(replacements.get(ch, ch) for ch in text)


def math_tex(text: str) -> str:
    symbols = {
        "−": "-", "×": r"\times", "÷": r"\div", "·": r"\cdot", "⋅": r"\cdot",
        "≤": r"\leq", "≥": r"\geq", "≠": r"\neq", "≈": r"\approx", "∼": r"\sim",
        "∑": r"\sum", "Σ": r"\sum", "∫": r"\int", "∂": r"\partial", "∞": r"\infty",
        "√": r"\sqrt{}", "α": r"\alpha", "β": r"\beta", "γ": r"\gamma", "δ": r"\delta",
        "θ": r"\theta", "λ": r"\lambda", "μ": r"\mu", "π": r"\pi", "σ": r"\sigma",
        "φ": r"\phi", "ω": r"\omega", "∈": r"\in", "∉": r"\notin", "∩": r"\cap",
        "∪": r"\cup", "→": r"\to", "↔": r"\leftrightarrow", "°": r"^{\circ}",
    }
    result = []
    subscripts = str.maketrans("₀₁₂₃₄₅₆₇₈₉", "0123456789")
    superscripts = str.maketrans("⁰¹²³⁴⁵⁶⁷⁸⁹", "0123456789")
    for char in text:
        if char in symbols:
            result.append(symbols[char])
        elif char in "₀₁₂₃₄₅₆₇₈₉":
            result.append("_{" + char.translate(subscripts) + "}")
        elif char in "⁰¹²³⁴⁵⁶⁷⁸⁹":
            result.append("^{" + char.translate(superscripts) + "}")
        elif "\u0400" <= char <= "\u052f":
            result.append(r"\text{" + char + "}")
        else:
            result.append({"\\": r"\backslash", "%": r"\%", "&": r"\&", "#": r"\#", "$": r"\$"}.get(char, char))
    return "".join(result)


def is_formula(text: str) -> bool:
    operators = "=±×÷√∑Σ∫∂∞≤≥≠≈∈∉∩∪"
    if len(text) > 240 or not any(char in text for char in operators):
        return False
    letters = sum(char.isalpha() for char in text)
    return letters < max(35, len(text) * 0.55)


def tex_document(folder: Path, source: Path | None, title: str, blocks: list[tuple[str, str]]) -> str:
    output = [
        r"\documentclass[12pt,a4paper]{article}",
        r"\usepackage{fontspec}",
        r"\usepackage{polyglossia}",
        r"\setmainfont{TeX Gyre Termes}",
        r"\newfontfamily\cyrillicfont{TeX Gyre Termes}",
        r"\setdefaultlanguage{ukrainian}",
        r"\setotherlanguage{english}",
        r"\usepackage{amsmath,amssymb,geometry,graphicx}",
        r"\geometry{margin=25mm}",
        r"\setlength{\parindent}{1.25cm}",
        r"\setlength{\parskip}{0.25em}",
        r"\begin{document}",
        f"\\title{{{escape_tex(title)}}}",
        r"\maketitle",
    ]
    if source is None:
        output.extend([r"\section*{Source not found}", "This folder had no DOCX, DOC, or PDF source file."])
    else:
        for kind, text in blocks:
            if kind == "heading":
                output.append(f"\\section*{{{escape_tex(text)}}}")
            elif is_formula(text):
                output.append(r"\[" + math_tex(text) + r"\]")
            else:
                output.append(escape_tex(text))
                output.append(r"\par")
    output.append(r"\end{document}")
    return "\n".join(output) + "\n"


def process_folder(folder: Path, title_override: str | None) -> Path:
    title = title_override or folder.name.replace("_", " ")
    citation_files = list(folder.glob("цитата.txt"))
    citation_hint = citation_files[0].read_text(encoding="utf-8", errors="replace") if citation_files else ""
    # Citation metadata helps distinguish a paper from supplementary or related DOC files.
    source = select_source(folder, f"{title} {citation_hint}")
    blocks: list[tuple[str, str]] = []
    if source:
        if source.suffix.casefold() == ".pdf":
            blocks = read_pdf(source, f"{title} {citation_hint}")
        elif source.suffix.casefold() == ".docx":
            blocks = read_docx(source)
        else:
            blocks = read_legacy_doc(source)
    safe_stem = re.sub(r"[^\w.-]+", "_", title, flags=re.UNICODE).strip("_.") or "paper"
    target = folder / f"{safe_stem}.tex"
    target.write_text(tex_document(folder, source, title, blocks), encoding="utf-8")
    return target


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", type=Path, default=Path("papers"), help="directory containing paper subfolders")
    parser.add_argument("--normalize-folder-names", action="store_true", help="replace spaces in immediate subfolder names with underscores")
    parser.add_argument("--paper-title", action="append", default=[], metavar="FOLDER=TITLE", help="choose the intended title for a book/proceedings folder; repeatable")
    parser.add_argument("--compile", action="store_true", help="compile generated files with xelatex; requires XeLaTeX on PATH")
    args = parser.parse_args()
    root = args.root.resolve()
    if not root.is_dir():
        parser.error(f"not a directory: {root}")
    if args.normalize_folder_names:
        normalize_folders(root)
    title_map = {}
    for entry in args.paper_title:
        if "=" not in entry:
            parser.error(f"invalid --paper-title {entry!r}; expected FOLDER=TITLE")
        key, value = entry.split("=", 1)
        title_map[key] = value
    folders = sorted((p for p in root.iterdir() if p.is_dir()), key=lambda p: p.name.casefold())
    if not folders:
        parser.error(f"no subfolders in {root}")
    compiler = shutil.which("xelatex") if args.compile else None
    miktex_engine = shutil.which("miktex-xetex") if args.compile else None
    if args.compile and not miktex_engine:
        local_app_data = os.environ.get("LOCALAPPDATA")
        if local_app_data:
            miktex_bin = Path(local_app_data) / "Programs" / "MiKTeX" / "miktex" / "bin" / "x64"
            candidate = miktex_bin / "miktex-xetex.exe"
            if candidate.is_file():
                miktex_engine = str(candidate)
                if not compiler and (miktex_bin / "xelatex.exe").is_file():
                    compiler = str(miktex_bin / "xelatex.exe")
    if args.compile and not compiler and not miktex_engine:
        parser.error("--compile requires xelatex (or MiKTeX's miktex-xetex) on PATH")
    failed = 0
    for folder in folders:
        try:
            out = process_folder(folder, title_map.get(folder.name))
            print(f"Wrote {out}")
            if compiler:
                run = subprocess.run([compiler, "-interaction=nonstopmode", "-halt-on-error", out.name], cwd=folder, capture_output=True, text=True)
                if run.returncode and miktex_engine:
                    run = subprocess.run(
                        [miktex_engine, "--undump=xelatex", "--disable-installer", "--miktex-disable-maintenance", "--miktex-disable-diagnose", "-interaction=nonstopmode", "-halt-on-error", out.name],
                        cwd=folder,
                        capture_output=True,
                        text=True,
                    )
                if run.returncode:
                    print(run.stdout[-3000:] + run.stderr[-1000:], file=sys.stderr)
                    failed += 1
                else:
                    print(f"Compiled {out.with_suffix('.pdf')}")
            elif miktex_engine:
                run = subprocess.run(
                    [miktex_engine, "--undump=xelatex", "--disable-installer", "--miktex-disable-maintenance", "--miktex-disable-diagnose", "-interaction=nonstopmode", "-halt-on-error", out.name],
                    cwd=folder,
                    capture_output=True,
                    text=True,
                )
                if run.returncode:
                    print(run.stdout[-3000:] + run.stderr[-1000:], file=sys.stderr)
                    failed += 1
                else:
                    print(f"Compiled {out.with_suffix('.pdf')}")
        except Exception as exc:
            print(f"ERROR {folder}: {exc}", file=sys.stderr)
            failed += 1
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
