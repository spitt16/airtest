<?php
namespace Drupal\twig_extension_helper\model;

use DateTime;
use Drupal\twig_extension_helper\util\ModelUtil;

/**
 * Class AnnouncementV2
 * @package Drupal\twig_extension_helper\model
 *
 * Information defining an announcement.
 *
 * Not directly constructed via TwigExtensionHelper.  Instead, it is extended by AnnouncementV2Paragraph, which is
 * in turn constructed by AnnouncementCollectionV2.  AnnouncementCollectionV2 is constructed in TwigExtensionHelper.
 */

class AnnouncementV2 {
  var $title = NULL;
  var $date = NULL;
  var $teaser_image = NULL;
  var $main_text = NULL;
  var $additional_text = NULL;

  function __construct($node_obj) {
      $this->title = ModelUtil::getValue($node_obj, "field_ann_title");
      $this->date = date_create_from_format("Y-m-d", ModelUtil::getTrimmedValue($node_obj, "field_ann_date"));
//      $this->teaser_image = ; // field_ann_teaser_image
      $this->main_text = ModelUtil::getValue($node_obj, "field_ann_main_text");
      $this->additional_text = ModelUtil::getValue($node_obj, "field_ann_additional_text");
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
   * @return ???
   */
  public function getTeaserImage() {
    return $this->teaser_image;
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
