
<?php



$result = db_query("SELECT fm.*
FROM {file_managed} AS fm
LEFT OUTER JOIN {file_usage} AS fu ON ( fm.fid = fu.fid )
LEFT OUTER JOIN {node} AS n ON ( fu.id = n.nid )
WHERE (fu.type = 'node' OR fu.type IS NULL) AND n.nid IS NULL
ORDER BY `fm`.`fid`  DESC");

//Delete file & database entry
foreach ($result as $delta => $record) {
     echo $record->fid;
	 echo "<br>";
}




// Get curl version array
$version = curl_version();

echo "cURL Version: ";
echo $version["version"];
echo "<br>";

?>


<?php
	phpinfo();
?>