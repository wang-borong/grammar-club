#!/usr/bin/env python

import os
import re
import sys
from html.parser import HTMLParser


def parse_Default(argdict):
    return ''

def parse_GrammarMark(argdict):
    s = ''
    for k, v in argdict.items():
        if k == 'note':
            s = f'[{v}]'
        else:
            print(f'Encounter unknow parsed tag {{{k}: {v}}}, please add it!')

    return s

def parse_GrammarTest(argdict):
    s = ''
    for k, v in argdict.items():
        if k == 'q':
            _v = v.replace('_', r'\_')
            s += f'{_v}'
        elif k == ':c':
            sd = eval(v)
            for _s in sd:
                s += '\\\\\n(A) '+_s
        elif k == 'a':
            s += f'\n\\tcblower\n\\textbf{{{v}}} '
        else:
            print(f'Encounter unknow parsed attr {{{k}: {v}}}, please add it!')
    return s

def parse_GrammarBox(argdict):
    s = ''
    for k, v in argdict.items():
        if k == 'wrong':
            s = f'[Red]'
        else:
            print(f'Encounter unknow parsed attr {{{k}: {v}}}, please add it!')
    return s

def parse_Figure(argdict):
    s = ''
    for k, v in argdict.items():
        if k == 'img':
            fn = os.path.basename(v)
            s = f'({fn})'
        else:
            print(f'Encounter unknow parsed attr {{{k}: {v}}}, please add it!')
    return s

md2tex = {
    r'i': (r'\textit', r'{', parse_Default, r'}'),
    r'b': (r'\textbf', r'{', parse_Default, r'}'),
    r'u': (r'\ul', r'{', parse_Default, r'}'),
    r'p': (r'', None, parse_Default, None),
    r'br': (r'\\', None, parse_Default, None),
    r'div': (r'', None, parse_Default, None),
    r'span': (r'', None, parse_Default, None),
    r'note': (r'\GrammarMark', r'{', parse_GrammarMark, r'}'),
    r'mark': (r'\GrammarMark', r'{', parse_GrammarMark, r'}'),
    r'test': (r'\begin{tcolorbox}'+'\n', None, parse_GrammarTest, '\n'+r'\end{tcolorbox}'),
    r'quote': (r'\begin{Examine}', '\n', parse_GrammarBox, '\n'+r'\end{Examine}'),
    r'card': (r'\begin{tcolorbox}'+'\n', None, parse_GrammarBox, '\n'+r'\end{tcolorbox}'),
    r'tense': (r'![]', None, parse_Figure, '{ width=40% }'),
    r'figure': (r'![]', None, parse_Figure, '{ width=40% }'),
}

# def replace_md_to_tex(tag, data):

class HTMLTag2TexCmd(HTMLParser):

    def __init__(self):
        super().__init__()
        self.container = []

    def handle_starttag(self, tag, attrs):
        if tag not in md2tex:
            print(f'tag {tag} not parsed!')
        ns = md2tex[tag][0]
        if len(attrs) > 0:
            args = {}
            for attr in attrs:
                if attr[1]:
                    args[attr[0]] = attr[1]
                    # print(attr[1])
            parse_func = md2tex[tag][2]
            ns += parse_func(args)
        ns += '' if md2tex[tag][1] == None else md2tex[tag][1]
        self.container.append(ns)

    def handle_endtag(self, tag):
        if md2tex[tag][3] != None:
            self.container.append(md2tex[tag][3])

    def handle_data(self, data):
        data = data.replace(r'_', r'\_')
        self.container.append(data)

    def retrive_text(self):
        text = ''.join(self.container)
        return text

parser = HTMLTag2TexCmd()

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

for file in sys.argv[1:]:
    with open(file, 'r') as f:
        content = f.read()
        content = tune_content(content)
        parser.feed(content)

print(book_header)
print(parser.retrive_text())
