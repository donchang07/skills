#!/usr/bin/env python3
"""Inspect editable narrative and preservation contracts; never claims visual QA."""
import argparse
import hashlib
import json
import posixpath
import sys
import zipfile
from pathlib import Path
from urllib.parse import unquote
import xml.etree.ElementTree as ET

P = 'http://schemas.openxmlformats.org/presentationml/2006/main'
A = 'http://schemas.openxmlformats.org/drawingml/2006/main'
R = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'
NS = {'p': P, 'a': A}
ROLES = {'content', 'toc', 'part', 'cover', 'profile', 'closing'}
FIXED = {'cover', 'profile', 'closing'}


def managed(name):
    return name.lower().startswith(('story explanation', 'changppt narrative')) or name.lower() in {'story headline', 'story detail'}


def text(element):
    return ''.join(n.text or '' for n in element.iter('{' + A + '}t'))


def canonical(element):
    # Expanded namespace names avoid namespace-prefix serialization differences.
    return (element.tag, tuple(sorted(element.attrib.items())), element.text or '',
            tuple(canonical(child) for child in element))


def shapes(root):
    tree = root.find('p:cSld/p:spTree', NS)
    result = []
    if tree is None:
        return result
    for shape in tree:
        properties = shape.find('.//p:cNvPr', NS)
        if properties is not None:
            result.append((properties.get('name', ''), shape))
    return result


def resolve_part(part, target):
    target = unquote(target)
    resolved = posixpath.normpath(target.lstrip('/') if target.startswith('/') else posixpath.join(posixpath.dirname(part), target))
    if resolved.startswith('../') or resolved == '..':
        raise ValueError('Relationship target escapes package: ' + target)
    return resolved


class Deck:
    def __init__(self, path):
        self.path = Path(path)
        with zipfile.ZipFile(path) as package:
            bad = package.testzip()
            if bad:
                raise ValueError('ZIP integrity failure: ' + bad)
            self.parts = {n: package.read(n) for n in package.namelist() if not n.endswith('/')}
        presentation = ET.fromstring(self.parts['ppt/presentation.xml'])
        self.size = presentation.find('p:sldSz', NS).attrib
        relations = self.relations('ppt/presentation.xml')
        self.slides = {}
        for index, node in enumerate(presentation.findall('p:sldIdLst/p:sldId', NS), 1):
            rid = node.get('{' + R + '}id')
            relation = relations[rid]
            if not relation.get('Type', '').endswith('/slide') or relation.get('TargetMode') == 'External':
                raise ValueError('Invalid presentation slide relationship: ' + str(rid))
            part = resolve_part('ppt/presentation.xml', relation['Target'])
            root = ET.fromstring(self.parts[part])
            if root.tag != '{' + P + '}sld':
                raise ValueError('Invalid slide XML: ' + part)
            identifier = node.get('id')
            if identifier in self.slides:
                raise ValueError('Duplicate SlideID: ' + identifier)
            self.slides[identifier] = {'index': index, 'part': part, 'root': root}

    def relations(self, part):
        relpart = posixpath.join(posixpath.dirname(part), '_rels', posixpath.basename(part) + '.rels')
        return {n.get('Id'): n.attrib for n in ET.fromstring(self.parts[relpart])} if relpart in self.parts else {}

    def notes(self, slide):
        found = []
        for relation in self.relations(slide['part']).values():
            if relation.get('Type', '').endswith('/notesSlide'):
                if relation.get('TargetMode') == 'External':
                    raise ValueError('External notes relationship')
                found.append(self.parts[resolve_part(slide['part'], relation['Target'])])
        return found


