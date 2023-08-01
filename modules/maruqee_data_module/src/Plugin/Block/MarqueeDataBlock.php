<?php

namespace Drupal\marquee_data_module\Plugin\Block;

use Drupal\Core\Block\BlockBase;
use Drupal\taxonomy\Entity\Vocabulary;
use Drupal\twig_extension_helper\model\MarqueeImagesVocabulary;
use Drupal\twig_extension_helper\util\BlockUtil;

/**
 * Provides a 'Hello' Block.
 *
 * @Block(
 *   id = "marquee_data_block",
 *   admin_label = @Translation("Marquee Data Block"),
 *   category = @Translation("AQ Data"),
 * )
 */

class MarqueeDataBlock extends BlockBase {

  /**
   * {@inheritdoc}
*/
  public function build() {
    $config = $this->getConfiguration();
    $home_marquee = BlockUtil::getConfigKey($config, "home_marquee");

    $build = array(
      '#theme' => 'marquee_data_template',
      '#attached' => array(
        'library' => array(
          'marquee_data_module/marquee_data_helper',
        )
      ),
      "#homeMarquee" => $home_marquee
    );

    //$marquee_images = new MarqueeImagesVocabulary('marquee_images');
    //$build['#attached']['drupalSettings']['sampleMarqueeImages'] = $marquee_images->getValue();

    $theme_directory = "/" . drupal_get_path('theme', 'anblue');
    $build['#attached']['drupalSettings']['themeDirectory'] = $theme_directory;

//    $marquee_tooltips = new TooltipVocabulary('tooltips');
//    $build['#attached']['drupalSettings']['marqueeTooltips'] = $marquee_tooltips->getValue();
    return $build;
  }
}
