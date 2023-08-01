<?php
namespace Drupal\twig_extension_helper\model;

use DateTime;
use Drupal\twig_extension_helper\util\ModelUtil;
use Drupal\twig_extension_helper\util\NodeUtil;

/**
 * Class AlertV2Paragraph
 * @package Drupal\twig_extension_helper\model
 *
 * All display settings for an individual alert.
 *
 * Extends and constructs AlertV2 so all functionality is in one object.
 *
 * Not directly constructed via TwigExtensionHelper.  Instead, it is constructed in AlertCollectionV2, which is
 * constructed in TwigExtensionHelper.
 */

class AlertV2Paragraph extends AlertV2 {
  var $node_id = NULL;
  var $is_enabled = NULL;
  var $is_archived = NULL;
  var $display_on_date = NULL;
  var $archive_on_date = NULL;

  function __construct($obj) {
    $this->node_id = ModelUtil::getValue($obj, "field_alert_alert_content");
    $this->is_enabled = boolval(ModelUtil::getValue($obj, "field_alert_is_enabled"));
    $this->is_archived = boolval(ModelUtil::getValue($obj, "field_alert_is_archived"));
    $this->display_on_date = date_create_from_format("Y-m-d", ModelUtil::getTrimmedValue($obj, "field_alert_display_on_date"));
    $this->archive_on_date = date_create_from_format("Y-m-d", ModelUtil::getTrimmedValue($obj, "field_alert_archive_on_date"));
    parent::__construct(NodeUtil::nodeLoad($this->node_id));
  }

  public function getNodeId() {
    return $this->node_id;
  }

  /**
   * @return bool
   */
  public function getIsEnabled() {
    return $this->is_enabled;
  }

  /**
   * @return bool
   */
  public function getIsArchived() {
    return $this->is_archived;
  }

  /**
   * @return DateTime|false|null
   */
  public function getDisplayOnDate() {
    return $this->display_on_date;
  }

  /**
   * @return DateTime|false|null
   */
  public function getArchiveOnDate() {
    return $this->archive_on_date;
  }

  /**
   * @return bool
   */
  public function isVisible() {
    if (!$this->getIsEnabled()) {
      return false;
    }
    if ($this->getDisplayOnDate() && $this->dateIsAfterToday($this->getDisplayOnDate())) {
      return false;
    }
    return true;
  }

  /**
   * @return bool
   */
  public function isArchived() {
    if ($this->getIsArchived()) {
      return true;
    }
    // True if Archive On Date is today or earlier
    if ($this->getArchiveOnDate() && !$this->dateIsAfterToday($this->getArchiveOnDate())) {
      return true;
    }
    return false;
  }

  /**
   * @param $dt
   * @return bool
   */
  public function dateIsAfterToday($dt) {
    $dt->setTime(0, 0);
    $today = new DateTime(); // FIXME: ensure New York tz
    $today->setTime(0,0);
    return $dt > $today;
  }
}
