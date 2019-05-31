<?php

function loginRestique($username, $code)
{
	$session = null;
	$uri = 'https://restique.paadoo.net:32779/login?name=' . $username . '&code=' . $code;
    $curl = curl_init();
    curl_setopt($curl, CURLOPT_URL, $uri);
    curl_setopt($curl, CURLOPT_RETURNTRANSFER, 1);
    curl_setopt($curl, CURLOPT_HEADER, 1);
	curl_setopt($curl, CURLOPT_SSL_VERIFYPEER, false);
	curl_setopt($curl, CURLOPT_SSL_VERIFYHOST, 0);
    $ret = curl_exec($curl);
    curl_close($curl);
	if (false == $ret) {
		var_dump(curl_error($curl));
		die("\n");
	}
	preg_match_all('/^Set-Cookie:\s*([^;]*)/mi', $ret, $matches);
	$cookies = array();
	foreach($matches[1] as $item) 
	{
		parse_str($item, $cookie);
		$cookies = array_merge($cookies, $cookie);
	}
	$session = key($cookies) . '=' . current($cookies);
	$f = fopen('./cookies', 'w');
	fwrite($f, $session);
	fclose($f);
	return $session;
}

function getSavedSession()
{
	$f = fopen('./cookies', 'r');
	$session = fread($f, filesize('./cookies'));
	fclose($f);
	return $session;
}

function queryRestique($db_name, $query, $session)
{
	$uri = 'https://restique.paadoo.net:32779/query?use=' . $db_name . '&sql=' . urlencode($query);
    $curl = curl_init();
    curl_setopt($curl, CURLOPT_URL, $uri);
    curl_setopt($curl, CURLOPT_RETURNTRANSFER, 1);
    curl_setopt($curl, CURLOPT_HEADER, 0);
	curl_setopt($curl, CURLOPT_SSL_VERIFYPEER, false);
	curl_setopt($curl, CURLOPT_SSL_VERIFYHOST, 0);
	curl_setopt($curl, CURLOPT_HTTPHEADER, array("Cookie: " . $session));
    $ret = curl_exec($curl);
    if (false == $ret) {
		var_dump(curl_error($curl));
		die("\n");
	}	
	return json_decode($ret);
}

function getDataOfTable($db_name, $shop_id, $tbl_name, $session)
{
	$sql = 'select count(1) from ' . $tbl_name . ' where shop_id=' . $shop_id . ';';
	$ret = queryRestique($db_name, $sql, $session);
	if ( null == $ret )
	{
		die("query count failed\n");
	}
	$c = (int)current(current($ret));
	$resArray = array();
	$oft = 0;
	while ($oft < $c ) {
		$sql = 'select * from ' . $tbl_name . ' where shop_id=' . $shop_id . ' order by id limit ' . $oft . ',1000;';
		$ret = queryRestique($db_name, $sql, $session);
		if ( null == $ret ) 
		{
			die("query data of table failed\n");
		}
		$oft += count($ret);
		foreach ($ret as $value) {
			$r = processResArray($value);
			array_push($resArray, $r);
		}
	}
	#var_dump($resArray);
	return processResArray($resArray);
}

function getSqliteItem($sqlite_db, $tbl_name, $id)
{
	$statement = $sqlite_db->prepare('SELECT * FROM ' . $tbl_name . ' WHERE id=:id;');
	$statement->bindValue(':id', $id);
	$result = $statement->execute();
	if ( null == $result )
		return null;
	return $result->fetchArray();
}

function processResArray($inArray)
{
	if ( null == $inArray )
		return null;
	$res = array();
	foreach ($inArray as $k1=> $v1) {
		$res[$k1] = $v1;
	}
	return $res;
}