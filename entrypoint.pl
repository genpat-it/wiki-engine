#!/bin/perl

my $default_template="/wiki/templates/template.docx";
my $default_docs_folder="docs";  # Default relative path
my $default_index_file="index.md";  # Default index file
my $mkdocs=0;
#
#--------------------------------------------------
#  PARAMETERS CHECK
#--------------------------------------------------
#
my $template="";
my $usetemplate=0;
my $efsa=0;
my $docs_folder=$default_docs_folder;
my $index_file=$default_index_file;

for(my $i=0; $i<@ARGV; $i++) {
	if($ARGV[$i] =~ /--efsa/i) {
		$efsa=1;
	}
  if($ARGV[$i] =~ /--mkdocs/i) {
    $mkdocs=1;
  }
	if($ARGV[$i] =~ /--template/i) {
		$usetemplate=1;
		$template=($i+1 < @ARGV)? 
						$ARGV[$i+1]:
						$default_template;
		if( -e $template ){
			print "#  Using template: $template\n";
		}else{
			print "#  ERROR - template is not a file: '$template'\n";
			exit(1);
		}
		$i++; # Skip next argument as it's the template path
	}
	if($ARGV[$i] =~ /--docs-dir/i) {
			$docs_folder=($i+1 < @ARGV)? 
											$ARGV[$i+1]:
											$default_docs_folder;
			my $full_docs_path = "/wiki/$docs_folder";
			if( -d $full_docs_path ){
					print "#  Using docs folder: $docs_folder\n";
			}else{
					print "#  ERROR - docs folder does not exist: '$full_docs_path'\n";
					exit(1);
			}
			$i++; # Skip next argument as it's the docs path
	}
	if($ARGV[$i] =~ /--index-file/i) {
			$index_file=($i+1 < @ARGV)? 
											$ARGV[$i+1]:
											$default_index_file;
			my $full_index_path = "/wiki/$docs_folder/$index_file";
			if( -f $full_index_path ){
					print "#  Using index file: $index_file\n";
			}else{
					print "#  ERROR - index file does not exist: '$full_index_path'\n";
					exit(1);
			}
			$i++; # Skip next argument as it's the index file path
	}
}
if($efsa && !( $usetemplate)){
	$template=$default_template;
	if(! -e $template ){
		print "#  ERROR - template is not a file: '$template'\n";
		exit(1);
	}
}
#--------------------------------------------------
#  MAIN
#--------------------------------------------------
#
my $text=($efsa)?"EFSA COMPATIBLE":"STANDARD";
print qq{
#--------------------------------------------------
#  Generate $text DOCX	
#--------------------------------------------------
};
# Create font cache
print "#  tmp dirs in /wiki/target/\n";
command("mkdir -p /wiki/target/tmp /wiki/target/docx /wiki/target/html ");
print "#  Loading fonts...\n";
command("mkdir -p /wiki/cache");
command("HOME=/wiki/cache fc-cache -fv");
# concat
if ($mkdocs) {
  print "#  MkDocs mode enabled\n";
  print "# Running concat_md_files_for_mkdocs.py: concatenate all the md files\n";
  command("python /app/bin/concat_md_files_for_mkdocs.py --docs-dir $docs_folder --index-file $index_file");
  print "#  copying mkdocs_cfg.yml\n";
  if (! -d "/wiki/target/md_for_mkdocs") {
    command("mkdir -p /wiki/target/md_for_mkdocs");
  }
  command("cp /app/bin/mkdocs_cfg.yml /wiki/target/md_for_mkdocs/");
  command("cp /app/plugins/init/main.py /wiki/target/md_for_mkdocs/");
  print "#  Running mkdocs build\n";
  command("mkdocs build -f /wiki/target/md_for_mkdocs/mkdocs_cfg.yml --site-dir /wiki/target/md_for_mkdocs/site");
}
print "# Running concat_md_files.py: concatenate all the md files\n";
command("python /app/bin/concat_md_files.py --docs-dir $docs_folder --index-file $index_file");
#
print "#	PANDOC MARKDOWN to DOCX\n";
#
if($efsa){
	print qq{
	#
	# EFSA case: manipulate the md file to be compatible with EFSA template
	# 
	};
	command("cd /wiki/target/tmp && perl /app/bin/md2html2docx_ref.pl all_docs.md $template");
}else{
	print qq{
	#
	# STANDARD case
	# 
	};
	$template=($usetemplate)? " --reference-doc $template":"";
	command("cd /wiki/target/tmp && pandoc all_docs.md -f markdown -t docx --filter pandoc-plantuml $template -o /tmp/out.docx");
}
command("mv /tmp/out.docx /wiki/target/docx/out.docx");
#html
print "# Generating HTML version with pandoc\n";
command("mkdir -p /wiki/target/html/plantuml-images");
command("cp -r /wiki/target/tmp/plantuml-images /wiki/target/html/ 2>/dev/null || true");
command("cd /wiki/target/html && pandoc -s ../tmp/all_docs.md --filter pandoc-plantuml -o out.html");
#cleaning
print "#  Cleaning tmp folders...\n";
command("rm -rf /wiki/target/tmp /wiki/cache");

print qq{
### DONE!
### You can find your html and docx versions in the target/docx and target/html folders 
###
};
#--------------------------------------------------
#  FUNCTIONS
#--------------------------------------------------
#
sub command() { my($cmd) = @_;
	print "Running command: $cmd";
	$ris=qx{$cmd};
	if($ris) {
		print "Result\n$ris";
	}
	if($?) {
		print "Error: $cmd";
		exit 1;
	}
}
