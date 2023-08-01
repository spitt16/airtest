<?php
namespace Drupal\twig_extension_helper\model;


class MainNavigationObj {
  var $main_navigation_links, $sub_navigation_links;

  function __construct($main_navigation_obj, $sub_navigation_obj) {
    $this->main_navigation_links = [];
    $this->sub_navigation_links = [];

    foreach($main_navigation_obj as $navigation_link_obj) {
      array_push($this->main_navigation_links, new NavLink($navigation_link_obj));
    }

    foreach($sub_navigation_obj as $navigation_link_obj) {
      array_push($this->sub_navigation_links, new NavLink($navigation_link_obj));
    }
  }

  /**
   * @return array
   */
  public function getMainNavigationLinks() {
    return $this->main_navigation_links;
  }

  /**
   * @return array
   */
  public function getSubNavigationLinks() {
    return $this->sub_navigation_links;
  }



}
