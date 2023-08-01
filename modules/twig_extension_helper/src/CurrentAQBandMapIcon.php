<?php
/**
 * Created by IntelliJ IDEA.
 * User: sdave
 * Date: 3/13/2018
 * Time: 3:26 PM
 */

namespace Drupal\twig_extension_helper;

use Drupal\twig_extension_helper\model\LinkImage;
use Drupal\twig_extension_helper\util\ParagraphUtil;

class CurrentAQBandMapIcon {

  var $image_icon, $tooltip_body;


  function __construct($node_obj) {

    $current_image_icon = ParagraphUtil::getParagraphs($node_obj, "field_home_map_icon_image");
    if(!is_null($current_image_icon[0])) {
      $this->image_icon = new LinkImage($current_image_icon[0]);
    }

    if(!is_null($node_obj->field_home_map_icon_tooltip[0])) {
      $this->tooltip_body = $node_obj->field_home_map_icon_tooltip[0]->value;
    }
  }

  /**
   * @return \Drupal\twig_extension_helper\model\LinkImage
   */
  public function getImageIcon() {
    return $this->image_icon;
  }

  /**
   * @return mixed
   */
  public function getTooltipBody() {
    return $this->tooltip_body;
  }

  public function hasLink() {
    return !is_null($this->image_icon->getLinkUrl());
  }

  public function hasTooltip() {
    return isset($this->tooltip_body);
  }


}
