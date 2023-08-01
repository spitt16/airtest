<?php

namespace Drupal\forecast_aq_data_module\Plugin\Block;

use Drupal\Core\Block\BlockBase;
use Drupal\twig_extension_helper\model\ParameterMessageVocabulary;

/**
 * Provides a 'Forecast AQ Data' Block.
 *
 * @Block(
 *   id = "forecast_aq_data_block",
 *   admin_label = @Translation("Forecast AQ Data Block"),
 *   category = @Translation("AQ Data"),
 * )
 */

class ForecastAQDataBlock extends BlockBase {

  /**
   * {@inheritdoc}
*/
  public function build() {
    $build = array(
      '#theme' => 'forecast_aq_data_template',
      '#attached' => array(
        'library' => array(
          'forecast_aq_data_module/forecast_aq_data_helper',
        ),
      ),
    );

    $plan_your_day_descriptions = new ParameterMessageVocabulary('plan_your_day_descriptions');
    $build['#attached']['drupalSettings']['planYourDayDescriptions'] = $plan_your_day_descriptions->getValue();

    return $build;
  }
}
