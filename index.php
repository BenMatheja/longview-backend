<?php

$id = uniqid();
move_uploaded_file($_FILES['data']['tmp_name'],'/home/ben/Web/longview-backend/json_out/json'.$id.'.gz');
echo '{"via":"55","sleep":30}';
?>

