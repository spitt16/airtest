<?php
namespace Drupal\twig_extension_helper\model;

use Drupal\twig_extension_helper\util\ModelUtil;
use Drupal\twig_extension_helper\util\NodeUtil;

class AnnouncementsBand {

  var $title,
    $has_back_to_top,
    $has_title_section,
    $anchor_tag = NULL,
    $announcement_collection_reference = NULL,
    $band_type = "Announcements",
    $band_style = "band-style-announcements",
	$more_about_line = NULL;
  var $node_id = NULL;

  function __construct($node_obj) {
    $this->node_id = ModelUtil::getValue($node_obj, "field_announcement_collection");
    $this->announcement_collection_reference = new AnnouncementCollectionV2(NodeUtil::nodeLoad($this->node_id));

    $this->title = $node_obj->field_title[0]->value;
    if(!is_null($node_obj->field_anchor_tag[0])) {
      $this->anchor_tag = $node_obj->field_anchor_tag[0]->value;
    }
	/* AirtNowDrupal Issue 5: cw 2018-05-17 */
	if(!is_null($node_obj->field_more_about_line[0])) {
      $this->more_about_line = $node_obj->field_more_about_line[0]->value;
    }
    $this->has_back_to_top = boolval($node_obj->field_has_back_to_top[0]->value);
    $this->has_title_section = boolval($node_obj->field_has_title_section[0]->value);

    $band_type_term = NodeUtil::termLoad($node_obj->field_band_type[0]->target_id);
    $this->band_type = $band_type_term->label();
  }

  public function getACNodeId() {
    return $this->node_id;
  }


  /**
   * @return mixed
   */
  public function getTitle() {
    return $this->title;
  }

  /**
   * @return bool
   */
  public function hasBackToTop() {
    return $this->has_back_to_top;
  }

  /**
   * @return bool
   */
  public function hasTitleSection() {
    return $this->has_title_section;
  }

  /**
   * @return mixed
   */
  public function getAnchorTag() {
    return $this->anchor_tag;
  }
  /** {# AirtNowDrupal Issue 5: cw 2018-05-17 #}
   * @return mixed
   */
  public function getMoreAboutLine() {
    return $this->more_about_line;
  }

  /**
   * @return AnnouncementCollectionV2
   */
  public function getAnnouncementCollectionReference() {
    return $this->announcement_collection_reference;
  }

  /**
   * @return string
   */
  public function getBandStyle() {
    return $this->band_style;
  }

  /**
   * @return null|string
   */
  public function getBandType() {
    return $this->band_type;
  }
}
