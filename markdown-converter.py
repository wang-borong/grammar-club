#!/usr/bin/env python

import os
import re
import sys
import argparse
from html.parser import HTMLParser


class MDConverter():
    
    def __init__(self) -> None:
        pass
        self.template = {}
        self.et = 0

    def parse_Default(self, argdict):
        return ''

    def get_template(self):
        return self.template

    def get_engine_type(self):
        return self.et

class MD2Tex(MDConverter):

    def __init__(self) -> None:
        super().__init__()
        self.template = {
            r'i': (r'\textit', r'{', self.parse_Default, r'}'),
            r'b': (r'\textbf', r'{', self.parse_Default, r'}'),
            r'u': (r'\ul', r'{', self.parse_Default, r'}'),
            r'p': (r'', None, self.parse_Default, None),
            r'br': (r'\\', None, self.parse_Default, None),
            r'div': (r'', None, self.parse_Default, None),
            r'span': (r'', None, self.parse_Default, None),
            r'note': (r'\GrammarMark', r'{', self.parse_GrammarMark, r'}'),
            r'mark': (r'\GrammarMark', r'{', self.parse_GrammarMark, r'}'),
            r'test': (r'\begin{tcolorbox}'+'\n', None, self.parse_GrammarTest, '\n'+r'\end{tcolorbox}'),
            r'quote': (r'\begin{Examine}', '\n', self.parse_GrammarBox, '\n'+r'\end{Examine}'),
            r'card': (r'\begin{tcolorbox}'+'\n', None, self.parse_GrammarBox, '\n'+r'\end{tcolorbox}'),
            r'tense': (r'![]', None, self.parse_Figure, '{ width=40% }'),
            r'figure': (r'![]', None, self.parse_Figure, '{ width=40% }'),
        }
        self.et = 1

    def parse_GrammarMark(self, argdict):
        s = ''
        for k, v in argdict.items():
            if k == 'note':
                s = f'[{v}]'
            else:
                print(f'Encounter unknow parsed tag {{{k}: {v}}}, please add it!')

        return s

    def parse_GrammarTest(self, argdict):
        s = ''
        for k, v in argdict.items():
            if k == 'q':
                _v = v.replace('_', r'\_')
                s += f'{_v}'
            elif k == ':c':
                sd = eval(v)
                i = 0
                seqs = ['A', 'B', 'C', 'D', 'E', 'F']
                for _s in sd:
                    seq = seqs[i]
                    s += f'\\\\\n{seq}. '+_s
                    i += 1
            elif k == 'a':
                s += f'\n\\tcblower\n\\textbf{{{v}}} '
            else:
                print(f'Encounter unknow parsed attr {{{k}: {v}}}, please add it!')
        return s

    def parse_GrammarBox(self, argdict):
        s = ''
        for k, v in argdict.items():
            if k == 'wrong':
                s = f'[Red]'
            else:
                print(f'Encounter unknow parsed attr {{{k}: {v}}}, please add it!')
        return s

    def parse_Figure(self, argdict):
        s = ''
        for k, v in argdict.items():
            if k == 'img':
                fn = os.path.basename(v)
                s = f'({fn})'
            else:
                print(f'Encounter unknow parsed attr {{{k}: {v}}}, please add it!')
        return s


class MD2EPUB(MDConverter):
    def __init__(self) -> None:
        super().__init__()
        self.template = {
            r'i': (r'_', None, self.parse_Default, r'_'),
            r'b': (r'**', None, self.parse_Default, r'**'),
            r'u': (r'', None, self.parse_Default, r''),
            r'p': ('\n', None, self.parse_Default, '\n'),
            r'br': (r'---', None, self.parse_Default, ''),
            r'div': (r'<div>', None, self.parse_Default, '</div>'),
            r'span': (r'<span>', None, self.parse_Default, '</span>'),
            r'note': (' [___ANCHOR]', None, self.parse_GrammarMark, None),
            r'mark': (' [___ANCHOR]', None, self.parse_GrammarMark, None),
            r'test': (r'::: {.box}'+'\n', None, self.parse_GrammarTest, '\n:::\n'),
            r'quote': (r'::: {.box}', '\n', self.parse_GrammarTest, '\n:::\n'),
            r'card': (r'::: {.box}'+'\n', None, self.parse_GrammarTest, '\n:::\n'),
            r'tense': (r'![]', None, self.parse_Figure, '{ width=60% }'),
            r'figure': (r'![]', None, self.parse_Figure, '{ width=60% }'),
        }
        self.et = 2

    def parse_GrammarMark(self, argdict):
        s = '{___V}'
        for k, v in argdict.items():
            if k == 'note':
                if v == 'S':
                    s = s.replace('___V', '.subject')
                elif v == 'V':
                    s = s.replace('___V', '.verb')
                elif v == 'O':
                    s = s.replace('___V', '.object')
                elif v == 'C':
                    s = s.replace('___V', '.complement')
                elif v == 'A':
                    s = s.replace('___V', '.adverb')
                else:
                    s = s.replace('___V', v)
            else:
                print(f'Encounter unknow parsed tag {{{k}: {v}}}, please add it!')

        return s

    def parse_GrammarTest(self, argdict):
        s = ''
        for k, v in argdict.items():
            if k == 'q':
                s += f'{v}\n\n---\n\n'
            elif k == ':c':
                sd = eval(v)
                i = 0
                seqs = ['A', 'B', 'C', 'D', 'E', 'F']
                for _s in sd:
                    seq = seqs[i]
                    s += f'</br>\n{seq}. '+_s
                    i += 1
            elif k == 'a':
                s += '\n\n---\n\n'
            elif k == 'wrong':
                s += ''
            else:
                print(f'Encounter unknow parsed attr {{{k}: {v}}}, please add it!')
        return s

    def parse_Figure(self, argdict):
        s = ''
        for k, v in argdict.items():
            if k == 'img':
                fn = os.path.basename(v)
                s = f'({fn})'
            else:
                print(f'Encounter unknow parsed attr {{{k}: {v}}}, please add it!')
        return s

