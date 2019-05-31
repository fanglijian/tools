<?php

srand(time());
function uuid()
{
	$gUUIDSet = 'abcdefghijklmnopqistuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
	$l = strlen($gUUIDSet);
	$res = 'F';
	for ( $i = 0; $i < 15; $i ++ )
	{
		$j = rand() % $l;
		$res .= $gUUIDSet[$j];
	}
	return $res;
}

$fp = 0;
$s1 = null;
$s2 = null;
if ( $argc > 2)
{
	$fp = $argv[1];
	$s1 = $argv[2];
	if ( $argc > 3)
		$s2 = $argv[3];
}
if ( null == $fp || null == $s1 )
{
	die("invalid arguments\n filePath strRep [newStr]\n");
}
if(!file_exists($fp))
{
	die("No File\n");
}

$f = fopen($fp, 'r');
$content = null;
$repHash = array();

if ( '-id' == $s1 )
{
	while(($line = fgets($f)) !== FALSE)
	{
		$line = trim($line);
		$i = strpos($line, 'id=',0);
		if ( $i === 0 )
		{
			$s1 = substr($line, 3,16);
			$s2 = uuid();
			$repHash[$s1] = $s2;
		}
    }
}
else if ( '-time' == $s1 )
{
	if ( null == $s2 )
		die('empty time');
	$iR = preg_match('/^\\d{10,10}$/', $s2);
	if ( $iR < 1)
		die('invalid time');
	while(($line = fgets($f)) !== FALSE)
	{
		$line = trim($line);
		$iR = preg_match('/^.+=(\\d{10,10})$/', $line, $mat);
		if ( $iR > 0 )
		{
			$repHash[$mat[1]] = $s2;
		}
    }	
}
else
{
	if ( null == $s2 )
		$s2 = uuid();
	$repHash[$s1] = $s2;
}

fseek($f, 0);
while(($line = fgets($f)) !== FALSE)
{
	foreach ($repHash as $key => $value) {
		$line = str_replace($key, $value, $line);
	}
	if ( null == $content )
		$content = $line;
	else
		$content .= $line;
}
fclose($f);
if ( null != $content )
{
	$np = $fp. '.replace';
	$f = fopen($np, 'w');
	fwrite($f, $content);
	fclose($f);
	$tp = $fp . '.bak';
	rename($fp, $tp);
	rename($np, $fp);
}