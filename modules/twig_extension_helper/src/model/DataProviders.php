<?php
namespace Drupal\twig_extension_helper\model;

use Drupal\twig_extension_helper\model\Image;
use Drupal\twig_extension_helper\model\File;
use Drupal\twig_extension_helper\util\ModelUtil;

class DataProviders {
  var $data_provider = NULL,
	  $code = NULL;

  function __construct($pub_obj) {
     $this->data_provider = ModelUtil::getValue($pub_obj, "field_data_provider");	 
	 $this->reporting_area_id = ModelUtil::getValue($pub_obj, "field_reporting_area_id");	 
	//var_dump($this);
	 if(!is_null($pub_obj->field_data_providers_path_id[0])) {
     	$this->data_provider_id = $pub_obj->field_data_providers_path_id[0]->value;
    	}
    }


  /**
   * @return null
   */
  public function getDataProviderName()
  {
    return $this->data_provider;
  }
	
	 /**
   * @return null
   */
  public function getDataProviderCode()
  {
    return $this->data_provider_code;
  }
	
	
 
}
