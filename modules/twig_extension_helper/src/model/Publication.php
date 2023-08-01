<?php
namespace Drupal\twig_extension_helper\model;

use Drupal\twig_extension_helper\model\Image;
use Drupal\twig_extension_helper\model\File;
use Drupal\twig_extension_helper\util\ModelUtil;

class Publication {
  var $publication_title = NULL,
    $publication_description = NULL,
    $publication_image = NULL,
    $publication_id = NULL,
    $publication_file = NULL,
	$publication_size = NULL,
	$publication_pages = NULL;

  function __construct($pub_obj) {
//    if(!is_null($pub_obj->field_publication_title[0])) {
//      $this->publication_title = $pub_obj->field_publication_title[0]->value;
      $this->publication_title = ModelUtil::getValue($pub_obj, "field_publication_title");
	  
	  $this->permanent_publication_name = ModelUtil::getValue($pub_obj, "field_permanent_publication_name");
	   
//    }

//    if(!is_null($pub_obj->field_publication_description[0])) {
//      $this->publication_description = $pub_obj->field_publication_description[0]->value;
      $this->publication_description = ModelUtil::getValue($pub_obj, "field_publication_description");
//    }
// AirNowDrupal Issue 7 Adding Publication size to the twig template   cw 2018-04-04
	  $this->publication_size = ModelUtil::getValue($pub_obj, "field_publication_size");
// AirNowDrupal Issue 7 Adding Publication size to the twig template   cw 2018-04-04
	  $this->publication_pages = ModelUtil::getValue($pub_obj, "field_publication_pages");
// AirNowDrupal AIR 34 Adding Publication date to the twig template   so 2021-07-20
	  $this->publication_date = ModelUtil::getValue($pub_obj, "field_publication_date");
	  
    if(!is_null($pub_obj->field_publication_image[0])) {
      $this->publication_image = new Image($pub_obj->field_publication_image[0]->target_id, null, $pub_obj->field_publication_image[0]->alt);
    }

    if(!is_null($pub_obj->field_publication_file[0])) {
      $this->publication_file = new File($pub_obj->field_publication_file[0]);
    }

    if(!is_null($pub_obj->field_publication_path_id[0])) {
      $this->publication_id = $pub_obj->field_publication_path_id[0]->value;
    }
	  
  }


  /**
   * @return null
   */
  public function getPermanentPublicationName()
  {
    return $this->permanent_publication_name;
  }
  
  /**
   * @return null
   */
  public function getPublicationTitle()
  {
    return $this->publication_title;
  }

  /**
   * @return null
   */
  public function getPublicationDescription()
  {
    return $this->publication_description;
  }

  /**
   * @return \Drupal\twig_extension_helper\model\Image|null
   */
  public function getPublicationImage()
  {
    return $this->publication_image;
  }

  /**
   * @return null
   */
  public function getPublicationFile()
  {
    return $this->publication_file;
  }

  /**
   * @return null
   */
  public function getPublicationId()
  {
    return $this->publication_id;
  }

  /** AirNowDrupal Issue 7 Adding Publication size to the twig template   cw 2018-04-04
   * @return null
   */
  public function getPublicationSize()
  {
    return $this->publication_size;
  }
	
  /** AirNowDrupal Issue 7 Adding Publication size to the twig template   cw 2018-04-04
   * @return null
   */
  public function getPublicationPages()
  {
    return $this->publication_pages;
  }

 /** AirNowDrupal AIR 34 Adding Publication date to the twig template   so 2021-07-20
   * @return null
   */
  public function getPublicationDate()
  {
    return $this->publication_date;
  }
  
}