class HTMLConverter(HTMLParser):

    def __init__(self, engine):
        super().__init__()
        self.container = []
        self.engine = engine
        self.template = engine.get_template()
        self.et = engine.get_engine_type()

    def handle_starttag(self, tag, attrs):
        if tag not in self.template:
            print(f'tag {tag} not parsed!')
        ns = self.template[tag][0]
        if len(attrs) > 0:
            args = {}
            for attr in attrs:
                if attr[1]:
                    args[attr[0]] = attr[1]
            parse_func = self.template[tag][2]
            ns += parse_func(args)
        ns += '' if self.template[tag][1] == None else self.template[tag][1]
        self.container.append(ns)

    def handle_endtag(self, tag):
        if self.template[tag][3] != None:
            self.container.append(self.template[tag][3])

    def handle_data(self, data):
        processed = False
        if self.et == 1:
            data = data.replace(r'_', r'\_')
        elif self.et == 2:
            if self.container and '___ANCHOR' in self.container[-1]:
                self.container[-1] = self.container[-1].replace('___ANCHOR', data)
                processed = True
        if not processed:
            self.container.append(data)

    def retrive_text(self):
        text = ''.join(self.container)
        return text


def tune_content(content):
    _content = content.replace('## Test', '## 测验')\
        .replace('# 序——我学英语的经验', '# 序——我学英语的经验 {-}')\
        .replace('### 启蒙的老师及语法书', '## 启蒙的老师及语法书 {-}')\
        .replace('### 大学教育', '## 大学教育 {-}')\
        .replace('### 一个晚上看一本小说', '## 一个晚上看一本小说 {-}')\
        .replace('### 享受阅读乐趣的第一步——不求甚解', '## 享受阅读乐趣的第一步——不求甚解 {-}')\
        .replace('### TIME 的挑战', '## TIME 的挑战 {-}')\
        .replace('### 懒人英语学习法', '## 懒人英语学习法 {-}')\
        .replace('# 前言', '# 前言 {-}')\
        .replace('Ⅰ', 'I')\
        .replace('Ⅲ', 'II')
    _content = re.sub(r'####.*?、', '### ', _content)
    _content = re.sub(r'#### ', '### ', _content)
    _content = re.sub(r'### (请.*)', r'**\g<1>**', _content)
    _content = re.sub(r'### (将.*)', r'**\g<1>**', _content)
    _content = re.sub(r'### (译文.*)', r'**\g<1>**', _content)
    _content = re.sub(r'### \d{1,2}\. ', '### ', _content)
    _content = re.sub(r'# 第.*?章 ', '# ', _content)
    _content = re.sub(r'^# ', '\n# ', _content)
    return _content


def md2tex(args):
    engine = MD2Tex()
    parser = HTMLConverter(engine)

    book_header = r"""
    ---
    title: 语法俱乐部
    author:
     - 旋元佑
    date:
     - 2024/09/30

    documentclass: ctexbook
    papersize: a4
    classoption:
     - sub4section
     - fontset=adobe

    indent: true
    listings: true
    numbersections:
     - sectiondepth: 5

    colorlinks: true
    graphics: true

    toc: true

    header-includes:
     - |
       ```{=latex}
       \usepackage{omni} 
       \usepackage{bookmark}

       % \graphicspath{src/.vuepress/}
       ```
    ...

    """

    for file in args.source:
       with open(file, 'r') as f:
           content = f.read()
           content = tune_content(content)
           parser.feed(content)

    with open(args.output, 'w') as f:
        f.write(book_header)
        f.write(parser.retrive_text())

def md2epub(args):
    engine = MD2EPUB()
    parser = HTMLConverter(engine)

    for file in args.source:
        with open(file, 'r') as f:
            content = f.read()
            content = tune_content(content)
            parser.feed(content)

    # print(book_header)
    text = parser.retrive_text()
    text = text.replace('] ', ']{.underline} ')
    text = text.replace('].', ']{.underline}.')
    text = text.replace('</br>', '\n\n')
    with open(args.output, 'w') as f:
        f.write(text)


def cli():
    parser = argparse.ArgumentParser(description='markdown converter (pandoc)')
    parser.add_argument('-t', '--type', default='latex',
                        help='what type to be converted to, latex or epub')
    parser.add_argument('-o', '--output', type=str,
                        help='output file')
    parser.add_argument('source', nargs='+',
                        help='the input markdwon files')
    args = parser.parse_args()
    
    return args

if __name__ == "__main__":
    args = cli()

    if args.type == 'epub':
        md2epub(args)
    else:
        md2tex(args)
