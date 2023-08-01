<?php
namespace Drupal\data_providers\Controller;

use Drupal\Core\Controller\ControllerBase;

class dataProvidersController extends ControllerBase {

  /**
   * Returns a simple page.
   *
   * @return array
   *   A simple renderable array.
   */
  public function dataProvidersPage($term_name) {
    $element['#theme'] = 'data_providers_template';
    $element['#term_name'] = $term_name;
    $element['#attached']['library'] = array(
      	'data_providers/data_providers_helper'
    	);
    return $element;
  }
	
}
