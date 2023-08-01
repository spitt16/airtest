<?php

/**
 * Created by IntelliJ IDEA.
 * User: sdave
 * Date: 3/28/2018
 * Time: 11:27 AM
 */

namespace Drupal\random_marquee_image_loader\Controller;
use \Drupal\twig_extension_helper\model\MarqueeImagesVocabulary;
use Drupal\Core\Controller\ControllerBase;

class RandomMarqueeImageLoader extends ControllerBase {
  public function randomImage(){
    $marquee_images_vocabulary = new MarqueeImagesVocabulary('marquee_images');
    $images = $marquee_images_vocabulary->getValue()["samples"];

    $num = rand(0, count($images) - 1);
    $img = $images[$num];

    $image = "img.jpg";
    $file =    readfile($img);
    $headers = array(
      'Content-Type'     => 'image/jpg',
      'Content-Disposition' => 'inline; filename="'.$file.'"');

    return new Response($image, 200, $headers);
  }
}
