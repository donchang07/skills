#!/usr/bin/env python3
"""Standard-library structural baseline; rendered PPT QA remains separate."""
import argparse
import ast
import posixpath
import re
import sys
import zipfile
from pathlib import Path
from urllib.parse import unquote, urlsplit
import xml.etree.ElementTree as ET


def markdown_targets(text):
    text = re.sub(r"(?ms)^\s*(```|~~~).*?^\s*\1[^\n]*$", "", text)
    text = re.sub(r"`[^`\n]+`", "", text)
    for match in re.finditer(r"!?\[[^\]\n]*\]\(\s*(<[^>]*>|(?:\\.|[^\s)])+)(?:\s+[^)]*)?\)", text):
        yield match.group(1).strip("<>")
    for match in re.finditer(r"(?m)^\s{0,3}\[[^\]]+\]:\s*(<[^>]+>|\S+)", text):
        yield match.group(1).strip("<>")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", type=Path, help="Legacy repository root containing chang-ppt")
    parser.add_argument("--skill-root", type=Path, help="Explicit skill directory")
    args = parser.parse_args()
    root = (args.skill_root or (args.project / "chang-ppt" if args.project else Path(__file__).resolve().parents[1])).resolve()
    failures = []

    def report(label, error=None):
        print(f"{'FAIL' if error else 'PASS'} {label}" + (f": {error}" if error else ""))
        if error:
            failures.append(label)

    skill = root / "SKILL.md"
    try:
        text = skill.read_text(encoding="utf-8-sig")
        front = re.match(r"\A---\s*\n(.*?)\n---(?:\s*\n|$)", text, re.S)
        if not front:
            raise ValueError("missing frontmatter")
        for field in ("name", "description"):
            match = re.search(rf"(?m)^{field}:\s*(.+)$", front.group(1))
            value = match.group(1).strip().strip("\"'") if match else ""
            if not value:
                raise ValueError(f"missing or empty {field}")
            if field == "name" and value != "chang-ppt":
                raise ValueError("name must be chang-ppt")
        report("SKILL.md frontmatter")
    except (OSError, UnicodeError, ValueError) as exc:
        report("SKILL.md frontmatter", str(exc))

    refs = root / "references"
    if not refs.is_dir():
        report("references directory", "missing")
    for doc in [skill, *sorted(refs.rglob("*.md"))]:
        try:
            broken, count = [], 0
            for target in markdown_targets(doc.read_text(encoding="utf-8-sig")):
                target = re.sub(r"\\([() ])", r"\1", target)
                url = urlsplit(target)
                if url.scheme or url.netloc or not url.path:
                    continue
                count += 1
                if not (doc.parent / unquote(url.path)).exists():
                    broken.append(target)
            report(f"links {doc.relative_to(root)} ({count} local)", ", ".join(broken) or None)
        except (OSError, UnicodeError, ValueError) as exc:
            report(f"links {doc.name}", str(exc))

    try:
        code = root / "brand_tables.py"
        ast.parse(code.read_text(encoding="utf-8-sig"), filename=str(code))
        report("brand_tables.py AST (not executed)")
    except (OSError, UnicodeError, SyntaxError) as exc:
        report("brand_tables.py AST", str(exc))

    try:
        with zipfile.ZipFile(root / "template.pptx") as ppt:
            bad = ppt.testzip()
            if bad:
                raise ValueError(f"ZIP CRC error: {bad}")
            report("template.pptx ZIP integrity")
            ns = {"p": "http://schemas.openxmlformats.org/presentationml/2006/main",
                  "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships"}
            presentation = ET.fromstring(ppt.read("ppt/presentation.xml"))
            size = presentation.find("p:sldSz", ns)
            if size is None or int(size.get("cx", "0")) <= 0 or int(size.get("cy", "0")) <= 0:
                raise ValueError("missing or nonpositive presentation dimensions")
            report(f"presentation dimensions {size.get('cx')} x {size.get('cy')} EMU")
            rels = {node.get("Id"): node for node in ET.fromstring(ppt.read("ppt/_rels/presentation.xml.rels"))}
            slides = presentation.findall("p:sldIdLst/p:sldId", ns)
            if not slides:
                raise ValueError("no presentation slides")
            names = set(ppt.namelist())
            for slide in slides:
                rid = slide.get("{" + ns["r"] + "}id")
                rel = rels.get(rid)
                if rel is None or not rel.get("Type", "").endswith("/slide") or rel.get("TargetMode") == "External":
                    raise ValueError(f"invalid slide relationship {rid}")
                target = rel.get("Target", "")
                part = posixpath.normpath(unquote(target).lstrip("/") if target.startswith("/") else posixpath.join("ppt", unquote(target)))
                if not target or part not in names:
                    raise ValueError(f"missing slide target {rid}: {part}")
                if ET.fromstring(ppt.read(part)).tag != "{" + ns["p"] + "}sld":
                    raise ValueError(f"invalid slide XML root: {part}")
            report(f"slide relationship targets ({len(slides)})")
    except (OSError, zipfile.BadZipFile, KeyError, ValueError, ET.ParseError) as exc:
        report("template.pptx structure", str(exc))

    print("NOT_RUN visual rendering, fonts, overlap, master preservation and PowerPoint validation")
    print(f"RESULT {'FAIL' if failures else 'PASS'} structural baseline ({len(failures)} failures)")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
