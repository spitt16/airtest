<?php
namespace Drupal\twig_extension_helper\model;

use Drupal\Core\Url;
use Drupal\twig_extension_helper\util\ModelUtil;

class Link {
  var $link_url = NULL,
    $link_title = NULL,
    $link_tab_location = NULL;

  function __construct($link_obj) {
    if(!is_null($link_obj->field_basic_link_url[0])) {
      $this->link_url = Url::fromUri($link_obj->field_basic_link_url[0]->uri);
    }

    if(!is_null($link_obj->field_basic_link_url[0])) {
      $this->link_title = $link_obj->field_basic_link_url[0]->title;
    }

    if(!is_null($link_obj->field_open_settngs[0])) {
      $this->link_tab_location = ModelUtil::stringToCleanKey($link_obj->field_open_settngs[0]->value);
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
  public function getLinkTitle() {
    return $this->link_title;
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
