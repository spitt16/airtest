<?php
namespace Drupal\twig_extension_helper\model;
use Drupal\file\Entity\File;
use Drupal\image\Entity\ImageStyle;

class Image {
  var $file,
      $image_url,
      $alt_text;

  function __construct($fid, $style=NULL, $alt_text="") {
    $file = File::load($fid);
    $this->file = $file;

    $url = "Not Found";
    $uri = $file->getFileUri();
    if(is_null($style) && !is_null($uri)) {
      $url = file_create_url($uri);
    } else if(!is_null($uri)){
      $url = ImageStyle::load($style)->buildUrl($uri);
    }

    $this->image_url = $url;

    $this->alt_text = $alt_text;//->get('alt')->getString();

  }

  /**
   * @return \Drupal\Core\GeneratedUrl|string
   */
  public function getImageUrl() {
    return $this->image_url;
  }


  public function getLoadedImage() {
    return $this->file;
  }

  /**
   * @return \Drupal\Core\Field\FieldItemListInterface|mixed
   */
  public function getAltText() {
    return $this->alt_text;
  }

}
