<?php
/**
 * Created by IntelliJ IDEA.
 * User: sdave
 * Date: 2/14/2018
 * Time: 11:23 AM
 */

namespace Drupal\twig_extension_helper\model;


use Drupal\twig_extension_helper\util\ModelUtil;

class Sidebar {
  var $name,
      $color,
      $body;

  function __construct($sidebar_obj) {
    if(!ModelUtil::isFirstNull($sidebar_obj->field_content_name)) {
      $this->name = $sidebar_obj->field_content_name[0]->value;
    }

    if(!ModelUtil::isFirstNull($sidebar_obj->field_content_body)) {
      $this->body = $sidebar_obj->field_content_body[0]->value;
    }

    if(!ModelUtil::isFirstNull($sidebar_obj->field_sidebar_color)) {
      $this->color = $sidebar_obj->field_sidebar_color[0]->color;
    }
  }

  /**
   * @return mixed
   */
  public function getName() {
    return $this->name;
  }

  /**
   * @return mixed
   */
  public function getColor() {
    return $this->color;
  }

  /**
   * @return mixed
   */
  public function getBody() {
    return $this->body;
  }



}
