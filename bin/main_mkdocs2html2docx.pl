#!/usr/bin/perl 

$usage=qq{
WIKI-ENGINE () using mmkdocs and pandoc.
From a set of markdown files, builds a static website and docx document.

Take a DIR_MKDOCS dir contains a dir "docs" where markdown and media files are located, and a "docx" dir where documents will be located

Pandoc (used v. 2.5)

usage:
	perl main_mkdocs2html2docx.pl   DIR_MKDOCS 		DOCX_TEMPLATE.docx
output:
	/tmp/out.docx
example:
	cd PROJECT_DIR
	perl bin/main_mkdocs2html2docx.pl   examples/   template/template_tecrep.docx
};
#
#--------------------------------------------------
#  INPUT
#--------------------------------------------------
#
$curr_dir=`pwd`; chomp($curr_dir);

my ($dir, $template)=@ARGV;
if($dir eq ''){
	print $usage; 
	exit;
}
if($dir!~/^\//){
	$dir="$curr_dir/$dir";
}
$dir_mkdocs=		"$dir/mkdocs";
$dir_docx=		"$dir/mkdocs/docx";
$perlscript="$curr_dir/bin/md2html2docx_tecrep.pl";

if(! -d $dir_mkdocs ){
	print $usage; 
	print "ERROR: $dir_mkdocs is not a directory\n"; 
	exit;
}
if(! -d $dir_docx ){
	print $usage; 
	print "ERROR: $dir_docx is not a directory\n"; 
	exit;
}
if(! -e "$perlscript" ){
	print $usage; 
	print "ERROR: $perlscript not reachable\n"; 
	exit;
}
if($template eq '' ){
	if(-e 'template/template_tecrep.docx'){
		$template="$curr_dir/template/template_tecrep.docx";
	}else{
		print $usage; 
		exit;		
	}
}

if($template!~/^\//){
	$template="$curr_dir/$template";
}

#
#--------------------------------------------------
#  MAIN
#--------------------------------------------------
#
my $cmd=qq{
cd $dir_mkdocs;
sudo docker run -it --rm -v \$(pwd):/app efsa-wiki:latest concat;
sudo docker run -it --rm -p 8001:8000 -v \$(pwd):/app efsa-wiki mkdocs build -f mkdocs-efsa.yml
cd $dir_docx;
perl $perlscript all_docs.md $template
};

runbash($cmd);

#
sub runbash {
	my ($cmd)=@_;
	print "run:\n$cmd\n";
	my $ris=qx{$cmd};
	print "$ris";
}#---------------------

