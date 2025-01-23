#!/usr/bin/perl 
$usage=qq{
Pandoc conversion of a file markdown to a docx file with EFSA styles.
Pandoc (used v. 2.5)

usage:
	perl md2html2docx_ref.pl   FILE_MD.md 		EFSA_TEMPLATE.docx
output:
	/tmp/out.docx
example:
	cd PROJECT_DIR
	perl bin/md2html2docx_ref.pl   examples/example.md   template/template.docx
};
#--------------------------------------------------
#  INPUT
#--------------------------------------------------
#
my ($file_md, $template)=@ARGV;
$file_md_changed=		"/tmp/out_changed.md";
$file_html=				"/tmp/out.html";
$file_html_changed=		"/tmp/out_changed.html";
$file_out=				"/tmp/out.docx";
if($file_md eq ''){
	print $usage; 
	exit;
}
if($template eq '' ){
	if(-e 'template/template.docx'){
		$template='template/template.docx'
	}else{
		print $usage; 
		exit;		
	}
}
#
#--------------------------------------------------
#  MAIN
#--------------------------------------------------
#
change_md_with_custom_style();
plain_pandoc_markdown2html();
change_html_correcting_pandoc_error();
ref_based_pandoc_html2docx();
print_output();
#
#--------------------------------------------------
#  FUNCTIONS
#--------------------------------------------------
#
sub change_md_with_custom_style {
	open(F,$file_md);
	$str="";
	while(<F>){
		$r=$_;
		if($r=~/^#\s+(Summary|Table of contents|Abstract|Glossary .*|References.*|Documentation .*)/){
			#
			### NO ### $r=qq|[$1]{custom-style="EFSA_Heading 1 (no number)"}\n|;
		}
		elsif($r=~/^(#+)\s+(\S.*)/){
			#
			### NO ### $num=length($1);
			### NO ### $r=qq|[$2]{custom-style="EFSA_Heading $num"}\n|;
		}
		elsif($r=~/^(\s*)([-*])\s+(\S+.*)/){
			#
			$num=($1 eq '')?'1':'2';
			$r=qq|[$3]{custom-style="List $num"}\n|;
		}else{
			#
			$r=~  s|^Figure \S+: (.*?)|[$1]{custom-style="EFSA_Figure title"}| ;
		}
		#
		$str .= $r;
		#	print "----$r" ;
	}
	close(F);
	str2file($file_md_changed, $str);
}#---------------------------------------------

sub plain_pandoc_markdown2html{
	runbash("pandoc $file_md_changed -f markdown -t html  > $file_html");
}#---------------------------------------------

sub change_html_correcting_pandoc_error{
	#  
	# change 
	#	data-custom-style       -> custom-style
	#	span with custom-style  -> div 
	#	tables th and td adding EFSA specific custom-styles
	#
	open(F,$file_html);
	my $str="";
	while(<F>){
		$r=$_;
		$r=~   s/data-custom-style/custom-style/g  ;
		$r=~  s|<span custom-style(.*?)</span>|<div custom-style$1</div>|g ;
		$str .= $r;
	}
	close(F);
	#
	#	tables td adding EFSA specific custom-styles
	#	
	my @a= split(/<td/,$str);
	my $str="";
	foreach my $r (@a){
		if($r=~/div.*?custom-style/){
			$str.= '<td' .$r;
			next;
		}
		if($r =~ /( .*?>|>)(.*?)<\/td>(.*)/s ){
			$td=$1; $content=$2; $post=$3;
			$content = qq{<div custom-style="EFSA_Table data">$content</div></td>};
			$r=	'<td' .$td . $content . $post;
		}
		$str.= $r;
	}
	# $str=$sss;
	#
	#	tables th and td adding EFSA specific custom-styles
	#	
	$str=~  s|(<th .*?>\|<th>)(.*?)(</th>)|$1<div custom-style="EFSA_Table heading row">$2</div>$3|gs ;

	str2file($file_html_changed, $str);
}#---------------------------------------------

sub ref_based_pandoc_html2docx{
	open(F,$file_html);
	my $str="";
	while(<F>){
		$r=$_;
		$r=~  s|(<img .*?src=")\./media|$1./wiki/target/tmp/media|g ;
		$str .= $r;
	}
	close(F);
	runbash("pandoc  $file_html_changed -f html -t docx  --reference-doc $template > $file_out;");
}#---------------------------------------------

sub print_output{
	print "\n\nOPEN FILE DOCX:\nsoffice $file_out\n";
}
#
#--------------------------------------------------
#  BASIC FUNCTIONS
#--------------------------------------------------
#
sub file2array {
	my ($f)=@_;
	open(F,$f);
	my @a=<F>;
	close(F);
	return \@a;
}#---------------------

sub str2file {
	my ($f,$s)=@_;
	open(F,">$f");
	print F $s;
	close(F);
}#---------------------

sub runbash {
	my ($cmd)=@_;
	print "run:\n$cmd\n";
	my $ris=qx{$cmd};
	print "$ris";
}#---------------------

