FINAL_HTML=$1.changed
echo $FINAL_HTML
sed s/data-custom-style/custom-style/ $1 > $FINAL_HTML
sed -i -E  's|<span custom-style(.*?)</span>|<div custom-style\1</div>|' $FINAL_HTML

pandoc  $FINAL_HTML -f html -t docx  --reference-doc template/template.docx > /tmp/out.docx; soffice /tmp/out.docx &v