def inspect(source, result, contract):
    findings = []

    def fail(code, message, identifier=None):
        entry = {'code': code, 'message': message}
        if identifier is not None:
            entry['slide_id'] = str(identifier)
        findings.append(entry)

    if source.size != result.size:
        fail('size_changed', 'Source and result dimensions differ.')
    if list(source.slides) != list(result.slides):
        fail('slide_order_changed', 'Stable SlideID list or order changed.')
    rows = contract.get('slides')
    if not isinstance(rows, list):
        raise ValueError('Contract slides must be a list.')
    font = float(contract.get('font_size_pt', 14)) * 100
    if font <= 0:
        raise ValueError('font_size_pt must be positive.')
    seen = set()
    for row in rows:
        identifier = str(row['slide_id'])
        role = row.get('role')
        if identifier in seen or role not in ROLES:
            raise ValueError('Duplicate SlideID or invalid role: ' + identifier)
        seen.add(identifier)
        slide = result.slides.get(identifier)
        if slide is None:
            fail('slide_missing', 'Contract SlideID absent from result.', identifier)
            continue
        if 'slide_index' in row and int(row['slide_index']) != slide['index']:
            fail('slide_index_mismatch', 'Optional index does not match stable SlideID.', identifier)
        objects = [(name, shape) for name, shape in shapes(slide['root']) if managed(name)]
        if role != 'content':
            if objects:
                fail('excluded_has_narrative', 'Excluded role contains managed narrative shapes.', identifier)
            if role in FIXED:
                original = source.slides.get(identifier)
                if original is None or source.parts[original['part']] != result.parts[slide['part']]:
                    fail('fixed_slide_changed', 'Fixed-role slide XML is not byte-identical.', identifier)
            continue
        for kind in ('headline', 'detail'):
            expected = row.get(kind)
            if not isinstance(expected, str) or not expected.strip():
                raise ValueError('Content requires nonempty headline/detail: ' + identifier)
            label = 'Story ' + kind
            candidates = [shape for name, shape in objects if name == label or name.lower().startswith('changppt narrative ' + kind)]
            if len(candidates) != 1:
                fail('narrative_count', kind + ' must have exactly one managed text shape.', identifier)
                continue
            shape = candidates[0]
            if text(shape) != expected:
                fail('narrative_text', kind + ' text differs from contract.', identifier)
            paragraphs = shape.findall('.//a:p', NS)
            if len(paragraphs) != 1 or shape.findall('.//a:br', NS) or '\n' in text(shape) or '\r' in text(shape):
                fail('narrative_break', kind + ' contains an explicit extra paragraph/line break.', identifier)
            for paragraph in paragraphs:
                props = paragraph.find('a:pPr', NS)
                if props is None or props.get('algn') != 'ctr':
                    fail('narrative_alignment', kind + ' must explicitly align centre.', identifier)
            for run in shape.findall('.//a:r', NS):
                if not text(run):
                    continue
                props = run.find('a:rPr', NS)
                try:
                    size = float(props.get('sz', -1)) if props is not None else -1
                except ValueError:
                    size = -1
                bold = props.get('b', '0') if props is not None else '0'
                if size != font or (kind == 'headline' and bold not in {'1', 'true'}) or (kind == 'detail' and bold not in {'0', 'false'}):
                    fail('narrative_format', kind + ' font size or bold/regular differs.', identifier)
        extra_text = [name for name, shape in objects if text(shape) and name not in {'Story headline', 'Story detail'} and not name.lower().startswith(('changppt narrative headline', 'changppt narrative detail'))]
        if extra_text:
            fail('extra_managed_text', 'Unexpected managed narrative text: ' + ', '.join(extra_text), identifier)

    for identifier, slide in source.slides.items():
        final = result.slides.get(identifier)
        if final is None:
            continue
        if contract.get('preserve_nonstory', True):
            original_shapes = [canonical(shape) for name, shape in shapes(slide['root']) if not managed(name)]
            final_shapes = [canonical(shape) for name, shape in shapes(final['root']) if not managed(name)]
            if original_shapes != final_shapes:
                fail('nonstory_changed', 'Non-managed shape XML changed.', identifier)
        if contract.get('preserve_notes', True) and source.notes(slide) != result.notes(final):
            fail('notes_changed', 'Notes bytes changed.', identifier)
    if contract.get('preserve_brand', True):
        def brand(deck):
            return {name: data for name, data in deck.parts.items() if name.startswith(('ppt/slideMasters/', 'ppt/slideLayouts/'))}
        if brand(source) != brand(result):
            fail('brand_changed', 'Master/layout package parts changed.')
    return {'status': 'failed' if findings else 'passed', 'findings': findings,
            'source_sha256': hashlib.sha256(source.path.read_bytes()).hexdigest(),
            'result_sha256': hashlib.sha256(result.path.read_bytes()).hexdigest(),
            'slide_count': len(result.slides), 'contract_slide_count': len(rows),
            'visual_validation': {'status': 'not_run', 'reason': 'OOXML-only inspection cannot establish wrapping, fit, optical centring or actual font rendering.'}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ('source', 'result', 'contract', 'report'):
        parser.add_argument('--' + name, type=Path, required=True)
    args = parser.parse_args()
    if args.report.resolve() in {args.source.resolve(), args.result.resolve(), args.contract.resolve()}:
        parser.error("--report must not overwrite source, result or contract.")
    try:
        report = inspect(Deck(args.source), Deck(args.result), json.loads(args.contract.read_text(encoding='utf-8-sig')))
    except (OSError, KeyError, ValueError, TypeError, ET.ParseError, zipfile.BadZipFile) as error:
        report = {'status': 'failed', 'findings': [{'code': 'invalid_input', 'message': str(error)}], 'visual_validation': {'status': 'not_run'}}
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'status': report['status'], 'finding_count': len(report['findings']), 'visual_validation': 'not_run'}, ensure_ascii=True))
    return 0 if report['status'] == 'passed' else 1


if __name__ == '__main__':
    sys.exit(main())
