<?php
namespace Drupal\twig_extension_helper\model;

use Drupal\twig_extension_helper\util\ModelUtil;

class Announcement {

  var $announcement_name = NULL,
    $body = NULL,
    $date = NULL;

  function __construct($node_obj) {
//    if(!is_null($node_obj->field_announcement_name[0])) {
//      $this->announcement_name = $node_obj->field_announcement_name[0]->value;
      $this->announcement_name = ModelUtil::getValue($node_obj, "field_announcement_name");
//    }

//    if(!is_null($node_obj->field_body[0])) {
      $this->body = ModelUtil::getValue($node_obj, "field_body");
//    }

//    if(!is_null($node_obj->field_date[0])) {
      $this->date = date_create_from_format("Y-m-d\TH:i:s", ModelUtil::getTrimmedValue($node_obj, "field_date"));
//    }
  }

  /**
   * @return string
   */
  public function getAnnouncementName() {
    return $this->announcement_name;
  }

  /**
   * @return string
   */
  public function getBody() {
    return $this->body;
  }

  /**
   * @return datetime
   */
  public function getRawDate() {
    return $this->date;
  }

  /**
   * @return string
   */
  public function getDate($format = 'Y-m-d') {
    return $this->date->format($format);
  }

}
