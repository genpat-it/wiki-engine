FILE_MD=$1
FILE_MD_CHANGED=/tmp/out_changed.md
FILE_HTML=/tmp/out.html
FILE_HTML_CHANGED=/tmp/out_changed.html

#echo "plain pandoc markdown2html  > FILE_HTML"
#echo "sed on examples/example.md  > $FILE_MD"

cp $1 $FILE_MD_CHANGED
sed -i -E  's|^# Summary|# [Summary]{custom-style="EFSA_Heading 1 (no number)"}|' $FILE_MD_CHANGED
sed -i -E  's|^# Table of contents|# [Table of contents]{custom-style="EFSA_Heading 1 (no number)"}|' $FILE_MD_CHANGED

sed -i -E  's|^# (.*)|# [\1]{custom-style="EFSA_Heading 1"}|' $FILE_MD_CHANGED
sed -i -E  's|^## (.*)|# [\1]{custom-style="EFSA_Heading 2"}|' $FILE_MD_CHANGED
sed -i -E  's|^### (.*)|# [\1]{custom-style="EFSA_Heading 3"}|' $FILE_MD_CHANGED
sed -i -E  's|^### (.*)|# [\1]{custom-style="EFSA_Heading 3"}|' $FILE_MD_CHANGED

sed -i -E  's|^([-*])\s+(\S+.*)|- [\2]{custom-style="EFSA_Bullet 1"}|' $FILE_MD_CHANGED
sed -i -E  's|^(\s+[-*])\s+(\S+.*)|\1 [\2]{custom-style="EFSA_Bullet 2"}|' $FILE_MD_CHANGED

sed -i -E  's|^Figure \S+: (.*?)|[\1]{custom-style="EFSA_Figure title"}|' $FILE_MD_CHANGED
#sed -i -E  's|(<td.*?>)(.*?)(</td>)|\1:::{custom-style="EFSA_Table data"}\n\2\n:::\n\3|g' $FILE_MD_CHANGED
#sed -i -E  's|(<th.*?>)(.*?)(</th>)|\1:::{custom-style="EFSA_Table heading row"}\n\2\n:::\n\3|g' $FILE_MD_CHANGED



#echo "plain pandoc markdown2html  > FILE_HTML"
pandoc $FILE_MD_CHANGED -f markdown -t html  > $FILE_HTML

#echo "sed on FILE_HTML  > $FILE_HTML_CHANGED"

cp $FILE_HTML $FILE_HTML_CHANGED
sed -i -E   s/data-custom-style/custom-style/  $FILE_HTML_CHANGED
sed -i -E  's|<span custom-style(.*?)</span>|<div custom-style\1</div>|' $FILE_HTML_CHANGED

sed -i -E  's|(<td.*?>)(.*?)(</td>)|\1<div custom-style="EFSA_Table data">\2</div>\3|gm' $FILE_HTML_CHANGED
sed -i -E  's|(<th.*?>)(.*?)(</th>)|\1<div custom-style="EFSA_Table heading row">\2</div>\3|gm' $FILE_HTML_CHANGED

#echo "ref-based pandoc html2docx $FILE_HTML_CHANGED  > /tmp/out.docx"
pandoc  $FILE_HTML_CHANGED -f html -t docx  --reference-doc template/template.docx > /tmp/out.docx;

#echo soffice 
soffice /tmp/out.docx &




# pandoc $1 -f markdown -t html  > FILE_HTML; pandoc  FILE_HTML -f html -t docx --reference-doc template/template.docx > /tmp/out.docx; soffice /tmp/out.docx &v

# pandoc examples/example.md -f markdown -t html  > FILE_HTML; pandoc  FILE_HTML -f html -t docx --reference-doc template/template.docx > /tmp/out.docx; soffice /tmp/out.docx &v


