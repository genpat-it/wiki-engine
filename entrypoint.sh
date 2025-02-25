#!/bin/bash

if [ "$1" = "build" ]; then
    # Create font cache
    echo "#######################################"
    echo "########## Loading fonts... ###########"
    echo "#######################################"
    mkdir -p /wiki/cache
    HOME=/wiki/cache fc-cache -fv
    
    # md2html2docx_ref
    echo "#####################################################"
    echo "########## Generating DOCX version... ###########"
    echo "#####################################################"
    mkdir -p /wiki/target/tmp /wiki/target/docx /wiki/target/html
    #cp -r /wiki/target/tmp/media /app/media

    if [ "$2" = "--docs-dir" ] && [ -n "$3" ]; then
        echo "Running concat_md_files.py with --docs-dir $3"
        python /app/bin/concat_md_files.py --docs-dir "$3"
    else
        echo "Running concat_md_files.py with default docs-dir"
        python /app/bin/concat_md_files.py
    fi

    perl /app/bin/md2html2docx_ref.pl /wiki/target/tmp/all_docs.md /wiki/templates/template.docx
    mv /tmp/out.docx /wiki/target/docx/out.docx
    
    #pandoc
    echo "########################################"
    echo "########## Generating HTML version... ###########"
    echo "########################################"
    pandoc -s /wiki/target/tmp/all_docs.md -o /wiki/target/html/out.html
    
    #cleaning
    echo "##############################################"
    echo "########## Cleaning tmp folders... ###########"
    echo "##############################################"
    rm -rf /wiki/target/tmp
    rm -rf /wiki/cache

    echo -e "\n\n"
    echo "#####################################################################"
    echo "### You can find yuor html and docx versions in the target folder ###"
    echo "#####################################################################"
else
    exec "$@"
fi

# Ensure draw.io script is executable
if [ ! -x /usr/local/bin/drawio-converter ]; then
    chmod +x /usr/local/bin/drawio-converter
fi