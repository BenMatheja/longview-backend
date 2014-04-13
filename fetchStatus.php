<?php
/**
 * Created by PhpStorm.
 * User: ben
 * Date: 3/18/14
 * Time: 6:22 PM
 */
$connection = new MongoClient( "mongodb://localhost");
//if($connection) echo "connected to mongodb";
$db = $connection->selectDB('rasp_status');
$cursor = $db->longview->find()->sort(array('timestamp' => -1))->limit(1);
$counter = 0;
foreach ($cursor as $doc){
	//echo '<pre>';
	echo json_encode($doc['payload']);
	$counter++;
	//echo '</pre>';
}

//echo 'found total '.$counter.' documents';

