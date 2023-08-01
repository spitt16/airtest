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

class MarqueeImagesVocabulary extends Vocabulary {
  public function __construct($vocabulary_name) {
    parent::__construct($vocabulary_name);
  }

  protected function buildValue(&$current_value, $object, $vocabulary_name) {
    $current_tid = $object->tid;

    $current_parameter_key = $this->vocabularyFieldLoad($current_tid, "field_sample_type")->getValue()[0]['value'];
    $safe_name = ModelUtil::stringToCleanKey($current_parameter_key);

    $temp_object = [];
    $marquee_img_paragraphs = ParagraphUtil::getParagraphs(TaxonomyUtil::termLoad($this->entity_manager, $current_tid), "field_marquee_images");

    foreach($marquee_img_paragraphs as $marquee_img_paragraph) {
      $img = new Image($marquee_img_paragraph->field_marquee_image[0]->target_id, NULL, "marquee image");
      array_push($temp_object, $img->getImageUrl());
//      $temp_object[$img->getCategoryKey()] = $parameter_msg->getMessage();
    }

    $current_value[$safe_name] = $temp_object;
  }
}
