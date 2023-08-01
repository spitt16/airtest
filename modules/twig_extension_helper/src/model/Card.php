<?php
namespace Drupal\twig_extension_helper\model;

use Drupal\twig_extension_helper\util\NodeUtil;
use Drupal\twig_extension_helper\util\ParagraphUtil;

class Card {
  var $nid,
    $card_type,
    $name = NULL,
	$titleBlankRows = 0, /** AirNowDrupal Issue #3 cw 2018-04-05 **/
    $mobile_friendly_name = NULL,
    $description = NULL,
    $image = NULL,
    $card_link = NULL;

  function __construct($node_obj) {
    $this->nid = $node_obj->nid[0]->value;
    $card_type_term = NodeUtil::termLoad($node_obj->field_card_type[0]->target_id);
    $this->card_type = $card_type_term->label();

    if(!is_null($node_obj->field_name[0])) {
      $this->name = $node_obj->field_name[0]->value;
    }

	/** AirNowDrupal Issue #3 cw 2018-04-05 **/
    if(!is_null($node_obj->field_title_blank_rows[0])) {
	  $this->titleBlankRows = $node_obj->field_title_blank_rows[0]->value;
	}

    if(!is_null($node_obj->field_mobile_friendly_name[0])) {
      $this->mobile_friendly_name = $node_obj->field_mobile_friendly_name[0]->value;
    }

    if(!is_null($node_obj->field_description[0])) {
      $this->description = $node_obj->field_description[0]->value;
    }

    $link = ParagraphUtil::getParagraphs($node_obj, "field_card_link");

    if(count($link) > 0) {
      $this->card_link = new Link($link[0]);
    }

    if(!is_null($node_obj->field_image[0])) {
      $this->image = new Image($node_obj->field_image[0]->target_id, null, $node_obj->field_image[0]->alt);
    }

  }

  /**
   * @return mixed
   */
  public function getNid() {
    return $this->nid;
  }

  /**
   * @return mixed
   */
  public function getCardType() {
    return $this->card_type;
  }

  /**
   * @return null
   */
  public function getName() {
    return $this->name;
  }
  /** AirNowDrupal Issue #3 cw 2018-04-05
   * @return null
   */
  public function getTitleBlankRows() {
    return $this->titleBlankRows;
  }

  /**
   * @return null
   */
  public function getMobileFriendlyName() {
    return $this->mobile_friendly_name;
  }

  /**
   * @return bool
   */
  public function hasMobileFriendlyName() {
    if(($this->mobile_friendly_name == NULL) || (strlen($this->mobile_friendly_name) == 0)) {
      return false;
    }

    return true;
  }

  /**
   * @return null
   */
  public function getSmartName() {
    if($this->hasMobileFriendlyName()) {
      return $this->mobile_friendly_name;
    } else {
      return $this->name;
    }
  }

  /**
   * @return null
   */
  public function getCardLink() {
    return $this->card_link;
  }



  /**
   * @return null
   */
  public function getDescription() {
    return $this->description;
  }

  /**
   * @return bool
   */
  public function hasDescription() {
    if(($this->description == NULL) || (strlen($this->description) == 0)) {
      return false;
    }
    return true;
  }

  /**
   * @return \Drupal\twig_extension_helper\model\Image|null
   */
  public function getImage() {
    return $this->image;
  }

  /**
   * @return bool
   */
  public function hasImage() {
    if($this->image == NULL) {
      return false;
    }
    return true;
  }


}
