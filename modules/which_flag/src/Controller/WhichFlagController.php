<?php
namespace Drupal\which_flag\Controller;
use Symfony\Component\HttpKernel\Exception\NotFoundHttpException;
use Drupal\Core\Controller\ControllerBase;
use Drupal\Core\Access\AccessResult;
use Drupal\Core\Session\AccountInterface;
class WhichFlagController extends ControllerBase {
  /**
   * Returns a simple page.
   *
   * @return array
   *   A simple renderable array.
   */
  public function whichFlagPage() {
    $element = array(
      '#attached' => array(
        'library' => array(
          'which_flag/which_flag_helper',
          'which_flag/print',
        )
      ),
    );
    $element['#theme'] = 'which_flag_template';
    return $element;
  }
   
}
