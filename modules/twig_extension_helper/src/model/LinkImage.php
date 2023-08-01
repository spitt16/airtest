<?php
namespace Drupal\twig_extension_helper\model;

use Drupal\Core\Url;
use Drupal\twig_extension_helper\util\ModelUtil;

class LinkImage extends Image{
  var $link_url = NULL,
      $link_tab_location = NULL;

  function __construct($node_obj, $style=NULL) {
    parent::__construct($node_obj->field_li_image[0]->target_id, $style, $node_obj->field_li_image[0]->alt);

    if(!is_null($node_obj->field_li_link[0])) {
      $this->link_url = Url::fromUri($node_obj->field_li_link[0]->uri);
    }

    if(!is_null($node_obj->field_open_settngs[0])) {
      $this->link_tab_location = ModelUtil::stringToCleanKey($node_obj->field_open_settngs[0]->value);
    }
  }

  /**
   * @return null
   */
  public function getLinkUrl() {
    return $this->link_url;
  }

  /**
   * @return null
   */
  public function getLinkTabLocation() {
    return $this->link_tab_location;
  }

  public function getLinkTabTarget() {
    return ModelUtil::keyToLinkTarget($this->link_tab_location);
  }
}
