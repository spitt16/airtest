<?php
namespace Drupal\twig_extension_helper\model;

use Drupal\twig_extension_helper\util\NodeUtil;
use Drupal\twig_extension_helper\util\ParagraphUtil;
use Drupal\twig_extension_helper\model\Link;

class LinksCard extends Card {

  var $links = [];

  function __construct($node_obj) {
    parent::__construct($node_obj);

    if(!is_null($node_obj->field_links)) {
      $linkObjects = ParagraphUtil::getParagraphs($node_obj, "field_links");
      foreach ($linkObjects as $link) {
        array_push($this->links, new Link($link));
      }
    }
  }


  /**
   * @return array
   */
  public function getLinks()
  {
    return $this->links;
  }

  /**
   * @return bool
   */
  public function hasDescription() {
    if(($this->links == NULL) || (count($this->links) == 0)) {
      return false;
    }
    return true;
  }

}
