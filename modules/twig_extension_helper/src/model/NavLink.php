<?php
namespace Drupal\twig_extension_helper\model;

use Drupal\Core\Url;

class NavLink {
  var $link_url = NULL,
      $link_title,
      $in_header,
      $in_footer,
      $open_new_tab;

  function __construct($navlink_obj) {
    if(!is_null($navlink_obj->field_navigation_url_link[0])) {
      $this->link_url = Url::fromUri($navlink_obj->field_navigation_url_link[0]->uri);
    }
    $this->link_title = $navlink_obj->field_link_text[0]->value;
    $this->in_header = boolval($navlink_obj->field_include_nav[0]->value);
    $this->in_footer = boolval($navlink_obj->field_include_footer[0]->value);
    if(!is_null($navlink_obj->field_open_in_new_tab[0])) {
      $this->open_new_tab = $navlink_obj->field_open_in_new_tab[0]->value;
    }
  }

  /**
   * @return mixed
   */
  public function getLinkUrl() {
    return $this->link_url;
  }

  /**
   * @return mixed
   */
  public function getLinkTitle() {
    return $this->link_title;
  }

  /**
   * @return mixed
   */
  public function getInHeader() {
    return $this->in_header;
  }

  /**
   * @return mixed
   */
  public function getInFooter() {
    return $this->in_footer;
  }

  /**
   * @return mixed
   */
  public function getOpenNewTab() {
    return $this->open_new_tab;
  }
}
