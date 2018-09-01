#!/usr/bin/env python3

from pathlib import Path
import config


def fetch(srcurl=config.dumpurl, dest=Path(config.dumpbz2)):
    from urllib.request import urlretrieve
    
    if dest.exists():
        print('exists: {}'.format(srcurl))
        return

    print('urlretrieve: {}'.format(srcurl))
    urlretrieve(srcurl, dest)


def parse(src=config.dumpbz2):
    import bz2
    from xml.etree.ElementTree import parse as parsexml

    print('parsexml: {}'.format(src))
    tree = parsexml(bz2.open(src))
    return tree


def extract_raw_hanja(src=config.dumpbz2, dest=Path(config.raw_hanja)):
    if dest.exists():
        print('exists: {}'.format(dest))
        return
    
    import re
    
    tree = parse(src=src)
    ns = {'mw': 'http://www.mediawiki.org/xml/export-0.10/'}
    pattern = re.compile('{{한자풀이[^}]*}}')

    print('extract: {}'.format(dest))
    with open(dest, 'w') as file:

        for pager in tree.findall('mw:page', ns):
            titler = pager.find('mw:title', ns)
            textr = pager.find('mw:revision/mw:text', ns)

            if textr.text:
                m = pattern.search(textr.text.replace('\n', ''))
                if m:
                    x = titler.text, m.group()
                    print(repr(x), file=file)


def run():
    fetch()
    extract_raw_hanja()

    
if __name__ == '__main__':
    run()
