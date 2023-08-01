<?php
/**
 * Created by IntelliJ IDEA.
 * User: sdave
 * Date: 1/23/2018
 * Time: 2:15 PM
 */

namespace Drupal\twig_extension_helper\model;

use Drupal\twig_extension_helper\util\ModelUtil;

class HomeMarquee {
  var $splash_default_message, $splash_sub_message, $marquee_image_vocabulary/*, $node*/;

  function __construct($node_obj) {
    if(!ModelUtil::isFirstNull($node_obj->field_marquee_default_message)) {
      $this->splash_default_message = $node_obj->field_marquee_default_message[0]->value;
    }

    if(!ModelUtil::isFirstNull($node_obj->field_marquee_default_sub_messag)) {
      $this->splash_sub_message = ModelUtil::getValue($node_obj, "field_marquee_default_sub_messag");
    }

    $this->marquee_image_vocabulary = new MarqueeImagesVocabulary('marquee_images');
//    $this->node = $node_obj;
  }

  /**
   * @return mixed
   */
  public function getSplashDefaultMessage() {
    return $this->splash_default_message;
  }

  /**
   * @return mixed
   */
  public function getSplashSubMessage() {
    return $this->splash_sub_message;
  }

  public function hasSplashSubMessage() {
    if(strlen(trim($this->splash_sub_message)) > 0) {
      return true;
    }

    return false;
  }

  /**
   * @return \Drupal\twig_extension_helper\model\MarqueeImagesVocabulary
   */
  public function getMarqueeImageVocabularyValue() {
    return $this->marquee_image_vocabulary->getValue()["samples"];
  }

//  public function getRandomMarqueeImage() {
//    $marquee_image_values = $this->getMarqueeImageVocabularyValue();
//    $random_num = rand( 0 , (count($marquee_image_values) - 1));
//    $random_img = "/marquee_image/random/" . $random_num ;
//    return $random_img;
//  }

  public function getSingleMarqueeImage($i) {
    $marquee_image_values = $this->getMarqueeImageVocabularyValue();
    if($i >= 0 && $i < count($marquee_image_values)) {
      return $marquee_image_values[$i];
    } else {
      return NULL;
    }
  }
}
