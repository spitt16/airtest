<?php
namespace Drupal\twig_extension_helper\model;

use DateTime;
use Drupal\twig_extension_helper\util\ModelUtil;

/**
 * Class Alertv2
 * @package Drupal\twig_extension_helper\model
 *
 * Information defining an alert.
 *
 * Not directly constructed via TwigExtensionHelper.  Instead, it is extended by Alertv2Paragraph, which is
 * in turn constructed by AlertCollectionV1.  AlertCollectionV1 is constructed in TwigExtensionHelper.
 */

class AlertV2 {
  var $title = NULL;
  var $date = NULL;
  var $main_text = NULL;
  var $additional_text = NULL;

  function __construct($node_obj) {
      $this->title = ModelUtil::getValue($node_obj, "field_alert_title");
      $this->date = date_create_from_format("Y-m-d", ModelUtil::getTrimmedValue($node_obj, "field_alert_date"));
      $this->main_text = ModelUtil::getValue($node_obj, "field_alert_main_text");
      $this->additional_text = ModelUtil::getValue($node_obj, "field_alert_additional_text");
  }

  /**
   * @return array|null
   */
  public function getTitle() {
    return $this->title;
  }

  /**
   * @return DateTime|false|null
   */
  public function getDate() {
    return $this->date;
  }

  /**
   * @return string
   */
  public function getMainText() {
    return $this->main_text;
  }

  /**
   * @return string
   */
  public function getAdditionalText() {
    return $this->additional_text;
  }
}
