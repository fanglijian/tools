<?php


$host = array('localhost');
$database = array('likeit');
$username = array('root');
$password = array('root');

#$host = array('unit-sql-01.paadoo.net', 'unit-sql-02.paadoo.net', 'unit-sql-03.paadoo.net', 'unit-sql-04.paadoo.net', 'unit-sql-05.paadoo.net');
#$database = array('shop', 'shop', 'shop', 'shop', 'shop');
#$username = array('shop-01-ro-01', 'shop-02-ro-01', 'shop-03-ro-01', 'shop-04-ro-01', 'shop-05-ro-01');
#$password = array('KaIL0BkKGuPfLTiC', 'Me1ftRCV23LVe7Vo', 'QBSH5KOFsdsC6Cc8', 'v2OwExSyuqGBZ1GJ', 'Js6ZRlytdSdSV7N3');

$shop = 104354;
$f = fopen('./table_of_shop_' . $shop . '.txt', 'w');  

$sz = count($host);
for ( $i = 0; $i < $sz; $i ++ )
{
  $mysqli = new mysqli($host[$i], $username[$i], $password[$i], $database[$i]);
  if ($mysqli->connect_errno) {
    die("Failed to connect to MySQL: (" . $mysqli->connect_errno . ") " . $mysqli->connect_error);
  }

  $result = $mysqli->query('show tables;');
  if (!$result) {
    $mysqli->close();
    die('Invalid query: ' . mysql_error() . "\n");
  }
  $tblArray = array();
  while ($row = $result->fetch_array(MYSQLI_BOTH)) {
    array_push($tblArray, $row[0]);
  }  
  foreach ($tblArray as $tbl) {
    $result = $mysqli->query('select count(1) as c from `' . $tbl . '` where shop_id=' . $shop . ';');
    if (!$result) {
      while ($row = $result->fetch_array(MYSQLI_BOTH)) {
        $c = (int)$row['c'];
        if ( $c > 0 )
          fwrite($f, $tbl . ':' .  $c . "\n" );
    }
  }
  $mysqli->close();
}
fclose($f);