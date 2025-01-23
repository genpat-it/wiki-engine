my $tbody=0;
while(<>){
	$r=$_;
	if( $r=~ /<tbody>/ ){
		$tbody=1;
	}elsif( $r=~ /<\/tbody>/ ){
		$tbody=0;
	}
	
	if($tbody==1){
		$r=~s/<th>/<td>/g;
		$r=~s/<th /<td /g;
		$r=~s/<\/th>/<\/td>/g;
	}

	print	$r;
}
