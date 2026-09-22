#!/usr/bin/env python3
"""Check a built documentation site without a browser or external requests.

Checks local file/fragment references, duplicate IDs, one main landmark and a
page title. Reports scripts and remote resources; does not claim visual or AT QA.
"""
from __future__ import annotations
import argparse
import json
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.ids = []
        self.scripts = 0
        self.remote = []
        self.main = 0
        self.title = False

    def handle_starttag(self, tag, items):
        attributes = dict(items)
        if 'id' in attributes:
            self.ids.append(attributes['id'])
        if tag == 'script':
            self.scripts += 1
        if tag == 'main':
            self.main += 1
        if tag == 'title':
            self.title = True
        for attribute in ('href', 'src'):
            if attribute in attributes:
                target = attributes[attribute]
                self.links.append(target)
                if tag != 'a' and urlsplit(target).scheme in ('http', 'https'):
                    self.remote.append(target)


def check_site(directory: Path) -> dict:
    root = directory.resolve()
    if not (root / 'index.html').is_file():
        raise ValueError('The site index is missing; run tools/build_site.py first.')
    pages = {}
    for path in sorted(root.rglob('*.html')):
        parser = Page()
        parser.feed(path.read_text(encoding='utf-8'))
        pages[path.resolve()] = parser
    missing, anchors, duplicates = [], [], []
    references = 0
    for path, page in pages.items():
        name = path.relative_to(root).as_posix()
        if len(page.ids) != len(set(page.ids)):
            duplicates.append(name)
        for target in page.links:
            parsed = urlsplit(target)
            if parsed.scheme or parsed.netloc:
                continue
            destination = (path.parent / unquote(parsed.path)).resolve() if parsed.path else path
            references += 1
            if not destination.exists():
                missing.append([name, target])
            elif parsed.fragment and destination in pages and unquote(parsed.fragment) not in pages[destination].ids:
                anchors.append([name, target])
    landmark_errors = [path.relative_to(root).as_posix() for path, page in pages.items()
                       if page.main != 1 or not page.title]
    scripts = sum(page.scripts for page in pages.values())
    remote = sum(len(page.remote) for page in pages.values())
    passed = not (missing or anchors or duplicates or landmark_errors or scripts or remote)
    return {
        'status': 'passed' if passed else 'failed',
        'htmlFiles': len(pages), 'localReferences': references,
        'missingTargets': missing, 'missingAnchors': anchors, 'duplicateIdPages': duplicates,
        'scripts': scripts, 'remoteResources': remote, 'missingMainOrTitle': landmark_errors,
        'notChecked': ['browser visual layout', 'assistive technology', 'external citation availability'],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('directory', type=Path)
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    try:
        result = check_site(args.directory)
        if args.report:
            args.report.parent.mkdir(parents=True, exist_ok=True)
            args.report.write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
        print(json.dumps(result, indent=2))
        return 0 if result['status'] == 'passed' else 1
    except (ValueError, OSError) as exc:
        print(json.dumps({'error': str(exc)}))
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
