<?php
date_default_timezone_set('Europe/Berlin');
echo 'welcome to api gen v1';
//echo generateRandomString();
echo '<pre>';
$string = file_get_contents('http://api.benmatheja.de/fetchStatus.php');

$json_array = json_decode($string,true);
echo '<pre>';
$longterm = $json_array[0]['LONGTERM'];
var_dump($instant = $json_array[0]['INSTANT']);

echo $longterm['Load'];
echo '<br>';
echo $longterm['CPU.cpu0.system'];
echo '<br>';
echo $longterm['CPU.cpu0.user'];
echo '<br>';
echo $longterm['CPU.cpu0.wait'];
echo '<br>';
echo $longterm['SysInfo.os.dist'];
echo '<br>';
echo $instant['SysInfo.cpu.type'];
echo '<br>';
echo $instant['SysInfo.hostname'];
echo '<br>';
echo $instant['SysInfo.kernel'];

echo '<br>';
echo gmdate("H:i:s", $instant['Uptime']);
echo '</pre>';
echo '-------';