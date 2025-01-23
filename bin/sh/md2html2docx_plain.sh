pandoc $1 -f markdown -t html  > /tmp/out.html; pandoc  /tmp/out.html -f html -t docx > /tmp/out.docx; soffice /tmp/out.docx &

# pandoc examples/example.md -f markdown -t html  > /tmp/out.html; pandoc  /tmp/out.html -f html -t docx --reference-doc template/template.docx > /tmp/out.docx; soffice /tmp/out.docx &v