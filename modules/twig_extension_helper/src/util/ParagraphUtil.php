<?php
namespace Drupal\twig_extension_helper\util;
use Drupal\Core\Entity\FieldableEntityInterface;
use Drupal\paragraphs\Entity\Paragraph;

class ParagraphUtil {

  public static function paragraphLoad($id) {
    return Paragraph::load($id);
  }

  public static function getParagraphs($node_obj, $field_name) {
    if(!$node_obj->hasField($field_name)) {
      return [];
    }
    $paragraph_obj = $node_obj->get($field_name);
    $paragraph_arr = [];

    for($field_i = 0; $field_i < count($paragraph_obj); $field_i++){
      $paragraph_target_value = $paragraph_obj[$field_i];
      $target_id = $paragraph_target_value->get('target_id')->getCastedValue();
      array_push($paragraph_arr, ParagraphUtil::paragraphLoad($target_id));
    }
    return $paragraph_arr;
  }

  public static function getParagraph($node_obj, $field_name) {
    if(!$node_obj->hasField($field_name)) {
      return NULL;
    }
    $paragraph_obj = $node_obj->get($field_name);

    if(count($paragraph_obj) > 0) {
      $paragraph_target_value = $paragraph_obj[0];
      $target_id = $paragraph_target_value->get('target_id')->getCastedValue();
      return ParagraphUtil::paragraphLoad($target_id);
    }

    return NULL;
  }
}
