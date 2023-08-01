<?php
namespace Drupal\site_map\Controller;

use Drupal\Core\Controller\ControllerBase;

class SiteMapController extends ControllerBase {


  /**
   * Returns a simple page.
   *
   * @return array
   *   A simple renderable array.
   */
  public function siteMap() {
    $element['#theme'] = 'site_map_template';

    return $element;
  }
}
