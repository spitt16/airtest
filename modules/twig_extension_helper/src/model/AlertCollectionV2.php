<?php
namespace Drupal\twig_extension_helper\model;

use Drupal\twig_extension_helper\util\ParagraphUtil;

/**
 * Class AlertCollectionV2
 * @package Drupal\twig_extension_helper\model
 *
 * Contains multiple alerts.
 *
 * Constructed in TwigExtensionHelper.
 */

class AlertCollectionV2 {
  var $node_id = NULL;
  var $alerts = [];

  function __construct($node_obj) {
    $this->node_id = $node_obj->nid[0]->value;
    $alert_paragraph_objs = ParagraphUtil::getParagraphs($node_obj, "field_alert_alert_paragraph");

    foreach($alert_paragraph_objs as $alert_paragraph_obj) {
      array_push($this->alerts, new AlertV2Paragraph($alert_paragraph_obj));
    }

    usort($this->alerts, function ($a, $b) {
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
  public function getAlerts() {
    return array_filter($this->alerts, function($obj){
      return !$obj->isArchived();
    });
  }

  /**
   * @return array
   */
  public function getArchivedAlerts() {
    return array_filter($this->alerts, function($obj){
      return $obj->isArchived();
    });
  }

  /**
   * @return int
   */
  public function getAllAlertCount() {
    return count($this->alerts);
  }
}
