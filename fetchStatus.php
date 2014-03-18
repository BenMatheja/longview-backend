<?php
/**
 * Created by PhpStorm.
 * User: ben
 * Date: 3/18/14
 * Time: 6:22 PM
 */
$connection = new MongoClient( "mongodb://suchtundordnung.de");
if($connection) echo "connected to mongodb";
$db = $connection->rasp_status->longview;
echo $db->count();