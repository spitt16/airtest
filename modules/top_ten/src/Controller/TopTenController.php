<?php
namespace Drupal\top_ten\Controller;
use Symfony\Component\HttpKernel\Exception\NotFoundHttpException;
use Drupal\Core\Controller\ControllerBase;
use Drupal\Core\Access\AccessResult;
use Drupal\Core\Session\AccountInterface;
class TopTenController extends ControllerBase {
  /**
   * Returns a simple page.
   *
   * @return array
   *   A simple renderable array.
   */
   public function topTenPage() {
     $element = array(
       '#attached' => array(
         'library' => array(
           'top_ten/top_ten_helper',
         )
       ),
     );
     $element['#theme'] = 'top_ten_template';

     return $element;
   }

}
