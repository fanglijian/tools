<?php

require 'base.php';

$db_name = 'shop01';
$shop_id = 0;
$tbl_names = [];
$username = null;
$tbl_name = null;
$code = null;
$session = null;
$query = null;
$check_all = false;

$i = 0;
$s1 = null;
$s2 = null;
if ( $argc > 1)
{	
	for ( $i = 1; $i < $argc - 1; $i ++ )
	{
		$s1 = $argv[$i];
		$s2 = $argv[$i + 1];
		if ( null == $s1 || null == $s2 )
			continue;
		if ( '-c' == $s1 )
			$code = $s2;
		else if ( '-u' == $s1 )
			$username = $s2;		
		else if ( '-d' == $s1 )
			$db_name = $s2;
		else if ( '-s' == $s1 )
			$shop_id = $s2;		
		else if ( '-q' == $s1 )
			$query = $s2;	
		else if ( '-t' == $s1 )
			$tbl_name = $s2;						
	}
}

if ( null != $username && null != $code )
{
	$session = loginRestique($username, $code);
}
if ( null == $session )
	$session = getSavedSession();
if ( null == $session )
	die("No session\n");

if ( null == $tbl_name )
	die("No table name\n");
$items = getDataOfTable($db_name, 105195, $tbl_name, $session);
if ( null == $items )
	die("No items\n");
echo "item count: " . count($items) . "\n";
$sqlite_db = new SQLite3("./main.db");
$notMatchFieldArray = array();
foreach ($items as $item) 
{
	$id = $item['id'];
	if ( null == $id ) 
	{
		echo "empty id\n";
		var_dump($item);
		echo "\n\n";
		continue;
	}
	$find_item = getSqliteItem($sqlite_db, $tbl_name, $id);
	if ( null == $find_item )
	{
		echo "cannot find id:" . $id . "\n";
		continue;
	}
	if ( $check_all )
	{
		foreach ($item as $field => $value) {
		 	if ( 'id' == $field || 'created' == $field || 'updated' == $field )
		 		continue;
		 	if ( !array_key_exists($field, $find_item))
		 	{
		 		if (!array_key_exists($field, $notMatchFieldArray))
		 		{
		 			echo "No field:" . $field . "\n";
		 			$notMatchFieldArray[$field] = 0;
		 		}
		 		continue;
		 	}
		 	if ( $value != $find_item[$field])
		 	{
		 		echo "NotEqual id:" . $id . ' field:' . $field . '  ' . $value . '  -> ' . $find_item[$field] . "\n";
		 	}
		 }
	}
	else
	{
		if ( $item['deleted'] != $find_item['deleted'])
		{
			echo "deleted value diff! id:" . $id . "\n";
			continue;
		}
	}
}


