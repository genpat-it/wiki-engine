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
    echo "########## Running md2html2docx_ref.pl... ###########"
    echo "#####################################################"
    mkdir -p /wiki/target/tmp /wiki/target/docx /wiki/target/html
    #cp -r /wiki/target/tmp/media /app/media
    python /app/bin/concat_md_files.py
    perl /app/bin/md2html2docx_ref.pl /wiki/target/tmp/all_docs.md /wiki/templates/template.docx
    mv /tmp/out.docx /wiki/target/docx/out.docx
    
    #pandoc
    echo "########################################"
    echo "########## Running pandoc... ###########"
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