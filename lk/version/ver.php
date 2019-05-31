<?php


$host = 'gdsa-sql.paadoo.net';
$database = 'main';
$username = 'main-ro-01';
$password = 'EdvrWh0fwHDSvCPR';

$argC = count($argv);
$help = false;
if ( $argC < 2 || strpos($argv[1], 'help') !== false )
{
  $help = true;
} 
else if ( $argv[1] == 'v' )
{
  $v = null;
  if ($argC > 2) 
  {
    $v = $argv[2];
  }
  if ( null == $v || empty($v) ) 
  {
    $help = true;
  }
  else 
  {
    $sql = 'select module_id,pkg,git_revision from sys_module_release where id in (select item_id from sys_release_item where release_id=(select id from sys_release where version=\'' . $v . '\'));';
  }
}
else if ( $argv[1] == 'g' )
{
  $g = null;
  if ($argC > 2) 
  {
    $g = $argv[2];
  }
  if ( null == $v || empty($v) ) 
  {
    $help = true;
  }  
  else
  {
    $sql = 'select m.module_id,m.pkg,m.git_revision,r.version,r.relnote,r.updated from sys_module_release ad m left join sys_release_item as i on m.id=i.item_id left join sys_release as r on i.release_id=r.id where m.git_revision like \'' . $g . '\';';
  }
}
else if ( $argv[1] == 'l' )
{
  $n = 5;
  if ($argC > 2)
  {
    $n = (int)$argv[2];
    if ($n < 1 )
      $n = 5;
  }
  $sql = "select version,status,relnote,updated,created from sys_release order by id desc limit " . $n . ";";
}
else
{
  $help = true;
}

if ($help)
{
  echo "l: list versions\nv: version module information\ng: match git version\n";
}
else
{
  $mysqli = new mysqli($host, $username, $password, $database);
  if ($mysqli->connect_errno) {
    die("Failed to connect to MySQL: (" . $mysqli->connect_errno . ") " . $mysqli->connect_error);
  }
  $result = $mysqli->query($sql);
  if (!$result) {
    $mysqli->close();
    die('Invalid query: ' . mysqli_error($mysqli) . "\n");
  }
  $first = true;
  $header = null;
  $content = "\n";
  while ($row = $result->fetch_array(MYSQLI_BOTH)) {
    foreach ($row as $key => $value) {
      if ( preg_match('/^\\d+$/', $key) > 0 )
        continue;
      if ($first)
      {
        if ( null == $header )
          $header = $key;
        else
          $header = $header . '   ' . $key;
      }
      $content = $content . '   ' . $value;
    }
    if ($first)
    {
      $first = false;
    }
    $content = $content . "\n";
  }  
  $mysqli->close();
  echo $header . $content;
}