<?php
namespace Drupal\twig_extension_helper\model;

use Drupal\twig_extension_helper\util\ParagraphUtil;

class SubpageHeader {

  var $subpage_title = NULL,
    $related_announcements = NULL,
    $description = NULL,
    $banner_slides = [];

  function __construct($node_obj) {
    $banners = ParagraphUtil::getParagraphs($node_obj, "field_banner_slides");
    if(!is_null($node_obj->field_subpage_title[0])) {
      $this->subpage_title = $node_obj->field_subpage_title[0]->value;
    }

    if(!is_null($node_obj->field_related_announcements[0])) {
      $this->related_announcements = $node_obj->field_related_announcements[0]->value;
    }

    if(!is_null($node_obj->field_subpage_description[0])) {
      $this->description = $node_obj->field_subpage_description[0]->value;
    }

    if(!is_null($node_obj->field_banner_slides[0])) {
      foreach ($banners as $bannerObject) {
        array_push($this->banner_slides, $this->constructBanner($bannerObject));
      }
    }
  }


  /**
   * @return string
   */
  public function getSubpageTitle()
  {
    return $this->subpage_title;
  }

  /**
   * @return string
   */
  public function getRelatedAnnouncements()
  {
    return $this->related_announcements;
  }

  /**
   * @return string
   */
  public function getDescription()
  {
    return $this->description;
  }

  /**
   * @return array
   */
  public function getBannerSlides()
  {
    return $this->banner_slides;
  }



  /**
   * @return array
   */
  public function constructBanner($bannerObject)
  {
    $banner = [];
    $banner['title'] = $bannerObject->field_banner_title[0]->value;
    $banner['description'] = $bannerObject->field_banner_description[0]->value;
    $banner['image'] = new Image($bannerObject->field_banner_image[0]->target_id);
    return $banner;
  }



}
