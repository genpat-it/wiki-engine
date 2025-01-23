FINAL_HTML=$1.changed
echo $FINAL_HTML
sed s/data-custom-style/custom-style/ $1 > $FINAL_HTML
pandoc  $FINAL_HTML -f html -t docx > /tmp/out.docx; soffice /tmp/out.docx &v

