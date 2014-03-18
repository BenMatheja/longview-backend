<?php
//takes gz input file and creates json array
function uncompressToJson($srcName)
{
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
//move & store uploaded file
$id = uniqid();
move_uploaded_file($_FILES['data']['tmp_name'], './json_out/json' . $id . '.gz');
$json_array = uncompressToJson('./json_out/json' . $id . '.gz');

$connection = new MongoClient( "mongodb://suchtundordnung.de");
$db = $connection->rasp_status;
$collection = $db->longview;
$collection->insert($json_array);



//debug out for longview client
echo '{"via":"55","sleep":30, "chatty":"yes"}';
?>

