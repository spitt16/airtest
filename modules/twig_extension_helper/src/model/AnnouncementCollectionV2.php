<?php
namespace Drupal\twig_extension_helper\model;

use Drupal\twig_extension_helper\util\ParagraphUtil;

/**
 * Class AnnouncementCollectionV2
 * @package Drupal\twig_extension_helper\model
 *
 * Contains multiple announcements.
 *
 * Constructed in TwigExtensionHelper.
 */

class AnnouncementCollectionV2 {
  var $node_id = NULL;
  var $announcements = [];

  function __construct($node_obj) {
    $this->node_id = $node_obj->nid[0]->value;
    $announcement_paragraph_objs = ParagraphUtil::getParagraphs($node_obj, "field_ann_announcement_paragraph");

    foreach($announcement_paragraph_objs as $announcement_paragraph_obj) {
      array_push($this->announcements, new AnnouncementV2Paragraph($announcement_paragraph_obj));
    }

    usort($this->announcements, function ($a, $b) {
      $dateA = $a->date;
      $dateB = $b->date;
      if ($dateA < $dateB) {
        return 1;
      }
      if ($dateA > $dateB) {
        return -1;
      }
      return 0;
    });
  }

  /**
   * @return null
   */
  public function getNodeId() {
    return $this->node_id;
  }

  /**
   * @return array
   */
  public function getAnnouncements() {
    return array_filter($this->announcements, function($obj){
      return !$obj->isArchived();
    });
  }

  /**
   * @return array
   */
  public function getArchivedAnnouncements() {
    return array_filter($this->announcements, function($obj){
      return $obj->isArchived();
    });
  }

  /**
   * @return int
   */
  public function getAllAnnouncementCount() {
    return count($this->announcements);
  }
}
