<?php

$shop_dir = './fix/shop';
$host = 'localhost';
$database = 'test';
$username = 'root';
$password = 'root';

$connection = mysql_connect($host, $username, $password);
if (!$connection) {
    die("could not connect to the database.\n" . mysql_error());
}
$selectedDb = mysql_select_db($database);
if (!$selectedDb) {
    die("could not to the database\n" . mysql_error());
}


foreach(scandir($shop_dir) as $file)
{
  if( $file == '.' || $file == '..' )
    continue; 
  if(!is_dir($shop_dir.'/'.$file))
    continue;
  $fp = $shop_dir. '/' .$file . '/ver_0.sql';
  $f = fopen($fp, 'r');
  $content = fread($f, 0x7fffffff);
  mysql_query($content, $connection);
  fclose($f);
  $i = 1;
  while(true)
  {
  	$fp = $shop_dir. '/' .$file . '/upgrade_' . $i . '.sql';
  	if (!file_exists($fp))
  	  break;
  	$f = fopen($fp, 'r');
    $content = fread($f, 0x7fffffff);
    mysql_query($content, $connection);
    fclose($f);
    $i ++;
  }
}