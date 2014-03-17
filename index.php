<?php

$id = uniqid();
move_uploaded_file($_FILES['data']['tmp_name'],'/home/ben/Web/json'.$id.'.gz');
echo '{"via":"55","sleep":30}';
?>

