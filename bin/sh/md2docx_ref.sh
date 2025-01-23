pandoc $1 -f markdown -t docx --reference-doc template/template.docx > /tmp/out.docx

# pandoc examples/example.md -f markdown -t docx --reference-doc template/template.docx > /tmp/out.docx