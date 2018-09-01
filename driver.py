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


def extract_props(src=config.raw_hanja, dest=Path(config.props_hanja)):
    if dest.exists():
        print('exists: {}'.format(dest))
        return
    else:
        print('extract: {}'.format(dest))

        
    from ast import literal_eval

    with open(src) as ifile, open(dest, 'w') as ofile:
        for line in ifile:
            line = line.rstrip()
            character, template = literal_eval(line)

            props = dict()            
            for item in template.replace('{{', '').replace('}}', '').split('|'):
                kv = item.split('=')
                if len(kv) == 2:
                    key, value = kv
                    value = value.replace('[[', '').replace(']]', '').replace('\t', '')
                    value = value.replace('1. ', '').replace('2. ', '')
                    value = value.split(',')
                    value = [x.strip() for x in value]
                    props[key] = value

            for key in ['음2', '음3', '음4', '음5']:
                props['음'] = props.get('음', []) + props.get(key, [])
                props.pop(key, None)
                
            props['글자'] = character

            if '신자체' in props or '간체' in props:
                continue
            
            if not props.get('음'):
                continue
                
            print(repr(props), file=ofile)


def run():
    fetch()
    extract_raw_hanja()
    extract_props()

    
if __name__ == '__main__':
    run()
