<?php
namespace Drupal\publications_pages\Controller;

use Drupal\Core\Controller\ControllerBase;

class PublicationsPagesController extends ControllerBase {


  /**
   * Returns a simple page.
   *
   * @return array
   *   A simple renderable array.
   */
  public function publicationsPage($term_name, $publication_id) {
//    $element['publication'] = \Drupal::service('plugin.manager.block')
//      ->createInstance('publications_pages_block')
//      ->build();
//    $element['#term'] = $term_name;
    $element['#theme'] = 'publications_pages_template';
    $element['#term_name'] = $term_name;
    $element['#publication_id'] = $publication_id;
    $element['#attached']['library'] = array(
      'publications_pages/publications_pages_helper'
    );

    return $element;
  }
}
