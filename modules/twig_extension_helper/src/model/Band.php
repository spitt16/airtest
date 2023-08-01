<?php
namespace Drupal\twig_extension_helper\model;

use Drupal\twig_extension_helper\util\NodeUtil;

class Band {

  var $title,
    $has_back_to_top,
    $has_title_section,
    $anchor_tag = NULL,
    $card_reference = [],
    $band_type = "General",
    $band_style = "band-style-default",
	$more_about_line = NULL;
 
  function __construct($node_obj) {

    $all_announcement_cards = TRUE;
    $all_nondesc_cards = TRUE;

    foreach($node_obj->field_card_reference as $current_card_reference) {
      $current_card = new Card(NodeUtil::nodeLoad($current_card_reference->target_id));

      if($current_card->getCardType() != "Announcement") {
        $all_announcement_cards = FALSE;
      }

      if($current_card->hasDescription()) {
        $all_nondesc_cards = FALSE;
      }

      array_push($this->card_reference, $current_card);
    }

    if($all_announcement_cards == TRUE) {
      $this->band_style = "band-style-announcements";
    }

    if($all_nondesc_cards == TRUE) {
      $this->band_style = "band-style-nondesc";
    }

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
   * @return array
   */
  public function getCardReference() {
    return $this->card_reference;
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
