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
  mysql_query('delete from ' . $file . ';', $connection);
}