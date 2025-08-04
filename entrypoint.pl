#!/bin/perl

my $default_template="/wiki/templates/template.docx";
my $default_docs_folder="docs";  # Default relative path
#
#--------------------------------------------------
#  PARAMETERS CHECK
#--------------------------------------------------
#
my $template="";
my $usetemplate=0;
my $efsa=0;
my $docs_folder=$default_docs_folder;

for(my $i=0; $i<@ARGV; $i++) {
	if($ARGV[$i] =~ /--efsa/i) {
		$efsa=1;
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
}
if($efsa && !( $usetemplate)){
	$template=$default_template;
	if(! -e $template ){
		print "#  ERROR - template is not a file: '$template'";
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
print "#  tmp dirs in /wiki/target/  ";
command("mkdir -p /wiki/target/tmp /wiki/target/docx /wiki/target/html ");
print "#  Loading fonts... ";
command("mkdir -p /wiki/cache");
command("HOME=/wiki/cache fc-cache -fv");
# concat
print "# Running concat_md_files.py: concatenate all the md files\n";
command("python /app/bin/concat_md_files.py --docs-dir $docs_folder");
#
print "#	PANDOC MARKDOWN to DOCX    #";
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
	command("cd /wiki/target/tmp && pandoc all_docs.md -f markdown -t docx $template > /tmp/out.docx");
}
command("mv /tmp/out.docx /wiki/target/docx/out.docx");
#html
print "# Generating HTML version with pandoc\n";
command("pandoc -s /wiki/target/tmp/all_docs.md -o /wiki/target/html/out.html");
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
