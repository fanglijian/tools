<?php

require 'base.php';

$db_shop = 'unit-sql-04';
$username = null;
$code = null;
$session = null;

$orderId = null;

$i = 0;
$s1 = null;
$s2 = null;
if ( $argc > 1)
{	
	for ( $i = 1; $i < $argc; )
	{
		$s1 = $argv[$i];
		$s2 = '';
		if ($i < $argc - 1)
			$s2 = $argv[$i + 1];
		if ( null == $s1)
		{
			$i ++;
			continue;
		}
		if ( '-c' == $s1 )
		{
			$code = $s2;
			$i += 2;
			continue;
		}
		else if ( '-u' == $s1 )
		{
			$username = $s2;
			$i += 2;
			continue;	
		}
		else if ( strlen($s1) == 16 )
			$orderId = $s1;
		$i += 1;
	}
}

if ( $orderId == null || empty($orderId))
{
	die("no order id");
}

if ( null != $username && null != $code )
{
	$session = loginRestique($username, $code);
}
if ( null == $session )
	$session = getSavedSession();
if ( null == $session )
	die("No session\n");

function getIds($tbl, $wh, $sel, $db, $ss)
{
	$selArray = false;
	if ($sel == null || empty($sel) || !is_array($sel) )
		$sql = 'select id from ' . $tbl . ' where ';
	else
	{
		$selArray = true;
		$sql = 'select ' . join(',', $sel) . ' from ' . $tbl . ' where ';
	}
	foreach ($wh as $key => $value) {
		$sql .= $key;
		if (is_array($value))
		{
			$sql .= ' in(';
			$i = 0;
			foreach ($value as $v) {
				if ( 0 == $i)
					$sql .= '\'' . $v . '\'';
				else
					$sql .= ',\'' . $v . '\'';
				$i ++;
			}
			$sql .= ')';
		}
		else
		{
			$sql .= '=\'' . $value . '\'';
		}
		$sql .= ' and deleted=0;';
	}
	#echo $sql . "\n";
	$ids = queryRestique($db, $sql, $ss);
	if ( null == $ids)
		return null;
	$result = array();
	if ($selArray)
	{
		foreach ($sel as $v) {
			$result[$v] = array();
		}
	}
	foreach ($ids as $item) {
		$item2 = processResArray($item);
		if ($selArray)
		{
			foreach ($sel as $v) {
				array_push($result[$v], $item2[$v]);
			}
		}
		else
		{
			array_push($result, $item2['id']);
		}
	}
	return $result;
} 

$oneOrderIds = null;
$itemIds = null;
$orderPaymentIds = null;
$paymentIds = null;
$staffPerforIds = null;
$orderDeliveryIds = null;

$objIds = array();
array_push($objIds, $orderId);

$oneOrderIds = getIds('one_order', array( 'order_id' => $orderId ) , null, $db_shop, $session);
if ( null != $oneOrderIds )
{
	foreach ($oneOrderIds as $v) {
		array_push($objIds, $v);
	}
	$itemIds = getIds('order_item', array( 'one_order_id' => $oneOrderIds ), null, $db_shop, $session);
	$orderPayment = getIds('order_payment', array( 'one_order_id' => $oneOrderIds ), array('id', 'payment_id'), $db_shop, $session);
	if ( null != $itemIds )
	{
		foreach ($itemIds as $v) {
			array_push($objIds, $v);
		}
	}
	if ( null != $orderPayment )
	{
		$orderPaymentIds = $orderPayment['id'];
		$paymentIds = $orderPayment['payment_id'];
		if ( null != $paymentIds )
		{
			foreach ($paymentIds as $v) {
				array_push($objIds, $v);
			}
		}
	}
}
$staffPerforIds = getIds('staff_performance', array( 'object_id' => $objIds ) , null, $db_shop, $session);
$orderDeliveryIds = getIds('order_delivery', array( 'orders_id' => $orderId ) , null, $db_shop, $session);

$f = fopen("./delete_order.txt", "w");
fwrite($f, "orders." . $orderId . "\n    deleted=1\n");
if (null != $oneOrderIds)
{
	foreach ($oneOrderIds as $v) {
		fwrite($f, "one_order." . $v . "\n    deleted=1\n");
	}
}
if (null != $itemIds)
{
	foreach ($itemIds as $v) {
		fwrite($f, "order_item." . $v . "\n    deleted=1\n");
	}
}
if (null != $orderPaymentIds)
{
	foreach ($orderPaymentIds as $v) {
		fwrite($f, "order_payment." . $v . "\n    deleted=1\n");
	}
}
if (null != $paymentIds)
{
	foreach ($paymentIds as $v) {
		fwrite($f, "payment." . $v . "\n    deleted=1\n");
	}
}
if (null != $staffPerforIds)
{
	foreach ($staffPerforIds as $v) {
		fwrite($f, "staff_performance." . $v . "\n    deleted=1\n");
	}
}
if (null != $orderDeliveryIds)
{
	foreach ($orderDeliveryIds as $v) {
		fwrite($f, "order_delivery." . $v . "\n    deleted=1\n");
	}
}
fclose($f);
