# PDF typesetting

## Idea

The main idea behind generating the book in PDF format is to use Pandoc,
as it can convert markdown text to PDF using LaTeX.
However, the original markdown content contains numerous HTML tags,
which need to be converted to LaTeX commands first.
To handle this, we created a Python script to perform the conversion
and generate a completely new markdown file.

Once all HTML tags have been converted to LaTeX commands,
we use the Pandoc tool to convert the new markdown file into a PDF.

## Gerneration

The LaTeX commands or environments used in this book are defined in the package omni.sty, located in this directory.
If you want to perform the convertion yourself, you will need to define the Pandoc command with some options.
However, I have already created a tool to handle this.
You can find it in [this repo](https://github.com/wang-borong/omnidoc).

## How to

```bash
# 1. get a new markdown file
python markdown-latex-ext.py ../src/content/Preface.md \
  ../src/content/Introduction.md \
  ../src/content/Chapter*.md > grammar-club.md
# 2. use my omnidoc tool
# NOTE: because this not a standard omnidoc repo, you can not use omnidoc tool directly.
# However, you can use the makefile to generate the final pdf file.
omnidoc lib -i
mkdir build
TARGET=grammar-club MAIN=grammar-club.md OMNI_PANDOC_OPTS=--resource-path=../src/.vuepress/public \
  make -f ~/.local/share/omnidoc/tool/top.mk pandoc
```
