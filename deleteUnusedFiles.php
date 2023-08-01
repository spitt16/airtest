<?php
// Delete Unused Files cw 2021-04-26
// from: https://www.drupal.org/node/733258#comment-5582764
//

use Drupal\Core\Database\Connection;

$db = \Drupal::database("airnowgov"); 
$result = $db->select('node', 'n'); 
$query->fields('n'); 
$query->condition('type', "page", "="); 
$result = $query->execute()->fetchAll(); 
print_r($result);



$result = db_query("SELECT fm.*
FROM {file_managed} AS fm
LEFT OUTER JOIN {file_usage} AS fu ON ( fm.fid = fu.fid )
LEFT OUTER JOIN {node} AS n ON ( fu.id = n.nid )
WHERE (fu.type = 'node' OR fu.type IS NULL) AND n.nid IS NULL
ORDER BY `fm`.`fid`  DESC");

//Delete file & database entry
foreach ($result as $delta => $record) {
    //file_delete($record->fid);
	echo "$record->fid";
	echo "<br>";
	}

?>
