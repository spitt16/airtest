<?php
namespace Drupal\twig_extension_helper\model;

use Drupal\twig_extension_helper\util\ParagraphUtil;

class Navigation {
  var $navigation_objs,
    $logo_image,
    $footer_site_text = NULL,
    $social_media_links = [],
    $status_messages = NULL;

  function __construct($node_obj) {
    $headers = ParagraphUtil::getParagraphs($node_obj, "field_navigation_headers");
    $this->navigation_objs = [];
    foreach($headers as $header) {
      array_push($this->navigation_objs, new HeaderNavigationObj($header));
    }

    $this->logo_image = new Image($node_obj->field_logo_image[0]->target_id, null, $node_obj->field_logo_image[0]->description);

    if(!is_null($node_obj->field_footer_site_text[0])) {
      $this->footer_site_text = $node_obj->field_footer_site_text[0]->value;
    }

    $link_images = ParagraphUtil::getParagraphs($node_obj, "field_social_media_links");

    foreach($link_images as $link_image) {
      array_push($this->social_media_links, new LinkImage($link_image, "thumbnail"));
    }

    $this->status_messages =  new StatusMessagesVocabulary('navigation_status_messages');
  }

  /**
   * @return mixed
   */
  public function getNavigationObjs() {
    return $this->navigation_objs;
  }

  public function getFooterNavigationObjs() {
    $tmp_arr = [];

    foreach($this->navigation_objs as $nav_obj) {
      if($nav_obj->getHeaderNavigationLink()->getInFooter()) {
        array_push($tmp_arr, $nav_obj);
      }
    }

    return $tmp_arr;
  }

  public function getTopNavigationObjs() {
    $tmp_arr = [];

    foreach($this->navigation_objs as $nav_obj) {
      if($nav_obj->getHeaderNavigationLink()->getInHeader()) {
        array_push($tmp_arr, $nav_obj);
      }
    }

    return $tmp_arr;
  }

  /**
   * @return \Drupal\twig_extension_helper\model\Image
   */
  public function getLogoImage() {
    return $this->logo_image;
  }

  /**
   * @return null
   */
  public function getFooterSiteText() {
    return $this->footer_site_text;
  }

  public function hasFooterSiteText() {
    if(!is_null($this->footer_site_text) && strlen($this->footer_site_text) > 0) {
      return true;
    }

    return false;
  }

  /**
   * @return array
   */
  public function getSocialMediaLinks() {
    return $this->social_media_links;
  }

  public function getStatusMessage1() {
    return $this->status_messages->getStatusMessage1();
  }

  public function getStatusMessages() {
    return $this->status_messages->getStatusMessages();
  }
}
