<?php
/**
 * Created by IntelliJ IDEA.
 * User: sdave
 * Date: 1/12/2018
 * Time: 5:15 PM
 */

namespace Drupal\twig_extension_helper\model;


use Drupal\twig_extension_helper\util\ModelUtil;
use Drupal\twig_extension_helper\util\TaxonomyUtil;

class Vocabulary {

  var $value = [],
      $entity_manager = NULL;

  public function __construct($vocabulary_name) {
    $this->setEntityManager();
    $raw_terms = $this->vocabularyTreeLoad($vocabulary_name);
    $temp_tree = [];
    foreach($raw_terms as $tree_obj) {
      $this->buildValue($temp_tree, $tree_obj, $vocabulary_name);
    }

    $this->value = $temp_tree;
  }

  protected function setEntityManager() {
    $this->entity_manager = \Drupal::entityTypeManager();
  }

  protected function buildValue(&$current_value, $object, $vocabulary_name) {
    $current_tid = $object->tid;
    $current_depth = $object->depth;
    $current_name = $object->name;

    if ($current_depth != 0) {
      return;
    }

    $safe_name = ModelUtil::stringToCleanKey($current_name);

    $current_value[$safe_name] = $object;
    $current_value[$safe_name]->children = [];

    $object_children = &$current_value[$safe_name]->children;

    $children = $this->vocabularyChildrenLoad($current_tid);
    if (!$children) {
      return;
    }

    $child_tree_objects = $this->vocabularyTreeLoad($vocabulary_name, $current_tid);

    foreach ($children as $child) {
      foreach ($child_tree_objects as $child_tree_object) {
        if ($child_tree_object->tid == $child->id()) {
          $this->buildValue($object_children, $child_tree_object, $vocabulary_name);
        }
      }
    }
  }

  /**
   * @return array
   */
  public function getValue() {
    return $this->value;
  }

  protected function vocabularyTreeLoad($vocabulary_name, $tid=NULL) {
    return TaxonomyUtil::vocabularyTreeLoad($this->entity_manager, $vocabulary_name, $tid);
  }

  protected function vocabularyChildrenLoad($vocabulary_children_name) {
    return TaxonomyUtil::vocabularyChildrenLoad($this->entity_manager, $vocabulary_children_name);
  }

  protected function vocabularyFieldLoad($tid, $field_name) {
    return TaxonomyUtil::vocabularyFieldLoad($this->entity_manager, $tid, $field_name);
  }
}
