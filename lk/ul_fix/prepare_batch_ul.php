<?php

define('FILE_DIR', './queue/');
$fileNames = [];
$min = (int)0x7fffffff;
$max = 0;
if ($dh = opendir(FILE_DIR))
{
	while (($file = readdir($dh)) !== false)
	{
		if( is_dir(FILE_DIR.$file) || $file == "." || $file == ".." || substr($file, -3) != '.ul' )
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
	if (!array_key_exists($i, $fileNames))
	{
		echo "missing " . $i . "\n";
		continue;
	}
	$fname = $fileNames[$i];
	if ( null == $fname ) {
		echo "null file " . $i . "\n";
		continue;
	}
	echo $fname . "\n";
	$FILE_PATH = FILE_DIR . $fname;
	$f = fopen($FILE_PATH, 'rb');
	$parseFirst = false;
	$lastLine = null;
	$line_array = [];
	while(($line = fgets($f)) !== FALSE)
	{
		if (!$parseFirst) {
			$lastLine = null;
			$c = 16;
			while ( $c < strlen($line) ) {
				$arr = unpack("@" . $c . "/C4head", $line);
				$c1 = $arr['head1'];
				$c2 = $arr['head2'];
				$c3 = $arr['head3'];
				$c4 = $arr['head4'];
				if ( $c1 == 100 && $c2 == 97 && $c3 == 116 && $c4 == 97 ) {
					$ll = strlen($line);
					$c2 = $c + 7;
					if ( $ll > $c2 )
						$lastLine = substr($line, $c2);
					else {
						$line = fgets($f);
						$lastLine = substr($line, 7 - $ll - $c);
					}
					#$c = $c + 7;
					#$cl = strlen($line) - $c;
					#if ( $cl < 0 ) {
					#	echo $fname . "\n";
					#	echo $line . "\n";
					#	echo $c . "\n";
					#	echo($cl . "\n");
					#	$line = fgets($f);
					#	echo $line . "\n";
					#	die('');
					#}
					#$arr = unpack("@" . $c . "/a" . $cl . "tbl", $line);
					#$lastLine = $arr['tbl'];
					break;
				}
				$c ++;
			}
			$parseFirst = true;
			array_push($line_array, $lastLine);
		} else {
			#echo $line . "\n";
			array_push($line_array, $line);
		}
	}
	$line_array_len = count($line_array);
	if ( $line_array_len > 0 ) {
		#echo $line_array_len . "\n";
		for ( $k = $line_array_len - 1; $k >= 0; $k --)
		{
			$line = $line_array[$k];
			#echo $line . "\n";
			$c = 0;
			$end = null;
			while ( $c < strlen($line) - 5) {
				$arr = unpack("@" . $c . "/C5head", $line);
				$c1 = $arr['head1'];
				$c2 = $arr['head2'];
				$c3 = $arr['head3'];
				$c4 = $arr['head4'];
				$c5 = $arr['head5'];	
				if ( $c1 == 0x70 && $c2 == 0x70 && $c3 == 0x64 && $c4 == 0x76 ) {
					$ll = 
					$end = substr($line, 0, $c -2);
					break;
				}
				#$line = substr($line, 1);
				$c ++;
			}
			if ($c < strlen($line) - 5)
			{
				$line_array[$k] = $end;
				break;
			}
			else if ($k > 0)
			{
				$line_array[$k-1] .= $line_array[$k];
			}
		}
		for ( $g = 0; $g <= $k; $g ++ )
		{
			fwrite($f2, $line_array[$g]);
		}
	}
	fclose($f);
	fwrite($f2, "\r\n");
}

fclose($f2);