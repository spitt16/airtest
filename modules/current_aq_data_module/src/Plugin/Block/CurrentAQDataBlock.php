<?php

namespace Drupal\current_aq_data_module\Plugin\Block;

use Drupal\Core\Block\BlockBase;
use Drupal\twig_extension_helper\model\ParameterMessageVocabulary;
use Drupal\twig_extension_helper\util\BlockUtil;


/**
 * Provides a 'Current AQ Data' Block.
 *
 * @Block(
 *   id = "current_aq_data_block",
 *   admin_label = @Translation("Current AQ Data Block"),
 *   category = @Translation("AQ Data"),
 * )
 */

class CurrentAQDataBlock extends BlockBase {

  /**
   * {@inheritdoc}
*/
  public function build() {
    $config = $this->getConfiguration();
    $band = BlockUtil::getConfigKey($config, "band");

    $build = array(
      '#theme' => 'current_aq_data_template',
      '#attached' => array(
        'library' => array(
          'current_aq_data_module/current_aq_data_helper',
        ),
      ),
      "#band" => $band
    );

    $plan_your_day_descriptions = new ParameterMessageVocabulary('plan_your_day_descriptions');
    $build['#attached']['drupalSettings']['planYourDayDescriptions'] = $plan_your_day_descriptions->getValue();

    if($band->hasChartFilterDescriptions()) {
      $build['#attached']['drupalSettings']['currentBandChartFilterDescriptions'] = $band->getChartFilterDescriptions();
    }

    return $build;
  }
}
