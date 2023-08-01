<?php
namespace Drupal\twig_extension_helper\model;

use Drupal\twig_extension_helper\model\Image;
use Drupal\twig_extension_helper\model\File;
use Drupal\twig_extension_helper\util\ModelUtil;

class Partner {
  var $partner_title = NULL,
	$partner_id = NULL,
	$partner_url = NULL;

  function __construct($pub_obj) {
      $this->partner_name = ModelUtil::getValue($pub_obj, "field_partner_name");
      $this->partner_url = ModelUtil::getValue($pub_obj, "field_partner_url");	 
	  
	  if(!is_null($pub_obj->field_partner_path_id[0])) {
      $this->partner_id = $pub_obj->field_partner_path_id[0]->value;
    }
  }

  /**
   * @return null
   */
  public function getPartnerId()
  {
    return $this->partner_id;
  }
	
  /**
   * @return null
   */
  public function getPartnerName()
  {
    return $this->partner_name;
  }

  /**
   * @return null
   */
  public function getPartnerURL()
  {
    return $this->partner_url;
  }

}
