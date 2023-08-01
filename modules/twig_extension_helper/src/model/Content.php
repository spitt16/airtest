<?php
/**
 * Created by IntelliJ IDEA.
 * User: sdave
 * Date: 2/14/2018
 * Time: 11:19 AM
 */

namespace Drupal\twig_extension_helper\model;


use Drupal\twig_extension_helper\util\ModelUtil;
use Drupal\twig_extension_helper\util\ParagraphUtil;

class Content {
  var $name,
      $body,
      $anchor_id,
      $has_back_to_top,
      $sidebar = [];

  function __construct($content_obj) {
//    if(!ModelUtil::isFirstNull($content_obj->field_content_name)) {
    $this->name = ModelUtil::getValue($content_obj, "field_content_name");
//    }

//    if(!ModelUtil::isFirstNull($content_obj->field_content_body)) {
    $this->body = ModelUtil::getValue($content_obj, "field_content_body");
//    }

//    if(!ModelUtil::isFirstNull($content_obj->field_anchor_id)) {
    $this->anchor_id = ModelUtil::getCleanKeyValue($content_obj, "field_anchor_id");
//      $this->anchor_id = ModelUtil::stringToCleanKey($content_obj->field_anchor_id[0]->value);
//    }

//    $this->has_back_to_top = boolval($content_obj->field_has_back_to_top[0]->value);
    $this->has_back_to_top = ModelUtil::getBooleanValue($content_obj, "field_has_back_to_top");

    $sidebar_objs = ParagraphUtil::getParagraphs($content_obj, "field_content_sidebar");
    foreach($sidebar_objs as $sidebar_obj) {
      array_push($this->sidebar, new Sidebar($sidebar_obj));
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
  public function getBody() {
    return $this->body;
  }

  /**
   * @return mixed
   */
  public function getAnchorId() {
    return $this->anchor_id;
  }

  /**
   * @return bool
   */
  public function isHasBackToTop() {
    return $this->has_back_to_top;
  }

  /**
   * @return \Drupal\twig_extension_helper\model\Sidebar
   */
  public function getSidebar() {
    return $this->sidebar;
  }



}
