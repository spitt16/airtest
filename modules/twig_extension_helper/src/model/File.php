<?php
namespace Drupal\twig_extension_helper\model;

use Drupal\twig_extension_helper\util\ModelUtil;

class File {
  var $file_url = NULL;

  function __construct($file_obj) {

    $entity = $file_obj->entity;
    $this->file_url = file_create_url($entity->getFileUri());

  }

  /**
   * @return null
   */
  public function getFileUrl() {
    return $this->file_url;
  }


}
