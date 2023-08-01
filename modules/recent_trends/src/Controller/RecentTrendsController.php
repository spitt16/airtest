<?php
namespace Drupal\recent_trends\Controller;

use Drupal\Core\Controller\ControllerBase;

class RecentTrendsController extends ControllerBase {



  /**
   * Returns a simple page.
   *
   * @return array
   *   A simple renderable array.
   */
  public function recentTrends() {
//    $element['#theme'] = 'recent_trends_template';
    $element = array(
      '#theme' => 'recent_trends_template',
      '#attached' => array(
        'library' => array(
          'recent_trends/recent_trends_helper',
        ),
      ),
    );
    return $element;

  }

}
