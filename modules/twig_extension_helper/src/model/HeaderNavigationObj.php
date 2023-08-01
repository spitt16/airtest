<?php
namespace Drupal\twig_extension_helper\model;

use Drupal\twig_extension_helper\util\ParagraphUtil;

class HeaderNavigationObj {
  var $header_navigation_link, $main_navigation_links;

  function __construct($header_navigation_obj) {
    $header = ParagraphUtil::getParagraphs($header_navigation_obj, "field_header_navigation_link")[0];
    $navigation_links = ParagraphUtil::getParagraphs($header_navigation_obj, "field_navigation_links");

    $this->main_navigation_links = [];
    $this->header_navigation_link = new NavLink($header);

    foreach($navigation_links as $navigation_link_obj) {
      $main_paragraph = ParagraphUtil::getParagraphs($navigation_link_obj, "field_title_navigation_link");
      $sub_paragraph = ParagraphUtil::getParagraphs($navigation_link_obj, "field_navigation_link");
      array_push($this->main_navigation_links, new MainNavigationObj($main_paragraph, $sub_paragraph));
    }


  }

  /**
   * @return \Drupal\twig_extension_helper\model\NavLink
   */
  public function getHeaderNavigationLink() {
    return $this->header_navigation_link;
  }

  /**
   * @return array
   */
  public function getNavigationLinks() {
    return $this->main_navigation_links;
  }
}
