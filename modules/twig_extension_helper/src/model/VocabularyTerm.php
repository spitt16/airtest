<?php
/**
 * Created by IntelliJ IDEA.
 * User: sdave
 * Date: 1/12/2018
 * Time: 5:18 PM
 */

namespace Drupal\twig_extension_helper\model;


use Drupal\twig_extension_helper\util\TaxonomyUtil;

class VocabularyTerm {

  var $tid,
    $children = [],
    $entity_manager = NULL;

  public function __construct($object) {
    $this->setEntityManager();
    $this->tid = $object->tid;
  }

  protected function setEntityManager() {
    $this->entity_manager = \Drupal::entityTypeManager();
  }

  /**
   * @return mixed
   */
  public function getTid() {
    return $this->tid;
  }

  /**
   * @return array
   */
  public function getChildren() {
    return $this->children;
  }

  public function addChildren($child) {
    array_push($this->children, $child);
  }

  protected function vocabularyChildrenLoad($vocabulary_children_name) {
    return TaxonomyUtil::vocabularyChildrenLoad($this->entity_manager, $vocabulary_children_name);
  }

  protected function vocabularyFieldLoad($tid, $field_name) {
    return TaxonomyUtil::vocabularyFieldLoad($this->entity_manager, $tid, $field_name);
  }

}
