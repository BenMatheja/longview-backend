<?php
/**
 * Created by PhpStorm.
 * User: ben
 * Date: 3/18/14
 * Time: 6:22 PM
 */
$connection = new MongoClient( "mongodb://suchtundordnung.de");
if($connection) echo "connected to mongodb";
echo '<br>';
$db = $connection->selectDB('rasp_status');
$list = $db->listCollections();
foreach ($list as $collection){
    echo "found $collection";
    echo '<br>';
}