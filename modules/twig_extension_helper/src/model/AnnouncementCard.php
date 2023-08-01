<?php
namespace Drupal\twig_extension_helper\model;

use Drupal\twig_extension_helper\util\NodeUtil;

class AnnouncementCard extends Card {

  var $announcement_name = NULL,
    $body = NULL,
    $date = NULL,
    $announcement_id;

  function __construct($node_obj) {
    parent::__construct($node_obj);

    if(!is_null($node_obj->field_announcement_reference)) {
      $announcement_node = NodeUtil::nodeLoad($node_obj->field_announcement_reference[0]->target_id);
      $announcement = new Announcement($announcement_node);

      $this->announcement_name = $announcement->getAnnouncementName();
      $this->body = $announcement->getBody();
      $this->date = $announcement->getRawDate();

      $this->announcement_id = $announcement_node->nid[0]->value;
    }
  }

  /**
   * @return null|string
   */
  public function getAnnouncementName() {
    return $this->announcement_name;
  }

  /**
   * @return null|string
   */
  public function getBody() {
    return $this->body;
  }

  /**
   * @return string
   */
  public function getDate($format = 'Y-m-d') {
    return $this->date->format($format);
  }

  /**
   * @return mixed
   */
  public function getAnnouncementId() {
    return $this->announcement_id;
  }


}
