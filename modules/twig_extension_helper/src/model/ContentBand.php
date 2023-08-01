<?php
/**
 * Created by IntelliJ IDEA.
 * User: sdave
 * Date: 2/14/2018
 * Time: 9:20 AM
 */

namespace Drupal\twig_extension_helper\model;


use Drupal\twig_extension_helper\util\ParagraphUtil;

class ContentBand extends Band {
  var $content = [],
      $sidebar = [];

  function __construct($node_obj) {
    parent::__construct($node_obj);

    $this->band_style = "band-style-content";

    $content_objs = ParagraphUtil::getParagraphs($node_obj, "field_band_contents");
    foreach($content_objs as $content_obj) {
      array_push($this->content, new Content($content_obj));
    }

    $sidebar_objs = ParagraphUtil::getParagraphs($node_obj, "field_band_sidebar");
    foreach($sidebar_objs as $sidebar_obj) {
      array_push($this->sidebar, new Sidebar($sidebar_obj));
    }


  }

  /**
   * @return array
   */
  public function getContent() {
    return $this->content;
  }

  /**
   * @return \Drupal\twig_extension_helper\model\Sidebar
   */
  public function getSidebar() {
    return $this->sidebar;
  }



}
