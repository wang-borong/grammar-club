# EPUB generation

Similar to PDF generation, EPUB generation also uses Pandoc.
Before using Pandoc to generate the EPUB, we need to convert the original markdown text to Pandoc-compatible markdown.
To achieve this, we extended the conversion script, which has been moved to the root directory of this project, to support EPUB.
You can use the conversion script to convert the markdown text as follows:

```bash
cd epub
python ../markdown-converter.py ../src/content/Preface.md \ 
  ../src/content/Introduction.md \
  ../src/content/Chapter*.md -o grammar-club.md -t epub
```

The -o option specifies the output Pandoc markdown file name, and the -t option specifies the conversion type, which can be either EPUB or LaTeX.

After generating the Pandoc markdown file, we use Pandoc to convert the markdown file to EPUB.
You can use the following command to generate an EPUB:

```bash
pandoc -f markdown -t epub3 --metadata title="语法俱乐部" \
  --resource-path=../src/.vuepress/public \
  --css epub.css --css heti.css grammar-club.md -o grammar-club.epub
```
