<?php

define('FILE_DIR', './');

$FILE_PATH = FILE_DIR . $argv[1];
$f = fopen($FILE_PATH, 'r');
$client_id = null;
$item_name = null;
$item_id = null;
$pos_owner_id = null;
$pos_owner_name = null;
$onlyCheck = false;
$insSpace = 4;
if ( $argc > 1)
{
	for ($i = 2; $i < $argc; $i ++ )
	{
		if ( $argv[$i] == 'check') {
			$onlyCheck = true;
		}
		else if ( substr($argv[$i], 0, 6) == 'space=')
			$insSpace = substr($argv[$i], 6, strlen($argv[$i]) - 6);
		else if ( substr($argv[$i], 0, 8) == 'item_id=')
			$item_id = substr($argv[$i], 8, strlen($argv[$i]) - 8);
		else if ( substr($argv[$i], 0, 10) == 'client_id=')
			$client_id = substr($argv[$i], 10, strlen($argv[$i]) - 10);
		else if ( substr($argv[$i], 0, 10) == 'item_name=')
			$item_name = substr($argv[$i], 10, strlen($argv[$i]) - 10);		
		else if ( substr($argv[$i], 0, 13) == 'pos_owner_id=')
			$pos_owner_id = substr($argv[$i], 13, strlen($argv[$i]) - 13);	
		else if ( substr($argv[$i], 0, 15) == 'pos_owner_name=')
			$pos_owner_name = substr($argv[$i], 15, strlen($argv[$i]) - 15);			
	}
}
$sapce = null;
for ( $i = 0; $i < $insSpace; $i ++ )
{
	if (null == $sapce )
		$sapce = ' ';
	else
		$sapce .= ' ';
}
echo 'space:s' . $sapce . "e\n";
echo 'client_id:' . $client_id . "\n";
echo 'item_id:' . $item_id . "\n";
echo 'item_name:' . $item_name . "\n";
echo 'pos_owner_id:' . $pos_owner_id . "\n";
echo 'pos_owner_name:' . $pos_owner_name . "\n";

if (!$onlyCheck)
  $f2 = fopen($FILE_PATH . '.tmp', 'w');

$lc = 1;
$emptArray = [];
while(($line = fgets($f)) !== FALSE)
{	  
	$line = trim($line);
	$arr = explode(' ', $line);
	if ( $arr !== FALSE )
	{
		$sz = count($arr);
		$line = null;
		for ( $g = 0; $g < $sz; $g ++)
		{
			if (null == $arr[$g])
				continue;
			$s = trim($arr[$g]);
			if (empty($s))
				continue;
			if ( null == $line )
				$line = $s;
			else
				$line = $line . $s;
		}	
	}
	$line = str_replace('%00%', 'NULL', $line);
	if( strpos( $line, '=' ) !== false )
	{
		if ( substr($line, -1) == '=' || substr($line, -4) == 'null' || substr($line, -4) == 'NULL' || substr($line, -4) == 'Null' )
		{
			$s = substr($line, 0, strpos($line, '=',0));
			if (array_key_exists($s, $emptArray))
				$emptArray[$s] = $emptArray[$s] + 1;
			else
				$emptArray[$s] = 1;
			if ( $s == 'client_id') {
				if ( null != $client_id ) {
					if (substr($line, -1) != '=') {
						echo $FILE_PATH . ' Line:' . $lc . ' wrong client(' . $line . '), using ' . $client_id . "\n";
						$line = substr($line, 0, strlen($line) - 4) . $client_id;
					} else {
						echo $FILE_PATH . ' Line:' . $lc . ' empty client, using ' . $client_id . "\n";
						$line .= $client_id;
					}
				} else {
					echo $FILE_PATH . ' Line:' . $lc . ' empty client' . "\n";
				}
			}
			else if ( $s == 'item_name') {
				if ( null != $item_name ) {
					if (substr($line, -1) != '=') {
						echo $FILE_PATH . ' Line:' . $lc . ' wrong item  name(' . $line . '), using ' . $item_name . "\n";
						$line = substr($line, 0, strlen($line) - 4) . $item_name;
					} else {
						echo $FILE_PATH .  ' Line:' . $lc . ' empt item  name, using ' . $item_name  . "\n";
						$line .= $item_name;
					}
				}
				else
					echo $FILE_PATH .  ' Line:' . $lc . ' empt item  name' . "\n";
			}
			else if ( $s == 'item_id') {
				if ( null != $item_id ) {
					if (substr($line, -1) != '=') {
						echo $FILE_PATH . ' Line:' . $lc . ' wrong item  id(' . $line . '), using ' . $item_id . "\n";
						$line = substr($line, 0, strlen($line) - 4) . $item_id;
					} else {
						echo $FILE_PATH . ' Line:' . $lc .  ' empt item  id, using ' . $item_id  . "\n";
						$line .= $item_id;
					}
				}
				else
					echo $FILE_PATH . ' Line:' . $lc .  ' empt item  id' . "\n";
			}	
			else if ( $s == 'pos_owner_id') {
				if ( null != $pos_owner_id ) {
					if (substr($line, -1) != '=') {
						echo $FILE_PATH . ' Line:' . $lc . ' wrong pos_owner_id  id(' . $line . '), using ' . $pos_owner_id . "\n";
						$line = substr($line, 0, strlen($line) - 4) . $pos_owner_id;
					} else {
						echo $FILE_PATH . ' Line:' . $lc .  ' empt pos_owner_id, using ' . $pos_owner_id  . "\n";
						$line .= $pos_owner_id;
					}
				}
				else
					echo $FILE_PATH . ' Line:' . $lc .  ' empt pos_owner_id' . "\n";
			}	
			else if ( $s == 'pos_owner_name') {
				if ( null != $pos_owner_name ) {
					if (substr($line, -1) != '=') {
						echo $FILE_PATH . ' Line:' . $lc . ' wrong pos_owner_name  id(' . $line . '), using ' . $pos_owner_name . "\n";
						$line = substr($line, 0, strlen($line) - 4) . $pos_owner_name;
					} else {
						echo $FILE_PATH . ' Line:' . $lc .  ' empt pos_owner_name, using ' . $pos_owner_name  . "\n";
						$line .= $pos_owner_name;
					}
				}
				else
					echo $FILE_PATH . ' Line:' . $lc .  ' empt pos_owner_name' . "\n";
			}							
		}
		$atrLst = explode('=', $line);
		if ( null != $atrLst && count($atrLst) > 0 )
		{
			$ignorAtr = $atrLst[0] == 'deleted' || $atrLst[0] == 'created' || $atrLst[0] == 'updated' || $atrLst[0] == 'saved';
			if ($ignorAtr) 
			{
				$ignorAtr = $atrLst[0] == 'saved' || count($atrLst) == 1;
				if (!$ignorAtr)
				{
					$v = trim($atrLst[1]);
					if ( empty($v) || $v == 'null' || $v == 'NULL' ||$v == 'Null' ||$v == '0' ||$v == '0.0')
						$ignorAtr = true;
				}
				if ($ignorAtr) 
				{
					continue;
				}
			}
		}
	    $line = $sapce . $line;
	}

	if (!$onlyCheck)
	{
		fwrite($f2, $line);
		fprintf($f2, "\n");
	}
	$lc ++;
}

fclose($f);
if (!$onlyCheck)
{
	fclose($f2);
	rename($FILE_PATH, $FILE_PATH . '.bak' );
	rename($FILE_PATH . '.tmp', $FILE_PATH);
}

echo "---- emtpy value ------\n";
foreach ($emptArray as $key => $value) {
	echo $key . ": " . $value . "\n";
}