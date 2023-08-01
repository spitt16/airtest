<?php
namespace Drupal\partners\Controller;

use Drupal\Core\Controller\ControllerBase;

class partnersController extends ControllerBase {


  /**
   * Returns a simple page.
   *
   * @return array
   *   A simple renderable array.
   */
  public function partnerPage($term_name, $partner_id) {
    $element['#theme'] = 'partners_template';
    $element['#term_name'] = $term_name;
    $element['#partner_id'] = $partner_id;
    $element['#attached']['library'] = array(
      'partners/partners_helper'
    );
    return $element;
  }
}