<?php
/**
 * Created by IntelliJ IDEA.
 * User: sdave
 * Date: 3/2/2018
 * Time: 2:26 PM
 */

namespace Drupal\twig_extension_helper\model;


class StatusMessagesVocabulary extends Vocabulary {
  public function __construct($vocabulary_name) {
    parent::__construct($vocabulary_name);
  }

  protected function buildValue(&$current_value, $object, $vocabulary_name) {
    array_push($current_value, new StatusMessageTerm($object));
  }

  public function getStatusMessage1() {
    $current_value = $this->getValue();
    if(count($current_value) > 0 ) {
      return $current_value[0];
    }
  }

  public function getStatusMessages() {
	$current_value = $this->getValue();
    if(count($current_value) > 0 ) {
      return $current_value;
   	  }
    }
  

}
