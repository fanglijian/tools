<?php

define('FILE_DIR', './');

$FILE_PATH = FILE_DIR . $argv[1];
$f = fopen($FILE_PATH, 'r');
$min = (int)0x7fffffff;
$max = 0;
while(($line = fgets($f)) !== FALSE)
{
	if(preg_match('/(\d+)\D/', $line, $matches) > 0)
	{
		$i = (int)$matches[1];
		if ( $i < $min )
		  $min = $i;
		if ( $i > $max )
		  $max = $i;
	}
}
fclose($f);
echo 'min: ' . $min . "\nmax: " . $max . "\nnum: " . ($max - $min) . "\ntime: ~" . ($max - $min) / 90;