import sys
import re
import subprocess

usage = """
Pandoc conversion of a file markdown to a docx file with EFSA styles.
Pandoc (used v. 2.5)
usage:
    python md2html2docx_ref.py   FILE_MD.md       EFSA_TEMPLATE.docx
    output:
    /tmp/out.docx
    example:
    cd PROJECT_DIR
    python bin/md2html2docx_ref.py   examples/example.md   template/template.docx
"""

#--------------------------------------------------
#  INPUT
#--------------------------------------------------



# Get the input markdown file and template from command line arguments
if len(sys.argv) != 3:
	sys.argv = (sys.argv[0] + " examples/example.md template/template.docx").split()
	print( f'{a[0]} {a[1]}  {a[2]}')
	#print(usage)
	sys.exit(1)

file_md, template = sys.argv[1], sys.argv[2]
file_md_changed = "/tmp/out_changed.md"
file_html = "/tmp/out.html"
file_html_changed = "/tmp/out_changed.html"
file_out = "/tmp/out.docx"

if not template:
    print(usage)
    sys.exit(1)

#--------------------------------------------------
#  MAIN
#--------------------------------------------------

def main():
    change_md_with_custom_style()
    plain_pandoc_markdown2html()
    change_html_correcting_pandoc_error()
    ref_based_pandoc_html2docx()
    print_output()

#--------------------------------------------------
#  FUNCTIONS
#--------------------------------------------------

def change_md_with_custom_style():
    # Open the markdown file and read its content
    with open(file_md, 'r') as f:
        content = f.readlines()

    new_content = []
    for line in content:
        # Apply custom styles based on the content of each line
        if R := re.match(r'^#\s+(Summary|Table of contents|Abstract|Glossary .*|References.*|Documentation .*)', line):
            print (f'[{R.group(1)}]{{custom-style="EFSA_Heading 1 (no number)"}}\n')
            new_content.append(f'[{R.group(1)}]{{custom-style="EFSA_Heading 1 (no number)"}}\n')
        elif re.match(r'^(#+)\s+(\S.*)', line):
            num = len(re.match(r'^(#+)', line).group(1))
            new_content.append(f'[{line.strip()}]{{custom-style="EFSA_Heading {num}"}}\n')
        elif re.match(r'^(\s*)([-*])\s+(\S+.*)', line):
            num = '1' if re.match(r'^(\s*)', line).group(1) == '' else '2'
            new_content.append(f'[{line.strip()}]{{custom-style="EFSA_Bullet {num}"}}\n')
        else:
            new_content.append(re.sub(r'^Figure \S+: (.*?)', r'[\1]{custom-style="EFSA_Figure title"}', line))

    # Write the modified content to a new markdown file
    with open(file_md_changed, 'w') as f:
        f.writelines(new_content)

def plain_pandoc_markdown2html():
    # Convert the modified markdown file to HTML using Pandoc
    runbash(f"pandoc {file_md_changed} -f markdown -t html > {file_html}")

def change_html_correcting_pandoc_error():
    # Open the HTML file and read its content
    with open(file_html, 'r') as f:
        content = f.read()

    # Correct Pandoc errors by modifying the HTML content
    content = re.sub(r'data-custom-style', 'custom-style', content)
    content = re.sub(r'<span custom-style(.*?)</span>', r'<div custom-style\1</div>', content)

    # Split the content by <td> tags and process each part
    parts = content.split('<td')
    new_content = parts[0]
    for part in parts[1:]:
        if 'div' in part and 'custom-style' in part:
            new_content += '<td' + part
            continue
        match = re.match(r'( .*?>|>)(.*?)</td>(.*)', part, re.S)
        if match:
            td, content, post = match.groups()
            content = f'<div custom-style="EFSA_Table data">{content}</div></td>'
            part = '<td' + td + content + post
        new_content += part

    # Add EFSA specific custom styles to <th> and <td> tags
    new_content = re.sub(r'(<th .*?>|<th>)(.*?)(</th>)', r'\1<div custom-style="EFSA_Table heading row">\2</div>\3', new_content, flags=re.S)

    # Write the modified HTML content to a new file
    with open(file_html_changed, 'w') as f:
        f.write(new_content)

def ref_based_pandoc_html2docx():
    # Convert the modified HTML file to DOCX using Pandoc with the specified template
    runbash(f"pandoc {file_html_changed} -f html -t docx --reference-doc {template} > {file_out}")

def print_output():
    # Print the path to the output DOCX file
    print(f"\n\nOPEN FILE DOCX:\nsoffice {file_out}\n")

#--------------------------------------------------
#  BASIC FUNCTIONS
#--------------------------------------------------

def runbash(cmd):
    # Execute a shell command and print its output
    print(f"run:\n{cmd}\n")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    print(result.stdout)

if __name__ == "__main__":
    main()
    