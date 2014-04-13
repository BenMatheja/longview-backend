<?php
date_default_timezone_set("Europe/Berlin");

//takes gz input file and creates json array
function uncompressToJson($srcName){
    $sfp = gzopen($srcName, "rb");
    $json_output = '';
    $json_array = null;

    while ($string = gzread($sfp, 4096)) {
        //fwrite($fp, $string, strlen($string));
        $json_output .= $string;
    }
    gzclose($sfp);
   return $json_array = json_decode($json_output);
}

//Validate Posting Client
function validateLongviewClient(){
	$uAgent = $_SERVER['HTTP_USER_AGENT'];
	$clientKey = explode('client: ',$uAgent);
	if(strpos($uAgent,'Linode Longview')!==false){
		return true;
	}
	else return false;
}
function pushToMongo($json_array){
	$connection = new MongoClient( "mongodb://localhost");
	$insert = 'longview';
	
	//db rasp status
	$db = $connection->rasp_status;
	$collection = $db->$insert;
	$collection->insert($json_array);
}

if(validateLongviewClient()){
$json_array = uncompressToJson($_FILES['data']['tmp_name']);
pushToMongo($json_array);
//debug out for longview client
echo '{"via":"55","sleep":120, "chatty":"yes"}';
}
else {
	echo 'access not granted';
}

?>

