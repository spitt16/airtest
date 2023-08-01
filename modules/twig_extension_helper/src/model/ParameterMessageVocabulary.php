<?php
/**
 * Created by IntelliJ IDEA.
 * User: sdave
 * Date: 1/16/2018
 * Time: 10:19 AM
 */

namespace Drupal\twig_extension_helper\model;


use Drupal\twig_extension_helper\util\ModelUtil;
use Drupal\twig_extension_helper\util\ParagraphUtil;
use Drupal\twig_extension_helper\util\TaxonomyUtil;

class ParameterMessageVocabulary extends Vocabulary {
  public function __construct($vocabulary_name) {
    parent::__construct($vocabulary_name);
  }

  protected function buildValue(&$current_value, $object, $vocabulary_name) {
    $current_tid = $object->tid;

    $current_parameter_key = $this->vocabularyFieldLoad($current_tid, "field_reporting_area_parameter")->getValue()[0]['value'];
    $safe_name = ModelUtil::stringToCleanKey($current_parameter_key);

    $temp_object = [];
    $parameter_msg_paragraphs = ParagraphUtil::getParagraphs(TaxonomyUtil::termLoad($this->entity_manager, $current_tid), "field_parameter_messages");

    foreach($parameter_msg_paragraphs as $parameter_msg_paragraph) {
      $parameter_msg = new ParameterMessage($parameter_msg_paragraph);
      $temp_object[$parameter_msg->getCategoryKey()] = array(
        "current" => $parameter_msg->getMessage(),
        "forecast" => $parameter_msg->getForecastMessage()
      );
    }

    $current_value[$safe_name] = $temp_object;
  }
}
