<?php
namespace Drupal\state_pages\Controller;
use Symfony\Component\HttpKernel\Exception\NotFoundHttpException;
use Drupal\Core\Controller\ControllerBase;
use Drupal\Core\Access\AccessResult;
use Drupal\Core\Session\AccountInterface;
class StatePagesController extends ControllerBase {



  /**
   * Returns a simple page.
   *
   * @return array
   *   A simple renderable array.
   */
  public function statePage() {
    $element = array(
      '#attached' => array(
        'library' => array(
          'state_pages/state_pages_helper',
          'state_pages/print',
        )
      ),
    );

    $californiaRegions = json_decode(file_get_contents(__DIR__ . "/../../misc/region_lookup.json"), true);
    $element['#theme'] = 'state_pages_template';
    $element['#attached']['drupalSettings']['california_regions'] = $californiaRegions;
    return $element;
  }
}
