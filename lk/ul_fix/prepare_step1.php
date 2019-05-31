<?php

define('FILE_DIR', './queue/');
$fileNames = [];
$min = (int)0x7fffffff;
$max = 0;
if ($dh = opendir(FILE_DIR))
{
	while (($file = readdir($dh)) !== false)
	{
		if( is_dir(FILE_DIR."/".$file) || $file == "." || $file == ".." || substr($file, -3) != '.ul' )
			continue;
		$Ni = 0;
		if(preg_match('/^(\d+)\D/', $file, $matches) > 0) {
			$Ni = (int)$matches[1];
			if ( $Ni < $min )
				$min = $Ni;
			if ( $Ni > $max )
				$max = $Ni;	
		} else {
			die("wrong .ul file:" . $file . "\n");
		}	
		$fileNames[$Ni] = $file;	
	}
	closedir($dh);
}
$sz = count($fileNames);
if ( $sz == 0 ) {
	die("No .ul files\n");
}

echo 'min ul: ' . $min . "\n";
echo 'max ul: ' . $max . "\n";
echo 'size:' . $sz . "\n";
$outFileName = 'out.ul';
if ( $argc > 1 && null !=  $argv[1] )
	$outFileName = $argv[1];
$outFileName = './' . $outFileName;
$f2 = fopen($outFileName, 'w');
for ( $i = $min; $i <= $max; $i ++ )
{
	$fname = $fileNames[$i];
	if ( null == $fname ) {
		echo "missing " . $i . "\n";
		continue;
	}
	$FILE_PATH = FILE_DIR . $fname;
	$fsz = filesize($FILE_PATH);
	$f = fopen($FILE_PATH, 'rb');
	$parseFirst = false;
	$lastLine = null;
	$content = fread($f, $fsz);
	fclose($f);
	$c = 0;
	while ( $c < 200) {
		$arr = unpack("@" . $c . "/C4head", $content);
		$c1 = $arr['head1'];
		$c2 = $arr['head2'];
		$c3 = $arr['head3'];
		$c4 = $arr['head4'];
		if ( $c1 == 100 && $c2 == 97 && $c3 == 116 && $c4 == 97 ) {
			break;
		}
		$c ++;
	}
	if ( $c >= 200 ) {
		die("cannot find start pos!\n");
	}
	$e = $fsz - 20;
	while ( ($fsz - $e) < 300 ) {
		$arr = unpack("@" . $e . "/C4head", $content);
		$c1 = $arr['head1'];
		$c2 = $arr['head2'];
		$c3 = $arr['head3'];
		$c4 = $arr['head4'];
		if ( $c1 == 0x70 && $c2 == 0x70 && $c3 == 0x64 && $c4 == 0x76 ) {
			break;
		}
		$e --;
	}
	if ( ($fsz - $e) >= 300 ) {
		die("cannot find end pos!\n");
	}
	$s = null;
	$c = $c + 7;
	$e = $e - 2;
	for ($g = $c; $g < $e; $g ++ ) 
	{
		$arr = unpack("@" . $g . "/Chead", $content);
		if ( null == $s )
			$s = chr($arr['head']); 
		else
			$s.=chr($arr['head']); 
	}
	fwrite($f2, $s);
	fwrite($f2, "\n");
}

fclose($f2);